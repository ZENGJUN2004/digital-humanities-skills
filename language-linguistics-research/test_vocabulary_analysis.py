#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试词汇分析模块
"""

from scripts.vocabulary_analysis import VocabularyAnalysis

# 测试词汇列表
test_words = ['running', 'unhappiness', 'better', 'quickly', 'linguistics', 'language', 'study', 'analysis', 'computer', 'natural']

# 初始化分析器
analyzer = VocabularyAnalysis(test_words, "english")

print("=== 词汇分析测试 ===")
print()

# 1. 测试词汇形态分析
print("1. 词汇形态分析")
print("-" * 50)
morphology_analysis = analyzer.analyze_morphology()
for word, analysis in morphology_analysis.items():
    print(f"{word}:")
    print(f"  词根: {analysis['root']}")
    print(f"  词缀: {analysis['affixes']}")
    print(f"  词性: {analysis['part_of_speech']}")
    print(f"  屈折变化: {analysis['inflections']}")
    print()

# 2. 测试词汇语义分析
print("2. 词汇语义分析")
print("-" * 50)
semantics_analysis = analyzer.analyze_semantics()
for word, analysis in semantics_analysis.items():
    print(f"{word}:")
    print(f"  语义类别: {analysis['semantic_category']}")
    print(f"  同义词: {analysis['synonyms'][:3]}")  # 显示前3个
    print(f"  反义词: {analysis['antonyms'][:3]}")  # 显示前3个
    print(f"  下位词: {analysis['hyponyms'][:3]}")  # 显示前3个
    print(f"  上位词: {analysis['hypernyms'][:3]}")  # 显示前3个
    print()

# 3. 测试词汇集合特征分析
print("3. 词汇集合特征分析")
print("-" * 50)
vocab_features = analyzer.analyze_vocabulary_features()
print(f"总词汇数: {vocab_features['total_words']}")
print(f"唯一词汇数: {vocab_features['unique_words']}")
print(f"平均词长: {vocab_features['avg_word_length']:.2f}")
print(f"词长分布: {vocab_features['length_distribution']}")
print(f"词性分布: {vocab_features['pos_distribution']}")
print(f"前缀分布: {vocab_features['prefix_distribution']}")
print(f"后缀分布: {vocab_features['suffix_distribution']}")
print()

print("=== 测试完成 ===")
