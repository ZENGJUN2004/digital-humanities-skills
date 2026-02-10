#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文化数据分析示例
演示文化数据分析模块的使用
"""

from scripts.cultural_data_analysis.cultural_analyzer import CulturalAnalyzer
import pandas as pd
import os

# 示例数据路径
data_path = "assets/sample_cultural_data/art_exhibition_visitors.csv"

# 检查数据文件是否存在
if not os.path.exists(data_path):
    print(f"警告: 示例数据文件不存在: {data_path}")
    print("请确保数据文件路径正确")
    exit(1)

try:
    # 加载数据
    print("加载文化数据...")
    data = pd.read_csv(data_path)
    print(f"数据加载完成，形状: {data.shape}")
    print(f"列名: {list(data.columns)}")
    
    # 初始化文化数据分析器
    print("\n初始化文化数据分析器...")
    analyzer = CulturalAnalyzer(data)
    
    # 描述性统计分析
    print("\n=== 描述性统计分析 ===")
    stats = analyzer.descriptive_statistics()
    
    if "error" in stats:
        print(f"分析错误: {stats['error']}")
    else:
        # 显示基本统计
        print(f"\n1. 数据基本信息:")
        print(f"   行数: {stats['shape']['rows']}")
        print(f"   列数: {stats['shape']['columns']}")
        
        # 显示数值型列统计
        print("\n2. 数值型列统计:")
        numeric_cols = list(stats['numeric_stats'].keys())
        for col in numeric_cols:
            if col in ['visitors', 'ticket_price', 'rating', 'artist_count', 'artwork_count', 'venue_size']:
                col_stats = stats['numeric_stats'][col]
                print(f"   {col}:")
                print(f"      均值: {col_stats['mean']:.2f}")
                print(f"      标准差: {col_stats['std']:.2f}")
                print(f"      最小值: {col_stats['min']:.2f}")
                print(f"      最大值: {col_stats['max']:.2f}")
        
        # 显示分类列统计
        print("\n3. 分类列统计:")
        categorical_cols = list(stats['categorical_stats'].keys())
        for col in categorical_cols:
            col_stats = stats['categorical_stats'][col]
            print(f"   {col}:")
            print(f"      唯一值数量: {col_stats['unique_values']}")
            print(f"      最常见值: {col_stats['top_value']}")
            print(f"      最常见值计数: {col_stats['top_value_count']}")
        
        # 显示缺失值
        print("\n4. 缺失值统计:")
        missing = stats['missing_values']
        has_missing = any(count > 0 for count in missing.values())
        if has_missing:
            for col, count in missing.items():
                if count > 0:
                    print(f"   {col}: {count} 个缺失值")
        else:
            print("   无缺失值")
    
    # 相关性分析
    print("\n=== 相关性分析 ===")
    correlation = analyzer.correlation_analysis()
    
    if "error" in correlation:
        print(f"分析错误: {correlation['error']}")
    else:
        # 显示皮尔逊相关系数
        print("\n1. 皮尔逊相关系数:")
        pearson_corr = correlation['pearson_correlation']
        # 显示参观者与其他变量的相关性
        if 'visitors' in pearson_corr:
            print("   参观者与其他变量的相关性:")
            for var, corr in pearson_corr['visitors'].items():
                if var != 'visitors':
                    print(f"      {var}: {corr:.3f}")
    
    # 聚类分析
    print("\n=== 聚类分析 ===")
    clustering = analyzer.cluster_analysis(n_clusters=3)
    
    if "error" in clustering:
        print(f"分析错误: {clustering['error']}")
    else:
        print(f"\n1. 聚类结果:")
        print(f"   聚类数量: {len(clustering['cluster_sizes'])}")
        print(f"   各聚类大小: {clustering['cluster_sizes']}")
        print(f"   聚类中心维度: {len(clustering['cluster_centers'][0])}")
        print(f"   参与聚类的列: {clustering['columns']}")
    
    # 时间序列分析
    print("\n=== 时间序列分析 ===")
    time_analysis = analyzer.time_series_analysis('start_date', 'visitors')
    
    if "error" in time_analysis:
        print(f"分析错误: {time_analysis['error']}")
    else:
        print(f"\n1. 时间序列基本信息:")
        print(f"   开始日期: {time_analysis['start_date']}")
        print(f"   结束日期: {time_analysis['end_date']}")
        print(f"   平均参观人数: {time_analysis['mean_value']:.2f}")
        print(f"   参观人数标准差: {time_analysis['std_value']:.2f}")
        print(f"   最高参观人数: {time_analysis['max_value']:.2f}")
        print(f"   最低参观人数: {time_analysis['min_value']:.2f}")
        print(f"   参观人数趋势: {time_analysis['trend']:.3f}")
        if time_analysis['trend'] > 0:
            print("   趋势分析: 参观人数呈上升趋势")
        elif time_analysis['trend'] < 0:
            print("   趋势分析: 参观人数呈下降趋势")
        else:
            print("   趋势分析: 参观人数保持稳定")
    
    # 情感分析（模拟）
    print("\n=== 情感分析 ===")
    # 为了演示，我们创建一个简单的展览评价列
    # 实际应用中，这里应该是真实的文本数据
    data['exhibition_review'] = [
        "这个展览非常精彩，展品丰富，布置精美",
        "现代艺术展很有创意，让人深思",
        "印象派画作太美了，非常喜欢",
        "当代艺术有点难以理解，但很有挑战性",
        "传统书画展很有文化底蕴",
        "巴洛克艺术展华丽壮观",
        "数字艺术展很有趣，互动性强",
        "摄影展很有冲击力",
        "雕塑展很有质感",
        "版画展很精致",
        "浮世绘展很有东方韵味",
        "非洲艺术展很有原始力量",
        "拉丁美洲艺术展色彩丰富",
        "伊斯兰艺术展很神秘",
        "东亚艺术展很有特色"
    ]
    
    # 重新初始化分析器以包含新列
    analyzer = CulturalAnalyzer(data)
    sentiment = analyzer.sentiment_analysis('exhibition_review')
    
    if "error" in sentiment:
        print(f"分析错误: {sentiment['error']}")
    else:
        print(f"\n1. 情感分析结果:")
        print(f"   情感分布: {sentiment['sentiment_counts']}")
        print(f"   平均正面词数: {sentiment['average_positive_words']:.2f}")
        print(f"   平均负面词数: {sentiment['average_negative_words']:.2f}")
    
    # 数据可视化（仅显示代码示例）
    print("\n=== 数据可视化示例 ===")
    print("\n1. 参观人数分布直方图:")
    print("   fig = analyzer.visualize('histogram', x_col='visitors', title='参观人数分布')")
    print("   fig.show()")
    
    print("\n2. 参观人数与票价散点图:")
    print("   fig = analyzer.visualize('scatter', x_col='ticket_price', y_col='visitors', title='参观人数与票价关系')")
    print("   fig.show()")
    
    print("\n3. 展览类型分布饼图:")
    print("   fig = analyzer.visualize('pie', x_col='exhibition_type', title='展览类型分布')")
    print("   fig.show()")
    
    print("\n4. 参观人数与场地大小关系热力图:")
    print("   fig = analyzer.visualize('heatmap', x_col='venue_size', y_col='visitors', title='参观人数与场地大小关系')")
    print("   fig.show()")
    
    # 导出分析结果
    print("\n=== 导出分析结果 ===")
    analysis_results = {
        "descriptive_statistics": stats,
        "correlation_analysis": correlation,
        "cluster_analysis": clustering,
        "time_series_analysis": time_analysis,
        "sentiment_analysis": sentiment
    }
    
    output_path = "cultural_analysis_results.json"
    success = analyzer.export_analysis(analysis_results, output_path)
    if success:
        print(f"分析结果已导出到: {output_path}")
    else:
        print("导出分析结果失败")
    
    print("\n=== 分析完成 ===")
    
except Exception as e:
    print(f"运行时错误: {e}")
    print("请确保已安装所有依赖项并提供有效的数据路径")

print("\n=== 使用说明 ===")
print("1. 确保已安装以下依赖项:")
print("   - numpy")
print("   - pandas")
print("   - scikit-learn")
print("   - networkx")
print("   - plotly")
print("   - matplotlib")
print("   - scipy")
print("2. 运行脚本查看分析结果")
print("3. 可以修改数据路径使用自己的文化数据")
