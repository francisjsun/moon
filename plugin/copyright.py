# Copyright (C) 2020 Francis Sun, all rights reserved.

import os

import vim


def main():
    current_dir = vim.eval("s:here")
    os.sys.path.append(os.path.join(current_dir, "../external/jupiter"))

    moon_cfg = vim.eval("g:moon_cfg")
    from jupiter import copyright_utility
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
