#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
スケジュール管理アプリケーション（GUI版）
simple_schedule_dao.pyの機能にwxPythonを使ったGUIを追加
"""

import wx
import datetime
import os
import sqlite3
from simple_schedule_dao import ScheduleDAO
from db_init import create_database

# データベースファイルのパス
DB_NAME = "scheduler.db"

class ScheduleDialog(wx.Dialog):
    """スケジュール追加・編集用ダイアログ"""
    def __init__(self, parent, title, schedule=None):
        super().__init__(parent, title=title, size=(500, 400))
        
        self.panel = wx.Panel(self)
        self.schedule = schedule  # 編集時はスケジュールデータを受け取る
        
        # ウィジェットの作成
        self.create_widgets()
        
        # 編集の場合、フィールドに値をセット
        if schedule:
            self.fill_fields()
            
        self.Center()
        
    def create_widgets(self):
        """ダイアログのウィジェットを作成"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # タイトル
        title_label = wx.StaticText(self.panel, label="タイトル:")
        self.title_ctrl = wx.TextCtrl(self.panel, size=(400, -1))
        title_box = wx.BoxSizer(wx.HORIZONTAL)
        title_box.Add(title_label, flag=wx.RIGHT, border=8)
        title_box.Add(self.title_ctrl, proportion=1)
        vbox.Add(title_box, flag=wx.EXPAND | wx.ALL, border=10)
        
        # 説明
        desc_label = wx.StaticText(self.panel, label="説明:")
        self.desc_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE, size=(400, 100))
        desc_box = wx.BoxSizer(wx.HORIZONTAL)
        desc_box.Add(desc_label, flag=wx.RIGHT, border=8)
        desc_box.Add(self.desc_ctrl, proportion=1)
        vbox.Add(desc_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        
        # 開始時間
        start_label = wx.StaticText(self.panel, label="開始時間:")
        self.start_ctrl = wx.TextCtrl(self.panel)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.start_ctrl.SetValue(now)
        start_box = wx.BoxSizer(wx.HORIZONTAL)
        start_box.Add(start_label, flag=wx.RIGHT, border=8)
        start_box.Add(self.start_ctrl, proportion=1)
        vbox.Add(start_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        
        # 終了時間
        end_label = wx.StaticText(self.panel, label="終了時間:")
        self.end_ctrl = wx.TextCtrl(self.panel)
        end_time = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
        self.end_ctrl.SetValue(end_time)
        end_box = wx.BoxSizer(wx.HORIZONTAL)
        end_box.Add(end_label, flag=wx.RIGHT, border=8)
        end_box.Add(self.end_ctrl, proportion=1)
        vbox.Add(end_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        
        # タイプ
        type_label = wx.StaticText(self.panel, label="タイプ:")
        self.type_ctrl = wx.Choice(self.panel, choices=["会議", "タスク", "イベント", "その他"])
        self.type_ctrl.SetSelection(0)
        type_box = wx.BoxSizer(wx.HORIZONTAL)
        type_box.Add(type_label, flag=wx.RIGHT, border=8)
        type_box.Add(self.type_ctrl, proportion=1)
        vbox.Add(type_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        
        # ボタン
        btn_sizer = wx.StdDialogButtonSizer()
        ok_btn = wx.Button(self.panel, wx.ID_OK)
        ok_btn.SetDefault()
        btn_sizer.AddButton(ok_btn)
        cancel_btn = wx.Button(self.panel, wx.ID_CANCEL)
        btn_sizer.AddButton(cancel_btn)
        btn_sizer.Realize()
        vbox.Add(btn_sizer, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        
        self.panel.SetSizer(vbox)
        
    def fill_fields(self):
        """編集時に既存データをフィールドにセット"""
        self.title_ctrl.SetValue(self.schedule[1])
        self.desc_ctrl.SetValue(self.schedule[2])
        self.start_ctrl.SetValue(self.schedule[3])
        
        if self.schedule[4]:  # end_timeがNoneでないなら
            self.end_ctrl.SetValue(self.schedule[4])
            
        type_map = {"会議": 0, "タスク": 1, "イベント": 2, "その他": 3}
        if self.schedule[5] in type_map:
            self.type_ctrl.SetSelection(type_map[self.schedule[5]])
    
    def get_schedule_data(self):
        """ダイアログから入力されたスケジュールデータを取得"""
        title = self.title_ctrl.GetValue()
        desc = self.desc_ctrl.GetValue()
        start_time = self.start_ctrl.GetValue()
        end_time = self.end_ctrl.GetValue()
        type_ = self.type_ctrl.GetString(self.type_ctrl.GetSelection())
        
        return title, desc, start_time, end_time, type_


class ScheduleFrame(wx.Frame):
    """スケジュール管理アプリのメインフレーム"""
    def __init__(self):
        super().__init__(None, title="シンプルスケジュール管理", size=(800, 600))
        
        # データベースの初期化と接続
        self.initialize_database()
        self.dao = ScheduleDAO()
        
        self.panel = wx.Panel(self)
        self.create_widgets()
        self.load_schedules()
        
        self.Center()
    
    def initialize_database(self):
        """データベースの初期化"""
        # テスト環境ではDBファイルを削除しない
        # 本番環境では既存のDBファイルがなければ作成する
        
        # データベースとテーブルの作成
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                type TEXT NOT NULL
            );
        """)
        conn.commit()
        conn.close()
        
    def create_widgets(self):
        """UIウィジェットの作成"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # タイトル
        title_text = wx.StaticText(self.panel, label="スケジュール一覧")
        title_font = title_text.GetFont()
        title_font.SetPointSize(14)
        title_font.SetWeight(wx.FONTWEIGHT_BOLD)
        title_text.SetFont(title_font)
        vbox.Add(title_text, flag=wx.ALL, border=10)
        
        # スケジュールリスト
        self.list_ctrl = wx.ListCtrl(self.panel, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'タイトル', width=150)
        self.list_ctrl.InsertColumn(2, '説明', width=200)
        self.list_ctrl.InsertColumn(3, '開始時間', width=150)
        self.list_ctrl.InsertColumn(4, '終了時間', width=150)
        self.list_ctrl.InsertColumn(5, 'タイプ', width=80)
        vbox.Add(self.list_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        
        # ボタン
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        add_btn = wx.Button(self.panel, label="追加")
        edit_btn = wx.Button(self.panel, label="更新")
        delete_btn = wx.Button(self.panel, label="削除")
        exit_btn = wx.Button(self.panel, label="終了")
        
        add_btn.Bind(wx.EVT_BUTTON, self.on_add)
        edit_btn.Bind(wx.EVT_BUTTON, self.on_edit)
        delete_btn.Bind(wx.EVT_BUTTON, self.on_delete)
        exit_btn.Bind(wx.EVT_BUTTON, self.on_exit)
        
        hbox.Add(add_btn, flag=wx.RIGHT, border=5)
        hbox.Add(edit_btn, flag=wx.RIGHT, border=5)
        hbox.Add(delete_btn, flag=wx.RIGHT, border=5)
        hbox.Add(exit_btn)
        
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)
        
        self.panel.SetSizer(vbox)
        
    def load_schedules(self):
        """データベースからスケジュールを読み込んでリストに表示"""
        self.list_ctrl.DeleteAllItems()
        schedules = self.dao.read_all()
        
        for schedule in schedules:
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(schedule[0]))
            for col in range(1, 6):
                value = schedule[col] if schedule[col] is not None else ""
                self.list_ctrl.SetItem(index, col, str(value))
    
    def reload_data(self):
        """データを再読み込みする（テスト用メソッド）"""
        self.load_schedules()
    
    def on_add(self, event):
        """スケジュール追加ボタンのイベントハンドラ"""
        dialog = ScheduleDialog(self, "スケジュール追加")
        if dialog.ShowModal() == wx.ID_OK:
            title, desc, start_time, end_time, type_ = dialog.get_schedule_data()
            if title and start_time:  # 必須項目のチェック
                self.dao.create(title, desc, start_time, end_time, type_)
                self.load_schedules()
            else:
                wx.MessageBox("タイトルと開始時間は必須です", "エラー", wx.OK | wx.ICON_ERROR)
        dialog.Destroy()
    
    def on_edit(self, event):
        """スケジュール編集ボタンのイベントハンドラ"""
        selected = self.list_ctrl.GetFirstSelected()
        if selected == -1:
            wx.MessageBox("編集するスケジュールを選択してください", "警告", wx.OK | wx.ICON_WARNING)
            return
            
        schedule_id = int(self.list_ctrl.GetItemText(selected))
        
        # スケジュールの情報を取得
        schedules = self.dao.read_all()
        schedule = None
        for s in schedules:
            if s[0] == schedule_id:
                schedule = s
                break
                
        if schedule:
            dialog = ScheduleDialog(self, "スケジュール編集", schedule)
            if dialog.ShowModal() == wx.ID_OK:
                title, desc, start_time, end_time, type_ = dialog.get_schedule_data()
                if title and start_time:  # 必須項目のチェック
                    self.dao.update(schedule_id, title, desc, start_time, end_time, type_)
                    self.load_schedules()
                else:
                    wx.MessageBox("タイトルと開始時間は必須です", "エラー", wx.OK | wx.ICON_ERROR)
            dialog.Destroy()
    
    def on_delete(self, event):
        """スケジュール削除ボタンのイベントハンドラ"""
        selected = self.list_ctrl.GetFirstSelected()
        if selected == -1:
            wx.MessageBox("削除するスケジュールを選択してください", "警告", wx.OK | wx.ICON_WARNING)
            return
            
        schedule_id = int(self.list_ctrl.GetItemText(selected))
        
        # 確認ダイアログ
        if wx.MessageBox("選択したスケジュールを削除しますか？", "確認", 
                         wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
            self.dao.delete(schedule_id)
            self.load_schedules()
    
    def on_exit(self, event):
        """アプリケーション終了ボタンのイベントハンドラ"""
        self.Close()
        
    def __del__(self):
        """デストラクタ：接続のクローズ"""
        self.dao.close()


def main():
    """アプリケーションのメイン関数"""
    app = wx.App()
    frame = ScheduleFrame()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main() 