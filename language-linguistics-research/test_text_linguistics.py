#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试文本语言学分析模块
"""

from scripts.text_linguistics_analysis import TextLinguisticsAnalysis

# 读取示例文本
with open('assets/sample_english_text.txt', 'r', encoding='utf-8') as f:
    english_text = f.read()

with open('assets/sample_chinese_text.txt', 'r', encoding='utf-8') as f:
    chinese_text = f.read()

# 初始化分析器实例
english_analyzer = TextLinguisticsAnalysis(english_text, "english")
chinese_analyzer = TextLinguisticsAnalysis(chinese_text, "chinese")

print("=== 文本语言学分析测试 ===")
print()

# 1. 测试英文文本特征分析
print("1. 英文文本特征分析")
print("-" * 50)
english_features = english_analyzer.analyze_text_features()
print(f"词数: {english_features['word_count']}")
print(f"句子数: {english_features['sentence_count']}")
print(f"词汇多样性: {english_features['lexical_diversity']:.2f}")
print(f"平均句长: {english_features['avg_sentence_length']:.2f}")
print(f"可读性指数:")
for key, value in english_features['readability'].items():
    print(f"  {key}: {value:.2f}")
print()

# 2. 测试英文文本风格分析
print("2. 英文文本风格分析")
print("-" * 50)
english_style = english_analyzer.analyze_style()
print(f"正式性: {english_style['formality']:.2f}")
print(f"复杂性: {english_style['complexity']:.2f}")
print(f"情感极性: {english_style['sentiment']['polarity']:.2f}")
print(f"主观性: {english_style['sentiment']['subjectivity']:.2f}")
print()

# 3. 测试英文文本类型识别
print("3. 英文文本类型识别")
print("-" * 50)
english_type = english_analyzer.identify_text_type()
print(f"语言: {english_type['language']}")
print(f"体裁: {english_type['genre']}")
print(f"语域: {english_type['register']}")
print()

# 4. 测试中文文本特征分析
print("4. 中文文本特征分析")
print("-" * 50)
chinese_features = chinese_analyzer.analyze_text_features()
print(f"词数: {chinese_features['word_count']}")
print(f"句子数: {chinese_features['sentence_count']}")
print(f"词汇多样性: {chinese_features['lexical_diversity']:.2f}")
print(f"平均句长: {chinese_features['avg_sentence_length']:.2f}")
print()

# 5. 测试中文文本风格分析
print("5. 中文文本风格分析")
print("-" * 50)
chinese_style = chinese_analyzer.analyze_style()
print(f"正式性: {chinese_style['formality']:.2f}")
print(f"复杂性: {chinese_style['complexity']:.2f}")
print(f"情感极性: {chinese_style['sentiment']['polarity']:.2f}")
print(f"主观性: {chinese_style['sentiment']['subjectivity']:.2f}")
print()

# 6. 测试中文文本类型识别
print("6. 中文文本类型识别")
print("-" * 50)
chinese_type = chinese_analyzer.identify_text_type()
print(f"语言: {chinese_type['language']}")
print(f"体裁: {chinese_type['genre']}")
print(f"语域: {chinese_type['register']}")
print()

print("=== 测试完成 ===")
