"""JD 分析记录 DAO"""

import json
from datetime import datetime
from typing import Optional

from db.connection import get_connection


def save(title: str, jd_text: str, result_dict: dict) -> int:
    """保存分析结果，返回记录 id"""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO jd_analysis (title, jd_text, result_json, created_at) "
        "VALUES (?, ?, ?, ?)",
        (
            title,
            jd_text,
            json.dumps(result_dict, ensure_ascii=False),
            datetime.now().isoformat(),
        ),
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def list_all() -> list[dict]:
    """列出所有历史记录（按时间倒序，仅返回摘要信息）"""
    conn = get_connection()
    rows = (
        conn.execute(
            "SELECT id, title, created_at FROM jd_analysis ORDER BY created_at DESC"
        )
        .fetchall()
    )
    conn.close()
    return [dict(r) for r in rows]


def get_by_id(record_id: int) -> Optional[dict]:
    """获取单条完整记录（含 result JSON）"""
    conn = get_connection()
    row = conn.execute("SELECT * FROM jd_analysis WHERE id = ?", (record_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    record = dict(row)
    record["result"] = json.loads(record["result_json"])
    return record


def delete(record_id: int):
    """删除一条记录"""
    conn = get_connection()
    conn.execute("DELETE FROM jd_analysis WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
