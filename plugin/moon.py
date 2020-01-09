import vim
try:
    from jupiter import copyright_utility
except ImportError:
    import subprocess
    import sys
    subprocess.run([sys.executable, "-m", "pip", "install", \
            "git+ssh://git@github.com/francisjsun/jupiter.git@master"])
    from jupiter import copyright_utility


cr = copyright_utility.Copyright(vim.current.buffer.name, vim.val("g:moon_author"))
vim.command("let g:moon_copyright = " + cr.Get())
