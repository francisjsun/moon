try:
    from jupiter import copyright_utility
except ImportError:
    import subprocess
    import sys
    subprocess.run([sys.executable, "-m", "pip", "install", "--user", "-e", \
            "../external/jupiter"])
    from jupiter import copyright_utility

import vim

if __name__ == "__main__":
    cr = copyright_utility.Copyright(vim.eval("g:moon_plugin_copyright_file_path"), \
            vim.eval("g:moon_plugin_copyright_author"))

    # if doc contains any literal quotes, then thoes quotes should be escaped to the 
    # final let command
    doc = cr.Get()
    raw_doc = ""
    for c in doc:
        if c == "\"":
            raw_doc += "\\\""
        else:
            raw_doc += c

    vim.command("let g:moon_plugin_copyright_doc = " + "\"" + raw_doc + "\"")
