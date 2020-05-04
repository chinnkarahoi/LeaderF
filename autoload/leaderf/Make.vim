" ============================================================================
" File:        Make.vim
" Description:
" Author:      Yggdroot <archofortune@gmail.com>
" Website:     https://github.com/Yggdroot
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

if leaderf#versionCheck() == 0
    finish
endif

exec g:Lf_py "import vim, sys, os.path"
exec g:Lf_py "cwd = vim.eval('expand(\"<sfile>:p:h\")')"
exec g:Lf_py "sys.path.insert(0, os.path.join(cwd, 'python'))"
exec g:Lf_py "from makeExpl import *"

function! leaderf#Make#Maps()
    nmapclear <buffer>
    nnoremap <buffer> <silent> <CR>          :exec g:Lf_py "makeExplManager.accept()"<CR>
    nnoremap <buffer> <silent> o             :exec g:Lf_py "makeExplManager.accept()"<CR>
    nnoremap <buffer> <silent> <2-LeftMouse> :exec g:Lf_py "makeExplManager.accept()"<CR>
    nnoremap <buffer> <silent> x             :exec g:Lf_py "makeExplManager.accept('h')"<CR>
    nnoremap <buffer> <silent> v             :exec g:Lf_py "makeExplManager.accept('v')"<CR>
    nnoremap <buffer> <silent> t             :exec g:Lf_py "makeExplManager.accept('t')"<CR>
    nnoremap <buffer> <silent> p             :exec g:Lf_py "makeExplManager._previewResult(True)"<CR>
    nnoremap <buffer> <silent> q             :exec g:Lf_py "makeExplManager.quit()"<CR>
    nnoremap <buffer> <silent> i             :exec g:Lf_py "makeExplManager.input()"<CR>
    nnoremap <buffer> <silent> <F1>          :exec g:Lf_py "makeExplManager.toggleHelp()"<CR>
    if has_key(g:Lf_NormalMap, "Make")
        for i in g:Lf_NormalMap["Make"]
            exec 'nnoremap <buffer> <silent> '.i[0].' '.i[1]
        endfor
    endif
endfunction

function! leaderf#Make#managerId()
    " pyxeval() has bug
    if g:Lf_PythonVersion == 2
        return pyeval("id(makeExplManager)")
    else
        return py3eval("id(makeExplManager)")
    endif
endfunction
