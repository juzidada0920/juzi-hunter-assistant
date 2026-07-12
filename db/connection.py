"""SQLite 连接管理"""

import os
import sqlite3

import config


def get_connection() -> sqlite3.Connection:
    """获取 SQLite 连接（自动创建 data/ 目录）"""
    os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_connection()
    schema_path = os.path.join(config.PROJECT_ROOT, "db", "schema.sql")
    with open(schema_path, encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
