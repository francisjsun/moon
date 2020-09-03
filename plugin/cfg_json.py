# Copyright (C) 2020 Francis Sun, all rights reserved.

import os
import json
import vim


class CfgJson:
    def __init__(self, vim_cfg_name, path, boilerplate):
        self.dirty = False
        self.vim_cfg = vim.bindeval(vim_cfg_name)
        self.path = path
        self.boilerplate = boilerplate
        self.cfg = {}
        if os.path.isfile(path):
            with open(path) as f:
                try:
                    self.cfg = json.load(f)
                    self.vim_cfg.update(self.cfg)
                except BaseException:
                    self.cfg = {}

        self.fill_with_boilerplate()

    def update_boilerplater(self, name, value):
        self.boilerplate[name] = value

    def set_path(self, path):
        self.path = path

    def fill_with_boilerplate(self):
        if self.cfg is not None:
            for k in self.boilerplate:
                if k not in self.cfg:
                    self.set_value(k, self.boilerplate[k])

    def set_value(self, name, value):
        self.cfg[name] = value
        self.vim_cfg[name] = value
        self.dirty = True

    def get_value(self, name):
        if name in self.cfg:
            return self.cfg[name]
        else:
            return None

    def flush(self, force=False):
        if force or self.dirty:
            try:
                with open(self.path, 'w') as f:
                    json.dump(self.cfg, f, indent=4)
                    return True
            except OSError:
                return False
