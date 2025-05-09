import wx

class CheckboxFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='チェックボックスアプリ', size=(300, 200))
        self.panel = wx.Panel(self)
        self.init_ui()
        self.Centre()

    def init_ui(self):
        # チェックボックスの作成
        self.checkbox1 = wx.CheckBox(self.panel, label='チェック1', pos=(20, 20))
        self.checkbox2 = wx.CheckBox(self.panel, label='チェック2', pos=(20, 50))
        self.checkbox3 = wx.CheckBox(self.panel, label='チェック3', pos=(20, 80))

        # 確認ボタンの作成
        self.button = wx.Button(self.panel, label='確認', pos=(20, 120))
        self.button.Bind(wx.EVT_BUTTON, self.on_check)

    def on_check(self, event):
        # チェックボックスの状態を取得
        status1 = 'チェック1: ' + ('ON' if self.checkbox1.IsChecked() else 'OFF')
        status2 = 'チェック2: ' + ('ON' if self.checkbox2.IsChecked() else 'OFF')
        status3 = 'チェック3: ' + ('ON' if self.checkbox3.IsChecked() else 'OFF')

        # メッセージダイアログで表示
        message = f'{status1}\n{status2}\n{status3}'
        wx.MessageBox(message, 'チェック状態', wx.OK | wx.ICON_INFORMATION)

def main():
    app = wx.App()
    frame = CheckboxFrame()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
