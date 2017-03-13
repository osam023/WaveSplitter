#!/usr/bin/env python
# coding:utf-8
import wx
import os
import sys

import WaveSplit

class MainPanel(wx.Panel):
    __open_path = ''

    def __init__(self, parent, idn, *args, **kw):
        wx.Panel.__init__(self, parent, idn, *args, **kw)
        self._setup()

        sTxt = wx.StaticText(self, -1, u"分割するファイル")
        top = wx.BoxSizer()
        top.Add(sTxt, 0, wx.ALL, 8)
        
        self.txtCtrl = wx.TextCtrl(self, -1, self.__open_path, size = (200, 20), style = wx.TE_RIGHT)
        openBtn = wx.Button(self, -1, u"開く", size = (80, 20))
        openBtn.Bind(wx.EVT_BUTTON, self._open_file)
        fileForm = wx.BoxSizer()
        fileForm.Add(self.txtCtrl, 0, wx.EXPAND | wx.LEFT, 10)
        fileForm.Add(openBtn, 0, wx.EXPAND | wx.LEFT, 10)
        
        splitCap = wx.StaticText(self, -1, u"分割サイズ")
        splitTitle = wx.BoxSizer()
        splitTitle.Add(splitCap, 0, wx.ALL, 8)
        
        self.splitSize = wx.TextCtrl(self, -1, "", size = (40, 20), style = wx.TE_RIGHT)
        splitSizeTxt = wx.StaticText(self, -1, u"個")
        splitForm = wx.BoxSizer()
        splitForm.Add(self.splitSize, 0, wx.EXPAND | wx.LEFT, 10 )
        splitForm.Add(splitSizeTxt, 0, wx.EXPAND | wx.LEFT, 4)
        
        exeBtn = wx.Button(self, -1, u"処理開始", size = (80, 20))
        exeBtn.Bind(wx.EVT_BUTTON, self._run)
        quitBtn = wx.Button(self, -1, u"終了", size = (80, 20))
        quitBtn.Bind(wx.EVT_BUTTON, self._quitApp)
        ctrlForm = wx.BoxSizer()
        ctrlForm.AddStretchSpacer(1)
        ctrlForm.Add(quitBtn, 0, wx.TOP, 10 )
        ctrlForm.Add(exeBtn, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        form = wx.BoxSizer(wx.VERTICAL)
        form.Add(top, 0, wx.EXPAND | wx.LEFT | wx.TOP)
        form.Add(fileForm, 0, wx.EXPAND | wx.LEFT)
        form.Add(splitTitle, 0, wx.EXPAND | wx.LEFT)
        form.Add(splitForm, 0, wx.EXPAND | wx.LEFT)
        form.Add(ctrlForm, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM)
        self.SetSizer(form)
        form.Fit(self)

    def _setup(self):
        self.__open_path = os.path.expanduser('~') + "/Desktop"
        
    def _quitApp(self, event):
        sys.exit(1)
        
    def _run(self, event):
        try:
            value = self.__check(self.splitSize.GetValue())
            ws = WaveSplit.WaveSplitter()
            ws.set_wavefile(self.__open_path)
            ws.set_splitsize(value)
            ws.run()
            dlg = wx.MessageDialog(self, u"Message:  正しく処理されました．", "SUCCESS!", style = wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        except IOError, err:
            self.__alert(u"Message:  ファイルが見つかりません．正しいファイルの場所を指定して下さい．", u"警告")
        except TypeError, err:
            self.__alert(u"Message:  値が入力されていません．．", u"警告")
             
    def __check(self, value):
        try:
            val = int(value)
            if val > 0:
                return val
            else:
                raise ZeroError
        except ZeroError, err:
            self.__alert(u"Message:  「0」が入力されています．「0」以上の数字を入力して下さい．", u"注意")
        except ValueError, err:
            self.__alert(u"Message:  数字以外が入力されています．数字を入力して下さい．", u"注意")
            
    def __alert(self, message, caption):
        dlg = wx.MessageDialog(self, message, caption, style = wx.OK | wx.ICON_HAND)
        dlg.ShowModal()
        dlg.Destroy()

    def _open_file(self, event):
        wildcard = "Wave source (*.wav)|*.wav"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
        )

        if dlg.ShowModal() == wx.ID_OK:
            self.__open_path = dlg.GetPaths()[0]
            self.txtCtrl.SetValue(self.__open_path)


class Error(Exception):
    pass
class ZeroError(Error):
    def __init__(self):
        pass
class FileNotFoundError(Error):
    def __init__(self):
        pass


def main():
    app = wx.PySimpleApp()
    frame = wx.Frame(None, wx.ID_ANY, u"音声ファイル分割ツール", size = (310, 170))
    panel = MainPanel(frame, wx.ID_ANY)
    frame.Show()
    app.MainLoop()
    
if __name__ == '__main__':
    main()
