import wx

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='テキスト入力アプリ')
        panel = wx.Panel(self)
        
        # テキスト入力欄
        self.text_input = wx.TextCtrl(panel, pos=(50, 50), size=(200, 30))
        
        # 表示ボタン
        display_button = wx.Button(panel, label='表示', pos=(50, 100))
        display_button.Bind(wx.EVT_BUTTON, self.on_display)
        
        # ウィンドウサイズの設定
        self.SetSize((300, 200))
        self.Centre()

    def on_display(self, event):
        # 入力されたテキストを取得
        input_text = self.text_input.GetValue()
        
        # ダイアログで表示
        wx.MessageBox(input_text, '入力されたテキスト', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
