# Copyright (C) 2020 Francis Sun, all rights reserved.

import vim
import os

current_dir = vim.eval('s:here')
os.sys.path.insert(0, os.path.join(current_dir, "../external/jupiter"))
from jupiter import copyright_utility # noqa: E402


def main():
    moon_cfg = vim.eval('g:moon_cfg')
    cr = copyright_utility.Copyright(
        vim.eval('g:moon_plugin_copyright_file_path'),
        moon_cfg['author'])

    # if doc contains any literal quotes, then thoes quotes should be escaped
    # to the final let command
    doc = cr.Get()
    raw_doc = ""
    for c in doc:
        if c == "\"":
            raw_doc += "\\\""
        else:
            raw_doc += c

    vim.command("let g:moon_plugin_copyright_doc = " + "\"" + raw_doc + "\"")


if __name__ == "__main__":
    main()
