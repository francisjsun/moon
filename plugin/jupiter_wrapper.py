# Copyright (C) 2020 Francis Sun, all rights reserved.

import vim
import os
import moon

current_dir = vim.eval('s:here')
os.sys.path.insert(0, os.path.join(current_dir, "../external/jupiter"))
from jupiter import copyright_declaration # noqa: E402
from jupiter import boilerplate # noqa: E402


def get_author():
    author = moon.moon_cfg.get_value('author')
    project_author = moon.moon_project_cfg.get_value('author')
    if project_author != '':
        author = project_author
    return author


def get_vim_let_string(src_str):
    # if string contains any literal quotes, then thoes quotes should be
    # escaped before used in let command
    ret = ""
    for c in src_str:
        if c == "\"":
            ret += "\\\""
        else:
            ret += c

    return ret


def get_copyright_doc():
    current_file = vim.eval('g:moon_current_file_path')
    cr = copyright_declaration.Copyright(current_file, get_author())

    vim.command("let g:moon_copyright_doc = " + "\"" +
                get_vim_let_string(cr.get_declaration()) + "\"")


def get_prefix():
    prefix = moon.moon_project_cfg.get_value('project_name')
    project_name_prefix = moon.moon_project_cfg.get_value(
        'project_name_prefix')
    if project_name_prefix != '':
        prefix = project_name_prefix + '_' + prefix
    return prefix


def get_include_guard():
    current_file = vim.eval('g:moon_current_file_path')
    current_file = current_file.replace(moon.moon_project_dir, '')
    prefix = get_prefix()
    include_guard_lines = boilerplate.get_include_guard(
        current_file, moon.moon_project_cfg.get_value('macro_ignored_dir'),
        prefix)
    vim.command("let g:moon_include_guard = [" +
                "\"" + include_guard_lines[0] + "\","
                "\"" + include_guard_lines[1] + "\","
                "\"\",\"\","  # two empty lines
                "\"" + include_guard_lines[2] + "\"]"
                )


def get_boilerplate():
    current_file = vim.eval('g:moon_current_file_path')
    current_file = current_file.replace(moon.moon_project_dir, '')
    prefix = get_prefix()

    bd = boilerplate.get(
        moon.moon_project_dir, current_file, get_author(),
        moon.moon_project_cfg.get_value('macro_ignored_dir'), prefix)
    vim_bd = vim.bindeval('g:moon_boilerplate')
    if 'copyright_declaration' in bd:
        vim_bd.extend([get_vim_let_string(bd['copyright_declaration']),
                       ""])
    if 'include_guard' in bd:
        include_guard_lines = bd['include_guard']
        vim_bd.extend([include_guard_lines[0],
                       include_guard_lines[1],
                       "", "",
                       include_guard_lines[2]])
    if 'cpp_include_header' in bd:
        vim_bd.extend([bd['cpp_include_header']])


if __name__ == "__main__":
    pass
