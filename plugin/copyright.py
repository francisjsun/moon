try:
    from jupiter import copyright_utility
except ImportError:
    import subprocess
    import sys
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", \
            "../external/jupiter"])
    from jupiter import copyright_utility

import vim

if __name__ == "__main__":
    cr = copyright_utility.Copyright(vim.eval("g:moon_plugin_copyright_file_path"), \
            vim.eval("g:moon_plugin_copyright_author"))
    vim.command("let g:moon_plugin_copyright_doc = " + cr.Get())
