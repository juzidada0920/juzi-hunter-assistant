"""JD 分析模块 —— 调用 Claude API 生成搜索栏位配置"""

import json

import anthropic

import config
from ai.prompt_templates import JD_ANALYSIS_SYSTEM_PROMPT, build_jd_analysis_prompt


def analyze_jd(jd_text: str) -> dict:
    """分析 JD 文本，返回搜索栏位配置建议。

    Args:
        jd_text: JD 原文（纯文本）

    Returns:
        dict: 包含 search_fields、keyword_combinations、talent_profile 的字典。
              调用失败时返回 {{"error": "错误描述"}}。
    """
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    try:
        response = client.messages.create(
            model=config.MODEL,
            max_tokens=2000,
            system=JD_ANALYSIS_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": build_jd_analysis_prompt(jd_text)}
            ],
        )

        raw_text = response.content[0].text

        # Claude 有时会在 JSON 外层包裹 ```json ... ```，做一下清理
        if raw_text.startswith("```"):
            lines = raw_text.split("\n")
            # 去掉首行 ```json 和末行 ```
            lines = [l for l in lines if not l.strip().startswith("```")]
            raw_text = "\n".join(lines)

        result = json.loads(raw_text)
        return result

    except json.JSONDecodeError as e:
        return {
            "error": f"AI 返回的内容无法解析为 JSON：{str(e)}",
            "raw_response": raw_text if "raw_text" in dir() else "",
        }
    except anthropic.APIError as e:
        return {"error": f"Claude API 调用失败：{str(e)}"}
    except Exception as e:
        return {"error": f"分析过程出现异常：{str(e)}"}
