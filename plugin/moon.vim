" moon plugin

" check python3

function! Moon#get_copyright()
  if has("python3") != 1
    echoerr "python3 is not found."
    return
  endif

  py3f moon.py
  return g:moon_copyright
endfunction
