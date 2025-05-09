import wx

class InputDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title='入力ダイアログ', size=(300, 200))
        self.init_ui()
        self.Centre()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 名前入力
        name_box = wx.BoxSizer(wx.HORIZONTAL)
        name_label = wx.StaticText(panel, label='名前:')
        self.name_input = wx.TextCtrl(panel)
        name_box.Add(name_label, 0, wx.ALL | wx.CENTER, 5)
        name_box.Add(self.name_input, 1, wx.ALL | wx.EXPAND, 5)

        # メッセージ入力
        msg_box = wx.BoxSizer(wx.HORIZONTAL)
        msg_label = wx.StaticText(panel, label='メッセージ:')
        self.msg_input = wx.TextCtrl(panel)
        msg_box.Add(msg_label, 0, wx.ALL | wx.CENTER, 5)
        msg_box.Add(self.msg_input, 1, wx.ALL | wx.EXPAND, 5)

        # ボタン
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, wx.ID_OK, 'OK')
        cancel_button = wx.Button(panel, wx.ID_CANCEL, 'Cancel')
        button_box.Add(ok_button, 0, wx.ALL, 5)
        button_box.Add(cancel_button, 0, wx.ALL, 5)

        # レイアウト
        vbox.Add(name_box, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(msg_box, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(button_box, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        panel.SetSizer(vbox)

    def get_values(self):
        return self.name_input.GetValue(), self.msg_input.GetValue()

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='ダイアログアプリ', size=(400, 300))
        self.init_ui()
        self.Centre()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 入力ボタン
        input_button = wx.Button(panel, label='入力')
        input_button.Bind(wx.EVT_BUTTON, self.on_input)

        # 表示用のテキスト
        self.display_text = wx.StaticText(panel, label='')
        self.display_text.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # レイアウト
        vbox.Add(input_button, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(self.display_text, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(vbox)

    def on_input(self, event):
        dialog = InputDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            name, message = dialog.get_values()
            display_text = f'入力結果：{name} - {message}'
            self.display_text.SetLabel(display_text)
        dialog.Destroy()

def main():
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
