import os
import sys

# 親ディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import wx
import unittest
from simple_schedule_dao import ScheduleDAO
from simple_schedule_dao_with_gui import ScheduleFrame

class TestScheduleFrame(unittest.TestCase):
    def setUp(self):
        self.app = wx.App(False)
        self.frame = ScheduleFrame()
        self.dao = self.frame.dao

        # テストデータ準備（既存をクリアしてから挿入）
        self.dao.cursor.execute("DELETE FROM schedule")
        self.dao.create("Test1", "Desc1", "2025-01-01 10:00", "2025-01-01 11:00", "Work")
        self.dao.create("Test2", "Desc2", "2025-01-02 12:00", "2025-01-02 13:00", "Private")
        self.frame.reload_data()

    def test_reload_data_shows_items_in_listctrl(self):
        list_ctrl = self.frame.list_ctrl
        item_count = list_ctrl.GetItemCount()
        self.assertEqual(item_count, 2)

        first_title = list_ctrl.GetItemText(0, 1)
        self.assertEqual(first_title, "Test1")

        second_title = list_ctrl.GetItemText(1, 1)
        self.assertEqual(second_title, "Test2")

    def test_update_button_functionality(self):
        # 最初のアイテムを選択
        self.frame.list_ctrl.Select(0)
        
        # 更新ボタンのイベントをシミュレート
        event = wx.CommandEvent(wx.wxEVT_BUTTON)
        self.frame.on_edit(event)
        
        # ダイアログが表示されたことを確認
        # 注: 実際のダイアログ操作は難しいため、ここではイベントハンドラが
        # 呼び出されたことのみを確認

    def test_exit_button_functionality(self):
        # 終了ボタンのイベントをシミュレート
        event = wx.CommandEvent(wx.wxEVT_BUTTON)
        self.frame.on_exit(event)
        
        # フレームが閉じられたことを確認
        self.assertFalse(self.frame.IsShown())

    def tearDown(self):
        self.frame.Destroy()
        self.app.ExitMainLoop()

if __name__ == "__main__":
    unittest.main()