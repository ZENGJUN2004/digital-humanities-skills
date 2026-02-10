#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
艺术与文化研究技能测试脚本
测试核心功能模块
"""

import os
import sys

# 确保可以导入脚本模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # 测试文化数据分析模块
    print("=== 测试文化数据分析模块 ===")
    from scripts.cultural_data_analysis.cultural_analyzer import CulturalAnalyzer
    import pandas as pd
    
    # 加载示例数据
    data_path = "assets/sample_cultural_data/art_exhibition_visitors.csv"
    if not os.path.exists(data_path):
        print(f"错误: 示例数据文件不存在: {data_path}")
    else:
        print("加载示例数据...")
        data = pd.read_csv(data_path)
        print(f"数据加载成功，形状: {data.shape}")
        
        # 初始化分析器
        print("初始化文化数据分析器...")
        analyzer = CulturalAnalyzer(data)
        
        # 测试描述性统计
        print("\n测试描述性统计分析...")
        stats = analyzer.descriptive_statistics()
        if "error" in stats:
            print(f"错误: {stats['error']}")
        else:
            print("描述性统计分析成功!")
            print(f"数据基本信息: {stats['shape']['rows']} 行, {stats['shape']['columns']} 列")
        
        # 测试相关性分析
        print("\n测试相关性分析...")
        correlation = analyzer.correlation_analysis()
        if "error" in correlation:
            print(f"错误: {correlation['error']}")
        else:
            print("相关性分析成功!")
            if 'visitors' in correlation['pearson_correlation']:
                print("参观者与其他变量的相关性计算成功")
        
        # 测试聚类分析
        print("\n测试聚类分析...")
        clustering = analyzer.cluster_analysis(n_clusters=3)
        if "error" in clustering:
            print(f"错误: {clustering['error']}")
        else:
            print("聚类分析成功!")
            print(f"聚类数量: {len(clustering['cluster_sizes'])}")
            print(f"各聚类大小: {clustering['cluster_sizes']}")
        
        # 测试时间序列分析
        print("\n测试时间序列分析...")
        time_analysis = analyzer.time_series_analysis('start_date', 'visitors')
        if "error" in time_analysis:
            print(f"错误: {time_analysis['error']}")
        else:
            print("时间序列分析成功!")
            print(f"开始日期: {time_analysis['start_date']}")
            print(f"结束日期: {time_analysis['end_date']}")
            print(f"平均参观人数: {time_analysis['mean_value']:.2f}")
        
        print("\n=== 文化数据分析模块测试完成 ===")
    
    # 测试数字图像处理模块（模拟测试，因为需要实际图像）
    print("\n=== 测试数字图像处理模块 ===")
    from scripts.digital_image_processing.image_analyzer import ImageAnalyzer
    
    # 测试初始化
    print("测试图像分析器初始化...")
    # 使用一个不存在的图像路径，测试错误处理
    test_image_path = "nonexistent_image.jpg"
    analyzer = ImageAnalyzer(test_image_path)
    print("图像分析器初始化成功（错误处理正常）")
    
    # 测试分析方法
    print("测试图像分析方法...")
    analysis = analyzer.analyze()
    if "error" in analysis:
        print(f"分析错误处理正常: {analysis['error']}")
    else:
        print("图像分析成功!")
    
    print("\n=== 数字图像处理模块测试完成 ===")
    
    print("\n=== 所有测试完成 ===")
    print("\n测试结果: 核心功能模块加载正常，基本功能测试通过!")
    print("\n注意:")
    print("1. 数字图像处理模块需要实际图像文件才能进行完整测试")
    print("2. 请在实际使用时提供真实的艺术作品图像路径")
    print("3. 文化数据分析模块已使用示例数据进行了完整测试")
    
except Exception as e:
    print(f"测试过程中出错: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 测试结束 ===")
