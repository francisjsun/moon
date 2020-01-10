" moon plugin

" here are 3 gloabl vim variable for interacting with moon.py
" g:moon_plugin_copyright_author, g:moon_plugin_copyright_file_path, 
" g:moon_plugin_copyright_doc
let g:moon_plugin_copyright_author = "unknown"

function! Moon#plugin#copyright#get_copyright_doc(file_path, author)
  if has("python3") != 1
    echoerr "python3 is not found."
    return ""
  endif

  let g:moon_plugin_copyright_file_path = a:file_path
  let g:moon_plugin_copyright_author = a:author
  py3f copyright.py
  return g:moon_plugin_copyright_doc
endfunction

function! Moon#plugin#copyright#add_copyright_to_current_file(author)
  echom "add copyright to current file" . %
  1insert Moon#plugin#copyright#get_copyright_doc(%, a:author)
endfunction
