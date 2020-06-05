" Copyright (C) 2020 Francis Sun, all rights reserved.

" moon plugin
let s:here = expand('<sfile>:p:h')

" check some requirements
if has('python3') == 0
  echoerr "No python3 supported!"
  finish
endif

" g:moon_cfg
" { clang_format_py_path, author, debug_info}
" debug_info: {target, args}
let g:moon_cfg = {'dirty': 0}

" vimrc_pre.py
execute 'py3f' s:here . '/start.py'

" clang-format
" make sure clang-format.py does exist
let g:clang_format_py_found = 0
if filereadable(g:moon_cfg['clang_format_py'])
  let g:clang_format_py_found = 1
endif
function! ClangFormatOnWrite()
  let l:lines = "all"
  if g:clang_format_py_found
    execute "py3f" g:moon_cfg['clang_format_py']
  endif
endfunction
augroup OnWrite
  autocmd!
  autocmd BufWritePre *.h,*.cc,*cpp call ClangFormatOnWrite()
augroup END

" open paired source or header file for current file
let g:fs_paried_file_extension_src = ['c', 'cpp', 'cc']
let g:fs_paried_file_extension_h = 'h'
let g:fs_paried_file_extension_src_default = 'cpp'
function! s:fs_open_paried_file_for_current_file()
let l:file_extension = expand('%:e')
let l:is_my_ext = 0 " 1: header, 2: src
" check against h and src
if l:file_extension == g:fs_paried_file_extension_h
  let l:is_my_ext = 1
endif
if l:is_my_ext == 0
  for ext in g:fs_paried_file_extension_src
    if l:file_extension == ext
      let l:is_my_ext = 2
      break
    endif
  endfor
endif
if l:is_my_ext
  let l:root_path = expand('%:p:r')
  function! s:fs_open_file(file_path)
    if buflisted(a:file_path)
      execute ':b ' . a:file_path
      return 1
    elseif filereadable(a:file_path)
      execute ':e ' . a:file_path
      return 1
    else
      return 0
    endif
  endfunction
  function! s:fs_prompt_to_create_new_file(file_path)
    let l:usr_choice = confirm("Paired file: \n" . a:file_path . 
          \ " was not found, create a new one? (Default: Yes)", "&Yes\n&No", 
          \ 1, "Question")
    if l:usr_choice == 1
      execute ':e ' . a:file_path
    endif
  endfunction
  if l:is_my_ext == 1 " header file
    let l:found_paired = 0
    for ext in g:fs_paried_file_extension_src
      if s:fs_open_file(l:root_path . '.' . ext)
        let l:found_paired = 1
        break
      endif
    endfor
    if l:found_paired == 0
      call s:fs_prompt_to_create_new_file(l:root_path . '.' . 
            \ g:fs_paried_file_extension_src_default)
    endif
  elseif l:is_my_ext == 2 " src file
    let l:header_path = l:root_path . '.' . g:fs_paried_file_extension_h
    if s:fs_open_file(l:header_path) == 0
      call s:fs_prompt_to_create_new_file(l:header_path)
    endif
  endif
else
  echom 'Unsupported file extension: ' . l:file_extension
endif
endfunction

command! OpenPairedFileForCurrentFile call s:fs_open_paried_file_for_current_file()
nnoremap <leader>o :OpenPairedFileForCurrentFile<CR>

" call quit.py when vim before quits
augroup PreVimQuit
  autocmd!
  autocmd VimLeavePre * execute 'py3f' s:here . '/quit.py'
augroup END
