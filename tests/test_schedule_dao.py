"""
【演習課題】
TDD演習：ScheduleDAO クラスの動作確認テスト（穴埋め版）
以下の「# TODO」で示された箇所を埋めてください。
"""

import unittest
import sqlite3
import os
import sys
from pathlib import Path
# プロジェクトルートをパスに追加して DAO モジュールを解決できるようにする
sys.path.append(str(Path(__file__).resolve().parent.parent))
from simple_schedule_dao import ScheduleDAO

TEST_DB = "test_scheduler.db"

class TestScheduleDAO(unittest.TestCase):
    """ScheduleDAOのUnitTest"""

    def setUp(self):
        """テストごとに呼ばれる準備処理"""
        self.conn = sqlite3.connect(TEST_DB)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                type TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        self.conn.close()

        # DAO接続
        self.dao = ScheduleDAO()
        self.dao.conn = sqlite3.connect(TEST_DB)
        self.dao.cursor = self.dao.conn.cursor()

    def tearDown(self):
        """テストごとに呼ばれる後処理"""
        self.dao.conn.close()
        os.remove(TEST_DB)

    def test_create_and_read(self):
        """予定追加と取得のテスト"""
        self.dao.create("会議", "打ち合わせ", "2025-04-01 10:00", "2025-04-01 11:00", "固定")
        schedules = self.dao.read_all()
        # 追加されたスケジュール数が1件であることを確認
        self.assertEqual(len(schedules), 1)

        # スケジュールのタイトルが "会議" であることを確認
        self.assertEqual(schedules[0][1], "会議")

    def test_update(self):
        """予定更新テスト"""
        self.dao.create("仮予定", "未定", "2025-04-02 14:00", None, "繰り返し")
        schedule_id = self.dao.read_all()[0][0]

        # スケジュール更新
        count = self.dao.update(schedule_id, "正式予定", "確定", "2025-04-02 14:00", "2025-04-02 15:00", "固定")
        # 更新件数が1件であることを確認
        self.assertEqual(count, 1)

        # 更新後のタイトルが "正式予定" であることを確認
        updated = self.dao.read_all()
        self.assertEqual(updated[0][1], "正式予定")

    def test_update_nonexistent(self):
        """存在しない予定の更新"""
        count = self.dao.update(999, "なし", "なし", "2025-01-01 00:00", None, "固定")
        # 更新件数が0件であることを確認
        self.assertEqual(count, 0)

    def test_delete(self):
        """予定削除テスト"""
        self.dao.create("削除テスト", None, "2025-04-03 09:00", "2025-04-03 10:00", "週間")
        schedule_id = self.dao.read_all()[0][0]

        # 削除操作を呼び出す
        self.dao.delete(schedule_id)

        # スケジュールが0件であることを確認
        schedules_after = self.dao.read_all()
        self.assertEqual(len(schedules_after), 0)

    def test_read_empty(self):
        """スケジュールが存在しない場合"""
        # スケジュール取得結果が空リストであることを確認
        schedules = self.dao.read_all()
        self.assertEqual(schedules, [])

if __name__ == '__main__':
    unittest.main()
