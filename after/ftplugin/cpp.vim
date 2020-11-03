if exists("g:moon_cpp_loaded")
  finish
endif

let g:moon_cpp_loaded = 1
setlocal cino+=g1 cino+=h1

" youcomplete me
" disable auto inserting header
let g:ycm_clangd_args = ['--header-insertion=never']
" set aditional semantic triggers for c-family, any two characters
let g:ycm_semantic_triggers = {
      \ 'c,cpp,hpp,objc': ['re!\w{2}'],
      \ }

" gdb settings
packadd termdebug

function! s:moon_cpp_start_gdb()
  mksession! session.vim
  only
  let l:debug_target = ""

  if l:debug_target == ""
    let l:debug_target = input("Debug program path: \n", "", "file")
    let g:moon_cfg['debug_info']['target'] = l:debug_target
    let g:moon_cfg['dirty'] = 1
  endif
  execute "Termdebug " . l:debug_target

  execute "normal \<C-W>p\<C-W>H"
endfunction

function! s:moon_cpp_quit_gdb()
  Gdb
  call term_sendkeys("", "q\<CR>")
  " source Session.vim
endfunction

command! FSStartGDB call s:moon_cpp_start_gdb()
command! FSQuitGDB call s:moon_cpp_quit_gdb()

nnoremap <F5> :Continue
nnoremap <F9> :Break
nnoremap <F10> :Over
