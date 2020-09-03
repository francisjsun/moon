# Copyright (C) 2020 Francis Sun, all rights reserved.

import vim
import os
from moon import moon_cfg
from moon import moon_project_cfg


current_dir = vim.eval('s:here')
os.sys.path.insert(0, os.path.join(current_dir, "../external/jupiter"))
from jupiter import copyright_utility # noqa: E402
from jupiter import include_guard # noqa: E402


def get_copyright_doc():
    current_file = vim.eval('g:moon_current_file_path')
    author = moon_cfg.get_value('author')
    project_author = moon_project_cfg.get_value('author')
    if project_author != '':
        author = project_author
    cr = copyright_utility.Copyright(current_file, author)

    # if doc contains any literal quotes, then thoes quotes should be escaped
    # to the final let command
    doc = cr.Get()
    raw_doc = ""
    for c in doc:
        if c == "\"":
            raw_doc += "\\\""
        else:
            raw_doc += c

    vim.command("let g:moon_copyright_doc = " + "\"" + raw_doc + "\"")


def get_include_guard():
    current_file = vim.eval('g:moon_current_file_path')
    project_dir = vim.eval('g:moon_project_dir')
    current_file = current_file.replace(project_dir, '')
    prefix = moon_project_cfg.get_value('project_name')
    project_name_prefix = moon_project_cfg.get_value('project_name_prefix')
    if project_name_prefix != '':
        prefix = project_name_prefix + '_' + prefix
    include_guard_lines = include_guard.get_include_guard(
        current_file, prefix)
    vim.command("let g:moon_include_guard = [" +
                "\"" + include_guard_lines[0] + "\","
                "\"" + include_guard_lines[1] + "\","
                "\"\",\"\","  # two empty lines
                "\"" + include_guard_lines[2] + "\"]"
                )


if __name__ == "__main__":
    pass
