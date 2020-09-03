# Copyright (C) 2020 Francis Sun, all rights reserved.

import os
import re
from moon import moon_cfg


def moon_find_file(dir, regex):
    if os.path.isdir(dir):
        try:
            cur_files = os.listdir(dir)
        except BaseException:
            return None
        for f in cur_files:
            full_path = os.path.join(dir, f)
            if os.path.isdir(full_path):
                ret = moon_find_file(full_path, regex)
                if ret is not None:
                    return ret
            else:
                if isinstance(regex, str):
                    regex = re.compile(regex)
                if regex.match(f):
                    return full_path

        return None


def setup_clang_format():
    # clang format
    if moon_cfg.get_value('clang_format_py') is None:
        # search for file clang-format.py
        clang_format_py_search_dir = "/usr"
        clang_format_py_filename = "clang-format.py"
        clang_format_py_path = moon_find_file(
            clang_format_py_search_dir, clang_format_py_filename)
        if clang_format_py_path is not None:
            moon_cfg.set_value('clang_format_py', clang_format_py_path)


def main():
    setup_clang_format()


if __name__ == "__main__":
    main()
