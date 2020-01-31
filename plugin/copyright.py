# Copyright (C) 2020 Francis Sun, all rights reserved.

import sys
import os
import vim

sys.path.append(os.path.join(vim.eval("s:here"), "../external/jupiter"))
from jupiter import copyright_utility


if __name__ == "__main__":
    cr = copyright_utility.Copyright(\
            vim.eval("g:moon_plugin_copyright_file_path"),\
            vim.eval("g:moon_plugin_copyright_author"))

    # if the doc contains any literal quotes, then all of thoes quotes should 
    # be escaped for being used in the vim let command
    doc = cr.Get()
    raw_doc = ""
    for c in doc:
        if c == "\"":
            raw_doc += "\\\""
        else:
            raw_doc += c

    vim.command("let g:moon_plugin_copyright_doc = " + "\"" + raw_doc + "\"")
