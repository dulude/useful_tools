#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Improved version of the GNU "tree" utility. Based on code originally written by Kevin Newton
(https://github.com/kddnewton/tree).
Improvements are as follows:
- Additional information (equivalent to that of the "ls -lah" command) can be optionally displayed
- Full absolute paths can be optionally displayed
"""

import argparse
import os
import pdb
import subprocess
import sys


class Tree:
    def __init__(self, absolute_paths, truncated_paths, verbose):
        self.absolute_paths = absolute_paths
        self.basepath = "/" + os.path.join(*os.getcwd().split("/")[:-1]) + "/"
        self.dirCount = 0
        self.fileCount = 0
        self.truncated_paths = truncated_paths
        self.verbose = verbose

    def register(self, absolute):
        if os.path.isdir(absolute):
            self.dirCount += 1
        else:
            self.fileCount += 1

    def summary(self):
        return str(self.dirCount) + " directories, " + str(self.fileCount) + " files"

    def walk(self, directory, prefix=""):
        filepaths = sorted([filepath for filepath in os.listdir(directory)])
        for index in range(len(filepaths)):
            if filepaths[index][0] == ".":
                continue

            absolute = os.path.join(directory, filepaths[index])
            self.register(absolute)

            if index == len(filepaths) - 1:
                if os.path.isdir(absolute):
                    file_path = filepaths[index] + "/"
                else:
                    file_path = filepaths[index]
                if self.absolute_paths:
                    file_path = file_path.replace(filepaths[index], os.path.abspath(absolute))
                if self.truncated_paths:
                    file_path = absolute.replace(self.basepath, "")
                print(prefix + "└── " + self.get_file_info(absolute) + file_path)
                if os.path.isdir(absolute):
                    self.walk(absolute, prefix + "    ")
            else:
                if os.path.isdir(absolute):
                    file_path = filepaths[index] + "/"
                else:
                    file_path = filepaths[index]
                if self.absolute_paths or self.truncated_paths:
                    file_path = file_path.replace(filepaths[index], os.path.abspath(absolute))
                if self.truncated_paths:
                    file_path = file_path.replace(self.basepath, "")
                print(prefix + "├── " + self.get_file_info(absolute) + file_path)
                if os.path.isdir(absolute):
                    self.walk(absolute, prefix + "│   ")

    def get_file_info(self, path):
        if self.verbose:
            foo = subprocess.run(["ls", "-lah", path], capture_output=True)
            if os.path.isdir(path):
                info_str = str(foo.stdout).split("\\n")[1]
                info_str = info_str[:-1]
            else:
                info_str = str(foo.stdout).split("\\n")[0]
                info_str = info_str[2:]
                info_str = info_str.replace(path, "")
            info_str = info_str.replace("\\", "  ")
        else:
            info_str = ""
        return info_str


parser = argparse.ArgumentParser(description='Improved version of the GNU "tree" utility')
parser.add_argument('-a', '--absolute_paths', required=False, action='store_true', help='If this option is '
                    'set, the full absolute path will be displayed for each file or directory instead of '
                    'just the filename with no additional path information.')
parser.add_argument('-d', '--directory', required=False, default=os.getcwd(), help='Starting path to process. '
                    'If not explicitly specified by the user, the default value is the current working '
                    'directory. If not explicitly set by the user, the default value is logical "False".')
parser.add_argument('-t', '--truncated_paths', required=False, action='store_true', help='If this option is '
                    'set, the path truncated at the level specified by the --directory input will be '
                    'displayed for each file or directory instead of just the filename with no additional '
                    'path information.')
parser.add_argument('-v', '--verbose', required=False, action='store_true', help='If this option is set, '
                    'additional information (equivalent to that of the "ls -lah" command) will be displayed '
                    'for each file or directory. If not explicitly set by the user, the default value is '
                    'logical "False".')
user_args = parser.parse_args()

if user_args.absolute_paths and user_args.truncated_paths:
    user_args.truncated_paths = False

if user_args.absolute_paths:
    print(os.getcwd()+"/")
elif user_args.truncated_paths:
    print(os.getcwd().split("/")[-1] + "/")
else:
    print(".")
tree = Tree(user_args.absolute_paths, user_args.truncated_paths, user_args.verbose)
tree.walk(user_args.directory)
print("\n" + tree.summary())
