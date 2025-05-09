import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="問題3：複数ボタン", size=(300, 150))
        panel = wx.Panel(self)

        ok_btn = wx.Button(panel, label="OK", pos=(50, 50))
        cancel_btn = wx.Button(panel, label="Cancel", pos=(150, 50))

        ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
        cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_ok(self, event):
        wx.MessageBox("OKが押されました", "Info")

    def on_cancel(self, event):
        wx.MessageBox("Cancelが押されました", "Info")

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
