" ============================================================================
" File:        leaderf.vim
" Description:
" Author:      Yggdroot <archofortune@gmail.com>
" Website:     https://github.com/Yggdroot
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

" Definition of 'arguments' can be similar as
" https://github.com/Yggdroot/LeaderF/blob/master/autoload/leaderf/Any.vim#L85-L140
let s:extension = {
            \   "name": "make",
            \   "help": "navigate the make",
            \   "manager_id": "leaderf#Make#managerId",
            \   "arguments": [
            \        {"name": ["--provider"], "nargs": 1, "help": ""},
            \        {"name": ["--consumer"], "nargs": 1, "help": ""},
            \        {"name": ["--previewer"], "nargs": 1, "help": ""},
            \   ]
            \ }
" In order that `Leaderf make` is available
call g:LfRegisterPythonExtension(s:extension.name, s:extension)

command! -bar -nargs=0 LeaderfMake Leaderf make

" In order to be listed by :LeaderfSelf
call g:LfRegisterSelf("LeaderfMake", "navigate the make")
