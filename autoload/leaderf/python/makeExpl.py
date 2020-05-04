#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vim
import os
import os.path
from leaderf.utils import *
from leaderf.explorer import *
import subprocess
from leaderf.manager import *


#*****************************************************
# MakeExplorer
#*****************************************************
class MakeExplorer(Explorer):
    def __init__(self):
        pass

    def getContent(self, *args, **kwargs):
        provider = kwargs.get("arguments", {}).get("--provider", [""])[0]
        result = lfEval("{}()".format(provider)).splitlines()
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

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return
        line = args[0]
        if self.consumer != "":
            lfEval('{}("{}")'.format(self.consumer, line))

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

