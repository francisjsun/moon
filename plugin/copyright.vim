" moon plugin

" here are 3 gloabl vim variable for interacting with moon.py
" g:moon_plugin_copyright_author, g:moon_plugin_copyright_file_path, 
" g:moon_plugin_copyright_doc
let g:moon_plugin_copyright_author = "unknown"
if has("python3") != 1
  echoerr "python3 is not found."
  finish
endif

let s:here = expand('<sfile>:p:h')

function! s:GetCopyrightDoc(file_path, author)
  let g:moon_plugin_copyright_file_path = a:file_path
  let g:moon_plugin_copyright_author = a:author
  execute 'py3f' s:here . '/copyright.py'
  return g:moon_plugin_copyright_doc
endfunction

function! moon#plugin#copyright#InsertCopyright(file_path, author)
  call append(0, s:GetCopyrightDoc(a:file_path, a:author))
endfunction
