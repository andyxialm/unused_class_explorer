"""
The MIT License (MIT)

Copyright (c) 2017 andy (https://github.com/andyxialm)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os.path as path
import os
import re

APP_PACKAGE_NAME = 'cn.refactor.xiandu'  # 此处修改成包名
ABS_ROOT_DIR_PATH = '/Users/andy/Documents/refactor/xiandu/app/src/main/java/cn/refactor/xiandu'  # 此处修改成包名的文件夹的绝对路径
SUFFIX_IMPORT = 'import '

file_path_list = []
dot_file_set = set([])
import_packages_list = []


def iterate(dir_path):
    for file_name in os.listdir(dir_path):
        abs_file_path = path.join(dir_path, file_name)
        if path.isdir(abs_file_path):
            iterate(abs_file_path)
        elif path.isfile(abs_file_path) and path.splitext(file_name)[1] == '.java':
            file_path_list.append(abs_file_path)


def analyze_class(abs_file_path):
    file = open(abs_file_path, 'r')
    for line in file.readlines():
        if re.match(SUFFIX_IMPORT, line.strip()) is not None:
            import_packages_list.append(line.strip().rsplit(SUFFIX_IMPORT)[1].rstrip(';'))


def filter_extensional_package(package):
    return str(package).startswith(APP_PACKAGE_NAME) and not str(package).startswith(APP_PACKAGE_NAME + '.R')

import_packages_list = list(filter(filter_extensional_package, import_packages_list))
import_packages_set = set(import_packages_list)


if path.exists(ABS_ROOT_DIR_PATH):
    if path.isdir(ABS_ROOT_DIR_PATH):
        iterate(ABS_ROOT_DIR_PATH)
    elif path.isfile(ABS_ROOT_DIR_PATH):
        file_path_list.append(ABS_ROOT_DIR_PATH)
else:
    raise FileNotFoundError

for file_path in file_path_list:
    analyze_class(file_path)

for file_path in file_path_list:
    file_path = str(file_path).replace('/', '.')
    dot_file = file_path[file_path.index(APP_PACKAGE_NAME): len(file_path) - len('.java')]
    dot_file_set.add(dot_file)

unused_class_set = sorted(dot_file_set - import_packages_set)

for unused_class in unused_class_set:
    print(unused_class)
