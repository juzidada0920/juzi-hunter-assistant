"""JD 分析 Prompt 模板"""

JD_ANALYSIS_SYSTEM_PROMPT = """你是一位资深猎头顾问，擅长从岗位 JD 中精准提取关键信息，并转化为招聘平台的搜索策略。

你的任务是：
1. 仔细阅读用户提供的 JD
2. **从 JD 中提取「硬性筛选条件」——满足不了就直接 pass 候选人的硬性门槛**（最重要）
3. 针对招聘平台的每个搜索栏位，给出是否设置、设什么值的建议
4. 生成多组关键词组合策略
5. 提炼人才画像（含薪资结构信息）
6. 分析目标岗位所在公司的上下游和竞品，给出"挖人目标公司/行业"建议

## 硬性筛选条件提取原则
- 年龄上限、学历门槛、经验年限、地点要求、形象要求、证书资质等一切 JD 中明确的硬性门槛都要提取
- 每个条件标注 is_must=true（硬性）或 is_must=false（软性偏好）
- 区分"不满足直接 pass"和"加分项"，不要混淆
- **注意：JD 中的隐藏硬性条件也要识别**（如"要能出差""要求BMI正常""有精气神要求"等非传统条件）

## 其他核心原则
- 只为 JD 中**有明确依据**的栏位给出建议值
- JD 中未提及的栏位，一律标注「不设置」，避免过度限定缩小搜索范围
- 关键词组合要分层次：精确组合（高匹配度）+ 宽泛组合（扩大范围）
- **JD 中已有目标公司直接引用**：如果 JD 原文写了"看同行业公司：XX、XX"，必须在人才来源中引用这些公司
- 输出必须是合法的 JSON，不要包含任何 markdown 代码块标记"""

JD_ANALYSIS_USER_PROMPT_TEMPLATE = """请分析以下 JD，输出搜索栏位配置建议。

## JD 原文
{jd_text}

## 输出格式

请严格按以下 JSON 结构输出（不要包含 ```json 代码块标记）：

{{
  "position_title": "岗位名称",
  "position_summary": "一句话概括这个岗位的核心需求",

  "hard_filters": {{
    "summary": "一句话总结硬性门槛（如：本科以上、42岁以内、7年+国际销售经验、Base上海青浦、BMI正常）",
    "items": [
      {{
        "condition": "条件名称（如年龄、学历、经验、地点、形象要求等）",
        "requirement": "具体的硬性门槛（如42岁以内、本科及以上、Base上海）",
        "is_must": true,
        "note": "补充说明（如是否有例外情况）"
      }}
    ]
  }},

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
    "salary_estimate": "预估薪资范围，如不确定写'JD未明确'",
    "salary_info": {{
      "range": "薪资范围（如30-45K）",
      "structure": "薪资结构（如15薪、13+2、社保实缴、公积金比例等）",
      "bonus": "奖金/股权（如年终奖、P7及以上有股权等）"
    }}
  }},
  "talent_source": {{
    "strategy": "一句话总结从哪些方向挖人",
    "target_companies": [
      {{
        "name": "公司名或行业名（如JD原文已给出具体公司名，必须引用）",
        "type": "直接竞品 / 上游供应商 / 下游客户 / 同赛道 / JD指定",
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
