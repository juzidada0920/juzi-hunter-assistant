"""JD 分析模块 —— 调用 DeepSeek API 生成搜索栏位配置"""

import json

from openai import OpenAI

import config
from ai.prompt_templates import build_jd_analysis_messages


def analyze_jd(jd_text: str) -> dict:
    """分析 JD 文本，返回搜索栏位配置建议。

    Args:
        jd_text: JD 原文（纯文本）

    Returns:
        dict: 包含 search_fields、keyword_combinations、talent_profile 的字典。
              调用失败时返回 {"error": "错误描述"}。
    """
    client = OpenAI(
        api_key=config.DEEPSEEK_API_KEY,
        base_url=config.DEEPSEEK_BASE_URL,
    )

    try:
        response = client.chat.completions.create(
            model=config.MODEL,
            max_tokens=2000,
            messages=build_jd_analysis_messages(jd_text),
        )

        raw_text = response.choices[0].message.content

        if not raw_text:
            return {"error": "AI 返回了空内容，请重试"}

        # DeepSeek 有时会在 JSON 外层包裹 ```json ... ```，做一下清理
        if raw_text.startswith("```"):
            lines = raw_text.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            raw_text = "\n".join(lines)

        result = json.loads(raw_text)
        return result

    except json.JSONDecodeError as e:
        return {
            "error": f"AI 返回的内容无法解析为 JSON：{str(e)}",
            "raw_response": raw_text if "raw_text" in dir() else "",
        }
    except Exception as e:
        return {"error": f"API 调用失败：{str(e)}"}
