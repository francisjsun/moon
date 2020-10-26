# Copyright (C) 2020 Francis Sun, all rights reserved.

import os
import json
import vim


class CfgJson:
    def __init__(self, vim_cfg_name, path, boilerplate):
        self.vim_cfg_name = vim_cfg_name
        self.boilerplate = boilerplate
        self.path = None
        self.dirty = False
        self.initialize(path)

    def initialize(self, path):
        if path == self.path:
            return
        else:
            self.flush()  # flush previous
            self.dirty = False
            vim.command("let " + self.vim_cfg_name + " = {}")
            self.vim_cfg = vim.bindeval(self.vim_cfg_name)
            self.path = path
            if os.path.isfile(path):
                with open(path) as f:
                    try:
                        cfg = json.load(f)
                        self.vim_cfg.update(cfg)
                    except BaseException:
                        vim.command("let " + self.vim_cfg_name + " = {}")
                        # re-bindeval due to new dictionary created
                        self.vim_cfg = vim.bindeval(self.vim_cfg_name)

            self.fill_with_boilerplate()

    def update_boilerplater(self, name, value):
        self.boilerplate[name] = value

    def set_path(self, path):
        self.path = path

    def fill_with_boilerplate(self):
        for k in self.boilerplate:
            if k not in self.vim_cfg:
                # fill up with boilerplate will not make cfg dirty
                self.vim_cfg[k] = self.boilerplate[k]

    def set_value(self, name, value):
        self.vim_cfg[name] = value
        self.dirty = True

    def get_value(self, name):
        # see json dump below
        cfg = vim.eval(self.vim_cfg_name)
        return cfg[name]

    def flush(self, force=False):
        if force or self.dirty:
            try:
                with open(self.path, 'w') as f:
                    # need to use vim.eval here, can't simply use the variable
                    # returned by bindval, that only gives byte type in both
                    # key and value of the dictionary
                    cfg = vim.eval(self.vim_cfg_name)
                    # dump a sorted json
                    json.dump(dict(sorted(cfg.items())), f, indent=4)
                    self.dirty = False
                    return True
            except OSError:
                return False
