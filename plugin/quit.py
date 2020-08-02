# Copyright (C) 2020 Francis Sun, all rights reserved.

import vim
import os
import os.path
import json

vim_moon_cfg = vim.eval("g:moon_cfg")

moon_cfg_file_name = "moon_cfg.json"
moon_cfg_file_path = os.path.join(vim.eval("g:vimrc_dir"), moon_cfg_file_name)

# NOTE! Value in dict returned by vim.eval is a string.
if vim_moon_cfg['dirty'] != '0':
    try:
        with open(moon_cfg_file_path, 'w') as moon_cfg_file:
            vim_moon_cfg['dirty'] = 0
            json.dump(vim_moon_cfg, moon_cfg_file)
    except OSError as err:
        print(err.strerror + "@" + err.filename)
        vim.command("call input(\"Press Enter to quit.\")")
