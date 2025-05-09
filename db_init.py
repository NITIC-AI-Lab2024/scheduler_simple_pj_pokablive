import sqlite3
import os

DB_NAME = "scheduler.db"

def create_database():
    """データベースを作成する"""
    # 既存のDBファイルが存在する場合は削除
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    # データベース接続
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # スケジュールテーブルの作成
    cursor.execute('''
        CREATE TABLE schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            start_time TEXT NOT NULL,
            end_time TEXT,
            type TEXT NOT NULL
        )
    ''')

    # 変更を保存
    conn.commit()
    conn.close()

    print(f"データベース '{DB_NAME}' が作成されました。")

if __name__ == "__main__":
    create_database()