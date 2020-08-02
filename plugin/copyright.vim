" Copyright (C) 2020 Francis Sun, all rights reserved.

" moon plugin

let s:here = expand('<sfile>:p:h')

function! s:get_copyright_doc(file_path)
  let g:moon_plugin_copyright_file_path = a:file_path
  execute 'py3f' s:here . '/copyright.py'
  return g:moon_plugin_copyright_doc
endfunction

function! s:add_copyright_to_current_file()
  " [""] will append an aditional empty line
  call append(0, [s:get_copyright_doc(expand('%:p')), ""])
endfunction

command! InsertCopyright call s:add_copyright_to_current_file()
