# Copyright (C) 2020 Francis Sun, all rights reserved.

import vim
import os
from cfg_json import CfgJson


def vim_setup():
    vim.command("chdir " + moon_project_dir)
    vim.command("set makeprg=" + moon_project_cfg.get_value('makeprg'))


# moon cfg
moon_cfg_file_name = "moon_cfg.json"
moon_cfg_file_path = os.path.join(vim.eval("g:vimrc_dir"), moon_cfg_file_name)
moon_cfg = CfgJson('g:moon_cfg', moon_cfg_file_path, {'author': "Unkown"})


def find_file(dir_name, dst_file_name):
    if os.path.isdir(dir_name):
        try:
            cur_files = os.listdir(dir_name)
        except BaseException:
            return None
        for f in cur_files:
            full_path = os.path.join(dir_name, f)
            if os.path.isdir(full_path):
                ret = find_file(full_path, dst_file_name)
                if ret is not None:
                    return ret
            else:
                if f == dst_file_name:
                    return full_path

        return None


def setup_clang_format():
    # clang format
    if moon_cfg.get_value('clang_format_py') is None:
        # search for file clang-format.py
        clang_format_py_search_dir = "/usr"
        clang_format_py_filename = "clang-format.py"
        clang_format_py_path = find_file(
            clang_format_py_search_dir, clang_format_py_filename)
        if clang_format_py_path is not None:
            moon_cfg.set_value('clang_format_py', clang_format_py_path)


# moon project cfg
moon_project_dir = vim.eval("getcwd()")
moon_project_cfg_file_name = "moon_project.json"
moon_project_cfg = CfgJson(
    'g:moon_project_cfg',
    os.path.join(moon_project_dir, moon_project_cfg_file_name),
    {
        'project_name': os.path.basename(moon_project_dir),
        'project_name_prefix': "",
        # ignored dir relatived to project dir
        'macro_ignored_dir': ["src"],
        'author': "",
        'makeprg': "cmake",
        'debug_info': {
            'target': "",
            'args': ""
        }
    })
vim_setup()


def find_file_backforward(dir_name, dst_file_name):
    if os.path.isdir(dir_name):
        try:
            cur_files = os.listdir(dir_name)
        except BaseException:
            return None
        for f in cur_files:
            full_path = os.path.join(dir_name, f)
            if os.path.isfile(full_path):
                if f == dst_file_name:
                    return full_path
        next_dir_name = os.path.dirname(dir_name)
        if next_dir_name != dir_name:
            return find_file_backforward(next_dir_name, dst_file_name)
        else:
            return None


def setup_moon_project():
    global moon_project_dir
    current_buffer_dir = os.path.dirname(os.path.abspath(
        vim.current.buffer.name))
    if moon_project_dir in current_buffer_dir:
        return
    moon_project_cfg_file_path = find_file_backforward(os.path.dirname(
        vim.current.buffer.name), moon_project_cfg_file_name)
    if moon_project_cfg_file_path is None:
        moon_project_cfg_file_path = os.path.join(vim.eval("getcwd()"),
                                                  moon_project_cfg_file_name)
    moon_project_dir = os.path.dirname(moon_project_cfg_file_path)
    moon_project_cfg.update_boilerplater('project_name', os.path.basename(
        moon_project_dir))
    moon_project_cfg.initialize(moon_project_cfg_file_path)
    vim_setup()
