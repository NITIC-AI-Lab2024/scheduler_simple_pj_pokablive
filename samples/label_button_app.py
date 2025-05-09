import wx

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='wxPython Demo')
        panel = wx.Panel(self)
        
        # テキスト表示
        text = wx.StaticText(panel, label='こんにちはwxPython!', pos=(50, 50))
        
        # 閉じるボタン
        close_button = wx.Button(panel, label='閉じる', pos=(50, 100))
        close_button.Bind(wx.EVT_BUTTON, self.on_close)
        
        # ウィンドウサイズの設定
        self.SetSize((300, 200))
        self.Centre()

    def on_close(self, event):
        self.Close()

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()