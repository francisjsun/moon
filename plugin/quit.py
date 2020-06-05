# Copyright (C) 2020 Francis Sun, all rights reserved.

import vim
import os
import os.path
import json

vim_moon_cfg = vim.eval("g:moon_cfg")

moon_cfg_file_name = "moon_cfg.json"
moon_cfg_file_path = os.path.join(vim.eval("g:vimrc_dir"), moon_cfg_file_name)
if vim_moon_cfg['dirty']:
    with open(moon_cfg_file_path, 'w') as moon_cfg_file:
        json.dump(vim_moon_cfg, moon_cfg_file)
