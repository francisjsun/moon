" Copyright (C) 2020 Francis Sun, all rights reserved.

" check some requirements
if has('python3') == 0
  echoerr "No python3 supported!"
  finish
endif

" moon plugin
let s:here = expand('<sfile>:p:h')

" append current path to python import path
py3 << EOF
import os
import vim
os.sys.path.append(vim.eval('s:here'))
import moon
EOF

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
augroup MoonOnWrite
  autocmd!
  autocmd BufWritePre *.h,*.cc,*cpp call ClangFormatOnWrite()
augroup END

" open paired source or header file for current file
let g:moon_paried_file_extension_src = ['c', 'cpp', 'cc']
let g:moon_paried_file_extension_h = ['h', 'hpp']
function! s:moon_open_paried_file_for_current_file()
  let l:file_extension = expand('%:e')
  let l:is_my_ext = 0 " 1: header, 2: src
  " check against h or hpp and src
  for ext in g:moon_paried_file_extension_h
    if l:file_extension == ext
      let l:is_my_ext = 1
      break
    endif
  endfor
  if l:is_my_ext == 0
    for ext in g:moon_paried_file_extension_src
      if l:file_extension == ext
        let l:is_my_ext = 2
        break
      endif
    endfor
  endif
  if l:is_my_ext
    let l:root_path = expand('%:p:r')
    function! s:moon_open_file(file_path)
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
    function! s:moon_prompt_to_create_new_file(file_path)
      let l:usr_choice = confirm("Paired file: \n" . a:file_path . 
            \ " was not found, create a new one? (Default: Yes)", "&Yes\n&No", 
            \ 1, "Question")
      if l:usr_choice == 1
        execute ':e ' . a:file_path
      endif
    endfunction
    let l:found_paired = 0
    if l:is_my_ext == 1 " header file
      for ext in g:moon_paried_file_extension_src
        if s:moon_open_file(l:root_path . '.' . ext) == 1
          let l:found_paired = 1
          break
        endif
      endfor
      if l:found_paired == 0
        " create source file
        call s:moon_prompt_to_create_new_file(l:root_path . '.' . 
              \ g:moon_project_cfg['cpp_file_default_extension'][1])
      endif
    elseif l:is_my_ext == 2 " src file
      for ext in g:moon_paried_file_extension_h
        if s:moon_open_file(l:root_path . '.' . ext) == 1
          let l:found_paired = 1
          break
        endif
      endfo
      if l:found_paired == 0
        " create header file
        call s:moon_prompt_to_create_new_file(l:root_path . '.' . 
              \ g:moon_project_cfg['cpp_file_default_extension'][0])
      endif
    endif
  else
    echom 'Unsupported file extension: ' . l:file_extension
  endif
endfunction

command! MoonOpenPairedFileForCurrentFile 
      \ call s:moon_open_paried_file_for_current_file()
nnoremap <leader>o :MoonOpenPairedFileForCurrentFile<CR>

" jupiter wrapper
py3 << EOF
import jupiter_wrapper
EOF
" insert copyright
function! s:get_copyright_doc(file_path)
  let g:moon_current_file_path = a:file_path
py3 << EOF
jupiter_wrapper.get_copyright_doc()
EOF
  return g:moon_copyright_doc
endfunction

function! s:insert_copyright_to_current_file()
  " [""] will append an aditional empty line
  call append(0, [s:get_copyright_doc(expand('%')), ""])
endfunction

command! MoonInsertCopyright call s:insert_copyright_to_current_file()

" insert include guard
function! s:get_include_guard(file_path)
  let g:moon_current_file_path = a:file_path
py3 << EOF
jupiter_wrapper.get_include_guard()
EOF
  return g:moon_include_guard
endfunction

function! s:insert_include_guard_to_current_file()
  call append(line("."), s:get_include_guard(expand('%')))
endfunction

command! MoonInsertIncludeGuard call s:insert_include_guard_to_current_file()

" boilerplate
function! s:get_boilerplate(file_path)
  let g:moon_current_file_path = a:file_path
  let g:moon_boilerplate = []
py3 << EOF
jupiter_wrapper.get_boilerplate()
EOF
  return g:moon_boilerplate
endfunction

function! s:insert_boilerplate()
  call append(0, s:get_boilerplate(expand('%')))
endfunction

augroup MoonNewFile
  autocmd!
  autocmd BufNewFile * call s:insert_boilerplate()
augroup END

" flush moon_project_file
function! s:flush_moon_project_file()
py3 << EOF
moon.moon_project_cfg.flush(True)
EOF
endfunction
command! MoonFlushMoonProjectFile call s:flush_moon_project_file()

" update moon project
function! s:update_moon_project()
py3 << EOF
moon.update_moon_project()
EOF
endfunction

augroup MoonEnterFile
  autocmd!
  autocmd BufEnter * call s:update_moon_project()
augroup END

" call quit.py when vim before quits
augroup MoonPreVimQuit
  autocmd!
  autocmd VimLeavePre * execute 'py3f' s:here . '/quit.py'
augroup END
