"""
【TDD演習用】ScheduleDAOクラス
最初はすべてのメソッドが pass になっています。
この状態から、テストを通すために1つずつ実装していきます。
"""

import sqlite3

DB_NAME = "scheduler.db"

class ScheduleDAO:
    """スケジュールデータへのCRUD操作クラス"""
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        # テーブルが存在しない場合は作成
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

    def create(self, title, description, start_time, end_time, type_):
        """(1) スケジュールを追加"""
        self.cursor.execute('''
            INSERT INTO schedule (title, description, start_time, end_time, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, start_time, end_time, type_))
        self.conn.commit()
        return self.cursor.lastrowid

    def read_all(self):
        """(1) 全スケジュール取得"""
        self.cursor.execute('SELECT * FROM schedule')
        return self.cursor.fetchall()

    def update(self, schedule_id, title, description, start_time, end_time, type_):
        """(2) スケジュール更新"""
        pass

    def delete(self, schedule_id):
        """(3) スケジュール削除"""
        pass

    def close(self):
        """接続を閉じる"""
        pass
