"""JD 分析 Prompt 模板"""

JD_ANALYSIS_SYSTEM_PROMPT = """你是一位资深猎头顾问，擅长从岗位 JD 中精准提取关键信息，并转化为招聘平台的搜索策略。

你的任务是：
1. 仔细阅读用户提供的 JD
2. 针对招聘平台的每个搜索栏位，给出是否设置、设什么值的建议
3. 生成多组关键词组合策略
4. 提炼人才画像
5. 分析目标岗位所在公司的上下游和竞品，给出"挖人目标公司/行业"建议

## 核心原则
- 只为 JD 中**有明确依据**的栏位给出建议值
- JD 中未提及的栏位，一律标注「不设置」，避免过度限定缩小搜索范围
- 关键词组合要分层次：精确组合（高匹配度）+ 宽泛组合（扩大范围）
- **人才来源分析**：基于 JD 的业务领域和技术栈，推理目标公司可能属于什么赛道，这个赛道的直接竞品有哪些、上游供应商有哪些、下游客户有哪些，从这些公司挖人命中率高
- 输出必须是合法的 JSON，不要包含任何 markdown 代码块标记"""

JD_ANALYSIS_USER_PROMPT_TEMPLATE = """请分析以下 JD，输出搜索栏位配置建议。

## JD 原文
{jd_text}

## 输出格式

请严格按以下 JSON 结构输出（不要包含 ```json 代码块标记）：

{{
  "position_title": "岗位名称",
  "position_summary": "一句话概括这个岗位的核心需求",
  "search_fields": [
    {{
      "field": "搜索关键词",
      "enabled": true,
      "value": "核心技术词 + 业务领域词 的组合",
      "reason": "基于JD的哪些要求得出这个关键词"
    }},
    {{
      "field": "职能",
      "enabled": true,
      "value": "具体职能方向",
      "reason": "JD中明确的职能描述"
    }},
    {{
      "field": "工作地点",
      "enabled": true,
      "value": "城市名称",
      "reason": "JD中写明的Base地点"
    }},
    {{
      "field": "薪资范围",
      "enabled": false,
      "value": "",
      "reason": "JD未明确薪资范围，建议不限"
    }},
    {{
      "field": "学历要求",
      "enabled": true,
      "value": "本科及以上 或 硕士及以上 等",
      "reason": "JD中的学历要求"
    }},
    {{
      "field": "工作经验",
      "enabled": true,
      "value": "X-Y年",
      "reason": "JD中的经验年限要求"
    }},
    {{
      "field": "职位类别",
      "enabled": true,
      "value": "职位大类",
      "reason": "基于JD判断的职位分类"
    }},
    {{
      "field": "行业领域",
      "enabled": true,
      "value": "目标行业",
      "reason": "JD中隐含或明确的行业方向"
    }},
    {{
      "field": "目标公司",
      "enabled": true,
      "value": "建议挖人的公司类型或具体公司名",
      "reason": "基于JD的业务赛道，从直接竞品、上游供应商、下游客户中寻找候选人"
    }},
    {{
      "field": "公司规模",
      "enabled": false,
      "value": "",
      "reason": "JD一般不限定公司规模，建议不限"
    }},
    {{
      "field": "融资阶段",
      "enabled": false,
      "value": "",
      "reason": "JD一般不限定融资阶段，建议不限"
    }},
    {{
      "field": "候选人活跃度",
      "enabled": true,
      "value": "3日内登录过 或 15日内登录过",
      "reason": "建议设近期活跃，提高联系成功率"
    }}
  ],
  "keyword_combinations": [
    "组合1: 核心词 + 业务词",
    "组合2: 同义词替换",
    "组合3: 宽泛搜索组合"
  ],
  "talent_profile": {{
    "education": "学历要求",
    "experience_years": "经验年限",
    "must_have_skills": ["必备技能1", "必备技能2"],
    "nice_to_have_skills": ["加分技能1", "加分技能2"],
    "industry_background": "期望的行业背景",
    "salary_estimate": "预估薪资范围，如不确定写'JD未明确'"
  }},
  "talent_source": {{
    "strategy": "一句话总结从哪些方向挖人（如：优先从XX赛道的直接竞品和上游供应商挖人，重点关注有XX业务经验的人选）",
    "target_companies": [
      {{
        "name": "公司A（或行业X）",
        "type": "直接竞品 / 上游供应商 / 下游客户 / 同赛道",
        "reason": "为什么从这里挖人命中率高"
      }}
    ]
  }}
}}

请直接输出 JSON，不要加任何解释性文字。"""


def build_jd_analysis_messages(jd_text: str) -> list[dict]:
    """构建 JD 分析的 messages（OpenAI 兼容格式）"""
    return [
        {"role": "system", "content": JD_ANALYSIS_SYSTEM_PROMPT},
        {"role": "user", "content": JD_ANALYSIS_USER_PROMPT_TEMPLATE.format(jd_text=jd_text)},
    ]
