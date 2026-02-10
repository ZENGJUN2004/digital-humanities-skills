#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
影响网络分析模块测试脚本
"""

import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.influence_network_analysis.influence_network_analyzer import InfluenceNetworkAnalyzer

print("测试影响网络分析模块...")

try:
    # 初始化影响网络分析器
    analyzer = InfluenceNetworkAnalyzer()
    print("初始化成功")
    
    # 构建影响网络
    influencers = {
        "柏拉图": {"era": "古希腊", "school": "柏拉图主义"},
        "亚里士多德": {"era": "古希腊", "school": "亚里士多德主义"},
        "笛卡尔": {"era": "近代", "school": "理性主义"}
    }
    
    relationships = [
        ("柏拉图", "亚里士多德", 0.9, "teacher"),
        ("亚里士多德", "笛卡尔", 0.6, "influence")
    ]
    
    analyzer.build_influence_network(influencers, relationships)
    print("构建网络成功")
    
    # 分析网络属性
    print("测试网络属性分析...")
    properties = analyzer.analyze_network_properties()
    print(f"网络属性: 节点数={properties['nodes']}, 边数={properties['edges']}")
    
    # 识别关键影响者
    print("测试关键影响者识别...")
    key_influencers = analyzer.identify_key_influencers()
    print("关键影响者识别成功")
    print("\n关键影响者:")
    for influencer, score in key_influencers['key_influencers']:
        print(f"  {influencer}: {score:.4f}")
    
    # 测试影响路径分析
    print("测试影响路径分析...")
    paths = analyzer.analyze_influence_paths("柏拉图", "笛卡尔")
    print("影响路径分析成功")
    print("\n影响路径 (柏拉图 -> 笛卡尔):")
    for path, weight in paths:
        print(f"路径: {' -> '.join(path)}, 权重: {weight:.4f}")
    
    # 测试影响社区分析
    print("测试影响社区分析...")
    communities = analyzer.analyze_influence_communities()
    print("影响社区分析成功")
    print(f"\n社区识别: 找到 {len(communities)} 个社区")
    
    print("\n影响网络分析模块测试成功!")
except Exception as e:
    print(f"影响网络分析模块测试失败: {e}")
    import traceback
    traceback.print_exc()
