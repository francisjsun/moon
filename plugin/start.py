# Copyright (C) 2020 Francis Sun, all rights reserved.

import vim
import os
import os.path
import re
import json


def moon_find_file(dir, regex):
    if os.path.isdir(dir):
        try:
            cur_files = os.listdir(dir)
        except BaseException:
            return None
        for f in cur_files:
            full_path = os.path.join(dir, f)
            if os.path.isdir(full_path):
                ret = moon_find_file(full_path, regex)
                if ret is not None:
                    return ret
            else:
                if isinstance(regex, str):
                    regex = re.compile(regex)
                if regex.match(f):
                    return full_path

        return None


moon_cfg_file_name = "moon_cfg.json"
moon_cfg_file_path = os.path.join(vim.eval("g:vimrc_dir"), moon_cfg_file_name)
moon_cfg_file = None
vim_moon_cfg = vim.bindeval("g:moon_cfg")
moon_cfg = None

if os.path.isfile(moon_cfg_file_path):
    with open(moon_cfg_file_path) as f:
        try:
            moon_cfg = json.load(f)
        except BaseException:
            pass

if moon_cfg is None:
    moon_cfg_file = open(moon_cfg_file_path, 'w')
    moon_cfg = {}


# clang format
if 'clang_format_py' not in moon_cfg:
    # search for file clang-format.py
    clang_format_py_search_dir = "/usr"
    clang_format_py_filename = "clang-format.py"
    moon_cfg['clang_format_py'] = moon_find_file(
            clang_format_py_search_dir, clang_format_py_filename)

# copyright author
if 'author' not in moon_cfg:
    moon_cfg['author'] = "Unknown"


# TODO move debug info into project cfg
# if 'debug_info' not in moon_cfg:
#     moon_cfg['debug_info'] = {'target': '', 'args': ''}
# else:
#     debug_info = moon_cfg['debug_info']
#     if 'target' not in debug_info:
#         moon_cfg['target'] = ''
#     if 'args' not in debug_info:
#         moon_cfg['args'] = ''

vim_moon_cfg.update(moon_cfg)


# save cfg file
if moon_cfg_file is not None:
    json.dump(moon_cfg, moon_cfg_file)
    moon_cfg_file.close()
