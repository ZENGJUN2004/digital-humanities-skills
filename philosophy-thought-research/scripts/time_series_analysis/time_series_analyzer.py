import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from collections import defaultdict

class TimeSeriesAnalyzer:
    def __init__(self):
        pass
    
    def analyze_concept_evolution(self, concept_data, time_periods, output_path=None, figsize=(14, 8)):
        """分析概念演变趋势"""
        # 准备数据
        concepts = list(concept_data.keys())
        n_concepts = len(concepts)
        n_periods = len(time_periods)
        
        # 创建数据矩阵
        data_matrix = np.zeros((n_concepts, n_periods))
        for i, concept in enumerate(concepts):
            for j, period in enumerate(time_periods):
                if period in concept_data[concept]:
                    data_matrix[i, j] = concept_data[concept][period]
        
        # 分析趋势
        trends = {}
        for i, concept in enumerate(concepts):
            # 计算线性回归斜率
            x = np.arange(n_periods)
            y = data_matrix[i, :]
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            trends[concept] = {
                'slope': slope,
                'r_value': r_value,
                'p_value': p_value,
                'std_err': std_err
            }
        
        # 绘制趋势图
        plt.figure(figsize=figsize)
        
        colors = plt.cm.tab20(np.linspace(0, 1, n_concepts))
        
        for i, (concept, color) in enumerate(zip(concepts, colors)):
            plt.plot(time_periods, data_matrix[i, :], marker='o', linestyle='-', linewidth=2, color=color, label=concept)
            
            # 添加趋势线
            x = np.arange(n_periods)
            y = data_matrix[i, :]
            slope, intercept, _, _, _ = stats.linregress(x, y)
            trend_line = intercept + slope * x
            plt.plot(time_periods, trend_line, linestyle='--', linewidth=1.5, color=color)
        
        plt.title('Concept Evolution Over Time')
        plt.xlabel('Time Period')
        plt.ylabel('Concept Significance')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"概念演变分析已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return trends
    
    def analyze_influence_spread(self, influence_data, time_periods, output_path=None, figsize=(14, 8)):
        """分析影响传播路径"""
        # 准备数据
        influencers = list(influence_data.keys())
        n_influencers = len(influencers)
        n_periods = len(time_periods)
        
        # 创建影响传播矩阵
        spread_matrix = np.zeros((n_influencers, n_periods))
        for i, influencer in enumerate(influencers):
            for j, period in enumerate(time_periods):
                if period in influence_data[influencer]:
                    spread_matrix[i, j] = influence_data[influencer][period]
        
        # 分析传播速度和范围
        spread_analysis = {}
        for i, influencer in enumerate(influencers):
            # 计算传播速度（斜率）
            x = np.arange(n_periods)
            y = spread_matrix[i, :]
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            # 计算传播范围（最大值）
            max_influence = np.max(y)
            
            # 计算传播峰值时间
            peak_time = time_periods[np.argmax(y)] if np.max(y) > 0 else None
            
            spread_analysis[influencer] = {
                'spread_speed': slope,
                'r_value': r_value,
                'p_value': p_value,
                'max_influence': max_influence,
                'peak_time': peak_time
            }
        
        # 绘制影响传播图
        plt.figure(figsize=figsize)
        
        colors = plt.cm.tab20(np.linspace(0, 1, n_influencers))
        
        for i, (influencer, color) in enumerate(zip(influencers, colors)):
            plt.plot(time_periods, spread_matrix[i, :], marker='o', linestyle='-', linewidth=2, color=color, label=influencer)
        
        plt.title('Influence Spread Over Time')
        plt.xlabel('Time Period')
        plt.ylabel('Influence Magnitude')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"影响传播分析已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return spread_analysis
    
    def detect_temporal_patterns(self, time_series_data, period=4, output_path=None, figsize=(14, 8)):
        """检测时间序列模式"""
        # 准备数据
        entities = list(time_series_data.keys())
        time_points = sorted(list(set(point for entity in time_series_data.values() for point in entity.keys())))
        
        # 创建数据矩阵
        n_entities = len(entities)
        n_time_points = len(time_points)
        data_matrix = np.zeros((n_entities, n_time_points))
        
        for i, entity in enumerate(entities):
            for j, time_point in enumerate(time_points):
                if time_point in time_series_data[entity]:
                    data_matrix[i, j] = time_series_data[entity][time_point]
        
        # 检测季节性/周期性模式
        patterns = {}
        for i, entity in enumerate(entities):
            # 计算自相关
            time_series = data_matrix[i, :]
            autocorr = np.correlate(time_series, time_series, mode='full')[len(time_series)-1:]
            autocorr = autocorr / autocorr[0]  # 归一化
            
            # 寻找周期性
            peaks = []
            for k in range(1, len(autocorr)):
                if k > 0 and k < len(autocorr)-1:
                    if autocorr[k] > autocorr[k-1] and autocorr[k] > autocorr[k+1] and autocorr[k] > 0.3:
                        peaks.append((k, autocorr[k]))
            
            patterns[entity] = {
                'autocorr': autocorr.tolist(),
                'peaks': peaks
            }
        
        # 绘制时间序列和自相关图
        plt.figure(figsize=figsize)
        
        # 时间序列图
        plt.subplot(2, 1, 1)
        colors = plt.cm.tab20(np.linspace(0, 1, n_entities))
        for i, (entity, color) in enumerate(zip(entities, colors)):
            plt.plot(time_points, data_matrix[i, :], marker='o', linestyle='-', linewidth=2, color=color, label=entity)
        plt.title('Time Series Data')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        
        # 自相关图
        plt.subplot(2, 1, 2)
        for i, (entity, color) in enumerate(zip(entities, colors)):
            autocorr = patterns[entity]['autocorr']
            lags = np.arange(len(autocorr))
            plt.plot(lags, autocorr, marker='o', linestyle='-', linewidth=1.5, color=color, label=entity)
        plt.title('Autocorrelation')
        plt.xlabel('Lag')
        plt.ylabel('Autocorrelation Coefficient')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"时间序列模式检测已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return patterns
    
    def analyze_philosophical_movements(self, movement_data, time_periods, output_path=None, figsize=(14, 8)):
        """分析哲学思潮的兴起和衰落"""
        # 准备数据
        movements = list(movement_data.keys())
        n_movements = len(movements)
        n_periods = len(time_periods)
        
        # 创建思潮影响力矩阵
        movement_matrix = np.zeros((n_movements, n_periods))
        for i, movement in enumerate(movements):
            for j, period in enumerate(time_periods):
                if period in movement_data[movement]:
                    movement_matrix[i, j] = movement_data[movement][period]
        
        # 分析思潮的生命周期
        movement_analysis = {}
        for i, movement in enumerate(movements):
            # 计算兴起时间（首次达到峰值的30%）
            values = movement_matrix[i, :]
            max_value = np.max(values)
            if max_value > 0:
                threshold = max_value * 0.3
                rise_time = None
                for j in range(n_periods):
                    if values[j] >= threshold:
                        rise_time = time_periods[j]
                        break
                
                # 计算衰落时间（从峰值下降到30%）
                peak_index = np.argmax(values)
                decline_time = None
                for j in range(peak_index, n_periods):
                    if values[j] <= threshold:
                        decline_time = time_periods[j]
                        break
                
                # 计算持续时间
                if rise_time and decline_time:
                    rise_index = time_periods.index(rise_time)
                    decline_index = time_periods.index(decline_time)
                    duration = decline_index - rise_index
                else:
                    duration = None
                
                movement_analysis[movement] = {
                    'rise_time': rise_time,
                    'decline_time': decline_time,
                    'peak_time': time_periods[peak_index],
                    'peak_influence': max_value,
                    'duration': duration
                }
        
        # 绘制思潮演变图
        plt.figure(figsize=figsize)
        
        colors = plt.cm.tab20(np.linspace(0, 1, n_movements))
        
        for i, (movement, color) in enumerate(zip(movements, colors)):
            plt.fill_between(time_periods, movement_matrix[i, :], alpha=0.3, color=color)
            plt.plot(time_periods, movement_matrix[i, :], marker='o', linestyle='-', linewidth=2, color=color, label=movement)
        
        plt.title('Philosophical Movements Over Time')
        plt.xlabel('Time Period')
        plt.ylabel('Movement Influence')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"哲学思潮分析已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return movement_analysis
    
    def generate_temporal_heatmap(self, data, output_path=None, figsize=(14, 10)):
        """生成时间序列热力图"""
        # 准备数据
        entities = list(data.keys())
        time_points = sorted(list(set(point for entity in data.values() for point in entity.keys())))
        
        # 创建数据矩阵
        n_entities = len(entities)
        n_time_points = len(time_points)
        matrix = np.zeros((n_entities, n_time_points))
        
        for i, entity in enumerate(entities):
            for j, time_point in enumerate(time_points):
                if time_point in data[entity]:
                    matrix[i, j] = data[entity][time_point]
        
        # 绘制热力图
        plt.figure(figsize=figsize)
        plt.imshow(matrix, cmap='viridis', aspect='auto', interpolation='nearest')
        
        # 添加颜色条
        plt.colorbar(label='Value')
        
        # 设置标签
        plt.yticks(np.arange(n_entities), entities)
        plt.xticks(np.arange(n_time_points), time_points, rotation=45, ha='right')
        
        plt.title('Temporal Heatmap')
        plt.xlabel('Time')
        plt.ylabel('Entity')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"时间序列热力图已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()

if __name__ == "__main__":
    # 示例使用
    analyzer = TimeSeriesAnalyzer()
    
    # 示例1: 概念演变分析
    concept_data = {
        "存在": {"古希腊": 5, "中世纪": 3, "近代": 4, "现代": 5},
        "知识": {"古希腊": 4, "中世纪": 3, "近代": 5, "现代": 4},
        "价值": {"古希腊": 3, "中世纪": 4, "近代": 4, "现代": 5},
        "理性": {"古希腊": 5, "中世纪": 2, "近代": 5, "现代": 3},
        "自由": {"古希腊": 2, "中世纪": 1, "近代": 5, "现代": 4}
    }
    time_periods = ["古希腊", "中世纪", "近代", "现代"]
    trends = analyzer.analyze_concept_evolution(concept_data, time_periods, output_path="concept_evolution_trend.png")
    print("\n概念演变趋势:")
    for concept, trend in trends.items():
        print(f"{concept}: 斜率 = {trend['slope']:.4f}, R值 = {trend['r_value']:.4f}, p值 = {trend['p_value']:.4f}")
    
    # 示例2: 影响传播分析
    influence_data = {
        "柏拉图": {"古希腊": 5, "中世纪": 4, "近代": 3, "现代": 2},
        "亚里士多德": {"古希腊": 4, "中世纪": 5, "近代": 4, "现代": 3},
        "笛卡尔": {"古希腊": 0, "中世纪": 0, "近代": 5, "现代": 4},
        "康德": {"古希腊": 0, "中世纪": 0, "近代": 4, "现代": 5},
        "尼采": {"古希腊": 0, "中世纪": 0, "近代": 2, "现代": 5}
    }
    spread_analysis = analyzer.analyze_influence_spread(influence_data, time_periods, output_path="influence_spread.png")
    print("\n影响传播分析:")
    for influencer, analysis in spread_analysis.items():
        print(f"{influencer}: 传播速度 = {analysis['spread_speed']:.4f}, 最大影响 = {analysis['max_influence']:.2f}, 峰值时间 = {analysis['peak_time']}")
    
    # 示例3: 时间序列模式检测
    time_series_data = {
        "存在主义": {"1900": 1, "1920": 2, "1940": 4, "1960": 5, "1980": 3, "2000": 2},
        "分析哲学": {"1900": 2, "1920": 3, "1940": 4, "1960": 5, "1980": 4, "2000": 3},
        "现象学": {"1900": 1, "1920": 3, "1940": 4, "1960": 4, "1980": 3, "2000": 2}
    }
    time_points = ["1900", "1920", "1940", "1960", "1980", "2000"]
    patterns = analyzer.detect_temporal_patterns(time_series_data, period=3, output_path="temporal_patterns.png")
    print("\n时间序列模式检测:")
    for entity, pattern in patterns.items():
        print(f"{entity} 的自相关峰值: {pattern['peaks']}")
    
    # 示例4: 哲学思潮分析
    movement_data = {
        "理性主义": {"1600": 2, "1650": 4, "1700": 5, "1750": 3, "1800": 2},
        "经验主义": {"1600": 1, "1650": 3, "1700": 4, "1750": 5, "1800": 3},
        "浪漫主义": {"1600": 0, "1650": 0, "1700": 1, "1750": 3, "1800": 5},
        "实证主义": {"1600": 0, "1650": 0, "1700": 0, "1750": 1, "1800": 3}
    }
    movement_periods = ["1600", "1650", "1700", "1750", "1800"]
    movement_analysis = analyzer.analyze_philosophical_movements(movement_data, movement_periods, output_path="philosophical_movements.png")
    print("\n哲学思潮分析:")
    for movement, analysis in movement_analysis.items():
        print(f"{movement}: 兴起时间 = {analysis['rise_time']}, 衰落时间 = {analysis['decline_time']}, 峰值时间 = {analysis['peak_time']}, 峰值影响 = {analysis['peak_influence']:.2f}")
    
    # 示例5: 生成时间序列热力图
    heatmap_data = {
        "柏拉图": {"古希腊": 5, "中世纪": 4, "近代": 3, "现代": 2},
        "亚里士多德": {"古希腊": 4, "中世纪": 5, "近代": 4, "现代": 3},
        "笛卡尔": {"古希腊": 0, "中世纪": 0, "近代": 5, "现代": 4},
        "康德": {"古希腊": 0, "中世纪": 0, "近代": 4, "现代": 5},
        "尼采": {"古希腊": 0, "中世纪": 0, "近代": 2, "现代": 5}
    }
    analyzer.generate_temporal_heatmap(heatmap_data, output_path="temporal_heatmap.png")