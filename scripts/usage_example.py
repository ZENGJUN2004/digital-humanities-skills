#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数字人文技能库使用示例

这个脚本展示了如何使用数字人文技能库的各种功能
"""

from digital_humanities import DigitalHumanities
import json

# 初始化数字人文技能库
dh = DigitalHumanities()

print("=" * 80)
print("数字人文技能库使用示例")
print("=" * 80)

# 示例1: 文本分析
print("\n1. 文本分析示例")
print("-" * 40)

text_request = {
    "description": "分析这段关于数字人文的文本",
    "text": "数字人文是一个充满活力的跨学科领域，它结合了传统人文学科与数字技术，为我们理解人类文化提供了新的视角。随着技术的不断进步，数字人文逐渐发展成为一个独立的研究领域，涵盖了文本分析、数字档案、虚拟重建等多个方向。"
}

text_result = dh.process_request(text_request)
print("文本分析结果:")
print(json.dumps(text_result["results"]["text_analysis"]["results"], ensure_ascii=False, indent=2))

# 示例2: 历史研究
print("\n2. 历史研究示例")
print("-" * 40)

historical_request = {
    "description": "处理历史数据",
    "historical_data": [
        {"event": "五四运动", "year": 1919, "location": "北京"},
        {"event": "新文化运动", "year": 1915, "location": "上海"},
        {"event": "辛亥革命", "year": 1911, "location": "武汉"}
    ]
}

historical_result = dh.process_request(historical_request)
print("历史研究结果:")
print(json.dumps(historical_result["results"]["historical_research"], ensure_ascii=False, indent=2))

# 示例3: 文化遗产
print("\n3. 文化遗产示例")
print("-" * 40)

heritage_request = {
    "description": "处理文化遗产数据",
    "heritage_data": {
        "name": "故宫博物院",
        "location": "北京",
        "year_built": 1420,
        "category": "古建筑"
    }
}

heritage_result = dh.process_request(heritage_request)
print("文化遗产处理结果:")
print(json.dumps(heritage_result["results"]["cultural_heritage"], ensure_ascii=False, indent=2))

# 示例4: 社会文化分析
print("\n4. 社会文化分析示例")
print("-" * 40)

social_request = {
    "description": "分析社会文化数据",
    "social_data": {
        "topic": "数字化生活",
        "sentiment": "positive",
        "trend": "increasing"
    }
}

social_result = dh.process_request(social_request)
print("社会文化分析结果:")
print(json.dumps(social_result["results"]["social_cultural_analysis"], ensure_ascii=False, indent=2))

# 示例5: 列出所有技能
print("\n5. 可用技能领域")
print("-" * 40)

skills = dh.list_skills()
for skill in skills:
    skill_info = dh.get_skill_info(skill)
    print(f"- {skill_info['name']}: {skill_info['description']}")

print("\n" + "=" * 80)
print("使用示例完成")
print("=" * 80)
