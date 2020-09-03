# Copyright (C) 2020 Francis Sun, all rights reserved.

import vim
import os
from cfg_json import CfgJson


# moon cfg
moon_cfg_file_name = "moon_cfg.json"
moon_cfg_file_path = os.path.join(vim.eval("g:vimrc_dir"), moon_cfg_file_name)
moon_cfg = CfgJson('g:moon_cfg', moon_cfg_file_path, {'author': "Unkown"})

# moon project cfg
moon_project_cfg_file_name = "moon_project.json"
vim_moon_project_cfg = vim.bindeval("g:moon_project_cfg")
project_dir = vim.eval("g:moon_project_dir")
moon_project_cfg_file_path = os.path.join(project_dir,
                                          moon_project_cfg_file_name)

moon_project_cfg = CfgJson('g:moon_project_cfg', moon_project_cfg_file_path,
                           {
                               'project_name': os.path.split(project_dir)[1],
                               'project_name_prefix': "",
                               'author': "Unknown",
                               'debug_info': {
                                   'target': "",
                                   'args': ""
                               }
                           })
