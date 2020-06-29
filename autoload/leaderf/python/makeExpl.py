#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import subprocess

import vim
from leaderf.explorer import *
from leaderf.manager import *
from leaderf.utils import *


#*****************************************************
# MakeExplorer
#*****************************************************
class MakeExplorer(Explorer):
    def __init__(self):
        pass

    def getContent(self, *args, **kwargs):
        provider = kwargs.get("arguments", {}).get("--provider", [""])[0]
        result = lfEval("{}()".format(provider))
        if not isinstance(result, list):
            result = result.splitlines()
        return result

    def getStlCategory(self):
        return "Make"

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))


#*****************************************************
# MakeExplManager
#*****************************************************
class MakeExplManager(Manager):

    def __init__(self):
        self.consumer = ""
        self.previewer = ""
        super(MakeExplManager, self).__init__()

    def startExplorer(self, win_pos, *args, **kwargs):
        self.consumer = kwargs.get("arguments", {}).get("--consumer", [""])[0]
        self.previewer = kwargs.get("arguments", {}).get("--previewer", [""])[0]
        super(MakeExplManager, self).startExplorer(win_pos, *args, **kwargs)

    def _getExplClass(self):
        return MakeExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Make#Maps()")

    def _needPreview(self, preview):
        super(MakeExplManager, self)._needPreview(preview)
        return lfEval("get(g:, 'Lf_PreviewInPopup', 0)") == '1'

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return
        line = args[0]
        if self.consumer != "":
            lfEval("{}('{}')".format(self.consumer, line.replace("'", "\\'")))
            return
        if len(args) == 0:
            return
        file = args[0]
        try:
            if not os.path.isabs(file):
                if self._getExplorer()._cmd_work_dir:
                    file = os.path.join(self._getExplorer()._cmd_work_dir, lfDecode(file))
                else:
                    file = os.path.join(self._getInstance().getCwd(), lfDecode(file))
                file = os.path.normpath(lfEncode(file))

            if kwargs.get("mode", '') != 't' or (lfEval("get(g:, 'Lf_DiscardEmptyBuffer', 0)") == '1'
                    and len(vim.tabpages) == 1 and len(vim.current.tabpage.windows) == 1
                    and vim.current.buffer.name == '' and len(vim.current.buffer) == 1
                    and vim.current.buffer[0] == '' and not vim.current.buffer.options["modified"]):
                if lfEval("get(g:, 'Lf_JumpToExistingWindow', 0)") == '1':
                    lfCmd("edit %s" % escSpecial(file))
                else:
                    if vim.current.buffer.options["modified"]:
                        lfCmd("hide edit %s" % escSpecial(file))
                    else:
                        lfCmd("edit %s" % escSpecial(file))
            else:
                lfCmd("Tabdrop %s" % escSpecial(file))
        except vim.error as e: # E37
            lfPrintError(e)

    def _getDigest(self, line, mode):
        """
        specify what part in the line to be processed and highlighted
        Args:
            mode: 0, 1, 2, return the whole line
        """
        if not line:
            return ''
        return line

    def _getDigestStartPos(self, line, mode):
        """
        return the start position of the digest returned by _getDigest()
        Args:
            mode: 0, 1, 2, return 1
        """
        return 0

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" x : open file under cursor in a horizontally split window')
        help.append('" v : open file under cursor in a vertically split window')
        help.append('" t : open file under cursor in a new tabpage')
        help.append('" i : switch to input mode')
        help.append('" p : preview the result')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help

    def _afterEnter(self):
        super(MakeExplManager, self)._afterEnter()

    def _beforeExit(self):
        super(MakeExplManager, self)._beforeExit()

    def _previewInPopup(self, *args, **kwargs):
        if len(args) == 0:
            return

        line = args[0]
        saved_eventignore = vim.options['eventignore']
        vim.options['eventignore'] = 'BufWinEnter'
        try:
            line = args[0]
            if self.previewer != "":
                line = lfEval('{}("{}")'.format(self.previewer, line))
            if os.path.isfile(line):
                buf_number = lfEval("bufadd('{}')".format(escQuote(line)))
                self._createPopupPreview(line, buf_number, 0)
        finally:
            vim.options['eventignore'] = saved_eventignore


#*****************************************************
# makeExplManager is a singleton
#*****************************************************
makeExplManager = MakeExplManager()

__all__ = ['makeExplManager']
