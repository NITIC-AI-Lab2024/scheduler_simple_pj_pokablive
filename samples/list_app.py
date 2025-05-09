import wx

class ListFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='リストアプリ', size=(400, 300))
        self.panel = wx.Panel(self)
        self.init_ui()
        self.Centre()

    def init_ui(self):
        # ListCtrlの作成
        self.list_ctrl = wx.ListCtrl(
            self.panel,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        
        # 列の追加
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, '名前', width=100)
        self.list_ctrl.InsertColumn(2, 'メッセージ', width=200)

        # 初期データの追加
        self.add_initial_data()

        # ボタンの作成
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        update_button = wx.Button(self.panel, label='更新')
        exit_button = wx.Button(self.panel, label='終了')
        
        # ボタンのイベントハンドラを設定
        update_button.Bind(wx.EVT_BUTTON, self.on_update)
        exit_button.Bind(wx.EVT_BUTTON, self.on_exit)

        # ボタンをサイザーに追加
        button_sizer.Add(update_button, 0, wx.ALL, 5)
        button_sizer.Add(exit_button, 0, wx.ALL, 5)

        # メインのサイザーを作成
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.panel.SetSizer(main_sizer)

    def add_initial_data(self):
        # 初期データを追加
        initial_data = [
            ('1', 'Alice', 'こんにちは'),
            ('2', 'Bob', 'おはよう'),
            ('3', 'Carol', 'こんばんわ')
        ]
        self.add_data_to_list(initial_data)

    def add_data_to_list(self, data):
        # リストをクリア
        self.list_ctrl.DeleteAllItems()
        # データを追加
        for index, (id_, name, message) in enumerate(data):
            self.list_ctrl.InsertItem(index, id_)
            self.list_ctrl.SetItem(index, 1, name)
            self.list_ctrl.SetItem(index, 2, message)

    def on_update(self, event):
        # 更新後のデータ
        updated_data = [
            ('4', 'Dave', 'やあ'),
            ('5', 'Eve', 'お疲れ様')
        ]
        self.add_data_to_list(updated_data)

    def on_exit(self, event):
        self.Close()

def main():
    app = wx.App()
    frame = ListFrame()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
