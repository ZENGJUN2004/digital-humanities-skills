import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from scipy import stats

class ConceptApplicationAnalyzer:
    def __init__(self):
        pass
    
    def analyze_concept_applications(self, application_data, output_path=None, figsize=(14, 10)):
        """分析概念在不同领域的应用"""
        # 准备数据
        concepts = list(application_data.keys())
        domains = list(set(domain for concept in application_data.values() for domain in concept.keys()))
        
        # 创建概念-领域矩阵
        n_concepts = len(concepts)
        n_domains = len(domains)
        matrix = np.zeros((n_concepts, n_domains))
        
        for i, concept in enumerate(concepts):
            for j, domain in enumerate(domains):
                if domain in application_data[concept]:
                    matrix[i, j] = application_data[concept][domain]
        
        # 分析概念在不同领域的应用强度
        application_analysis = {}
        for i, concept in enumerate(concepts):
            values = matrix[i, :]
            mean_application = np.mean(values)
            std_application = np.std(values)
            max_application = np.max(values)
            dominant_domain = domains[np.argmax(values)] if max_application > 0 else None
            
            application_analysis[concept] = {
                'mean_application': mean_application,
                'std_application': std_application,
                'max_application': max_application,
                'dominant_domain': dominant_domain,
                'values': values.tolist()
            }
        
        # 绘制热力图
        plt.figure(figsize=figsize)
        sns.heatmap(matrix, annot=True, cmap='viridis', xticklabels=domains, yticklabels=concepts, cbar_kws={'label': 'Application Strength'})
        plt.title('Concept Applications Across Domains')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"概念应用分析已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return application_analysis
    
    def analyze_application_trends(self, trend_data, output_path=None, figsize=(14, 8)):
        """分析概念应用的变化趋势"""
        # 准备数据
        concepts = list(trend_data.keys())
        time_periods = sorted(list(set(period for concept in trend_data.values() for period in concept.keys())))
        
        # 创建概念-时间矩阵
        n_concepts = len(concepts)
        n_periods = len(time_periods)
        matrix = np.zeros((n_concepts, n_periods))
        
        for i, concept in enumerate(concepts):
            for j, period in enumerate(time_periods):
                if period in trend_data[concept]:
                    matrix[i, j] = trend_data[concept][period]
        
        # 分析趋势
        trends = {}
        for i, concept in enumerate(concepts):
            # 计算线性回归斜率
            x = np.arange(n_periods)
            y = matrix[i, :]
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            trends[concept] = {
                'slope': slope,
                'r_value': r_value,
                'p_value': p_value,
                'std_err': std_err,
                'trend_direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable'
            }
        
        # 绘制趋势图
        plt.figure(figsize=figsize)
        
        colors = plt.cm.tab20(np.linspace(0, 1, n_concepts))
        
        for i, (concept, color) in enumerate(zip(concepts, colors)):
            plt.plot(time_periods, matrix[i, :], marker='o', linestyle='-', linewidth=2, color=color, label=concept)
            
            # 添加趋势线
            x = np.arange(n_periods)
            y = matrix[i, :]
            slope, intercept, _, _, _ = stats.linregress(x, y)
            trend_line = intercept + slope * x
            plt.plot(time_periods, trend_line, linestyle='--', linewidth=1.5, color=color)
        
        plt.title('Concept Application Trends Over Time')
        plt.xlabel('Time Period')
        plt.ylabel('Application Strength')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"概念应用趋势分析已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return trends
    
    def analyze_application_similarities(self, application_data, output_path=None, figsize=(12, 10)):
        """分析不同概念应用模式的相似性"""
        # 准备数据
        concepts = list(application_data.keys())
        domains = list(set(domain for concept in application_data.values() for domain in concept.keys()))
        
        # 创建概念-领域矩阵
        n_concepts = len(concepts)
        n_domains = len(domains)
        matrix = np.zeros((n_concepts, n_domains))
        
        for i, concept in enumerate(concepts):
            for j, domain in enumerate(domains):
                if domain in application_data[concept]:
                    matrix[i, j] = application_data[concept][domain]
        
        # 计算概念之间的相似度
        similarity_matrix = np.zeros((n_concepts, n_concepts))
        for i in range(n_concepts):
            for j in range(n_concepts):
                if i != j:
                    # 计算皮尔逊相关系数
                    correlation, _ = stats.pearsonr(matrix[i, :], matrix[j, :])
                    similarity_matrix[i, j] = correlation
                else:
                    similarity_matrix[i, j] = 1.0
        
        # 绘制相似度热力图
        plt.figure(figsize=figsize)
        sns.heatmap(similarity_matrix, annot=True, cmap='coolwarm', xticklabels=concepts, yticklabels=concepts, vmin=-1, vmax=1)
        plt.title('Concept Application Similarities')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"概念应用相似性分析已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return similarity_matrix
    
    def evaluate_application_effectiveness(self, effectiveness_data, output_path=None, figsize=(14, 8)):
        """评估概念应用的效果"""
        # 准备数据
        concepts = list(effectiveness_data.keys())
        metrics = list(set(metric for concept in effectiveness_data.values() for metric in concept.keys()))
        
        # 创建概念-指标矩阵
        n_concepts = len(concepts)
        n_metrics = len(metrics)
        matrix = np.zeros((n_concepts, n_metrics))
        
        for i, concept in enumerate(concepts):
            for j, metric in enumerate(metrics):
                if metric in effectiveness_data[concept]:
                    matrix[i, j] = effectiveness_data[concept][metric]
        
        # 评估概念应用效果
        effectiveness_analysis = {}
        for i, concept in enumerate(concepts):
            values = matrix[i, :]
            mean_effectiveness = np.mean(values)
            std_effectiveness = np.std(values)
            overall_effectiveness = np.sum(values)
            
            effectiveness_analysis[concept] = {
                'mean_effectiveness': mean_effectiveness,
                'std_effectiveness': std_effectiveness,
                'overall_effectiveness': overall_effectiveness,
                'values': values.tolist()
            }
        
        # 绘制雷达图
        plt.figure(figsize=figsize)
        
        # 计算角度
        angles = np.linspace(0, 2 * np.pi, n_metrics, endpoint=False).tolist()
        angles += angles[:1]  # 闭合图形
        
        for i, (concept, color) in enumerate(zip(concepts, plt.cm.tab20(np.linspace(0, 1, n_concepts)))):
            values = matrix[i, :].tolist()
            values += values[:1]  # 闭合图形
            plt.polar(angles, values, marker='o', linestyle='-', linewidth=2, color=color, label=concept)
            plt.fill(angles, values, alpha=0.2, color=color)
        
        # 添加标签
        plt.thetagrids(np.degrees(angles[:-1]), metrics)
        plt.title('Concept Application Effectiveness')
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"概念应用效果评估已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return effectiveness_analysis
    
    def generate_application_heatmap(self, application_data, output_path=None, figsize=(14, 10)):
        """生成概念应用热力图"""
        # 准备数据
        concepts = list(application_data.keys())
        contexts = list(set(context for concept in application_data.values() for context in concept.keys()))
        
        # 创建概念-语境矩阵
        n_concepts = len(concepts)
        n_contexts = len(contexts)
        matrix = np.zeros((n_concepts, n_contexts))
        
        for i, concept in enumerate(concepts):
            for j, context in enumerate(contexts):
                if context in application_data[concept]:
                    matrix[i, j] = application_data[concept][context]
        
        # 绘制热力图
        plt.figure(figsize=figsize)
        sns.heatmap(matrix, annot=True, cmap='viridis', xticklabels=contexts, yticklabels=concepts, cbar_kws={'label': 'Application Strength'})
        plt.title('Concept Application Heatmap')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"概念应用热力图已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return matrix

if __name__ == "__main__":
    # 示例使用
    analyzer = ConceptApplicationAnalyzer()
    
    # 示例1: 分析概念在不同领域的应用
    application_data = {
        "自由": {
            "政治": 5,
            "伦理": 4,
            "教育": 3,
            "艺术": 3
        },
        "正义": {
            "政治": 5,
            "伦理": 5,
            "法律": 5,
            "教育": 4
        },
        "理性": {
            "科学": 5,
            "哲学": 5,
            "教育": 4,
            "艺术": 2
        },
        "美德": {
            "伦理": 5,
            "教育": 4,
            "政治": 3,
            "艺术": 3
        },
        "真理": {
            "科学": 5,
            "哲学": 5,
            "宗教": 4,
            "教育": 4
        }
    }
    application_analysis = analyzer.analyze_concept_applications(application_data, output_path="concept_applications.png")
    print("\n概念应用分析:")
    for concept, analysis in application_analysis.items():
        print(f"{concept}: 平均应用强度 = {analysis['mean_application']:.2f}, 主导领域 = {analysis['dominant_domain']}")
    
    # 示例2: 分析概念应用的变化趋势
    trend_data = {
        "自由": {
            "1900": 3,
            "1950": 4,
            "2000": 5,
            "2050": 5
        },
        "正义": {
            "1900": 4,
            "1950": 4,
            "2000": 5,
            "2050": 5
        },
        "理性": {
            "1900": 5,
            "1950": 5,
            "2000": 4,
            "2050": 3
        },
        "美德": {
            "1900": 4,
            "1950": 3,
            "2000": 4,
            "2050": 4
        },
        "真理": {
            "1900": 5,
            "1950": 4,
            "2000": 4,
            "2050": 3
        }
    }
    trends = analyzer.analyze_application_trends(trend_data, output_path="application_trends.png")
    print("\n概念应用趋势分析:")
    for concept, trend in trends.items():
        print(f"{concept}: 趋势方向 = {trend['trend_direction']}, 斜率 = {trend['slope']:.4f}, R值 = {trend['r_value']:.4f}")
    
    # 示例3: 分析不同概念应用模式的相似性
    similarity_matrix = analyzer.analyze_application_similarities(application_data, output_path="application_similarities.png")
    print("\n概念应用相似性矩阵:")
    print(similarity_matrix)
    
    # 示例4: 评估概念应用的效果
    effectiveness_data = {
        "自由": {
            "社会影响": 4,
            "学术价值": 5,
            "实践效果": 4,
            "文化意义": 5
        },
        "正义": {
            "社会影响": 5,
            "学术价值": 5,
            "实践效果": 5,
            "文化意义": 4
        },
        "理性": {
            "社会影响": 4,
            "学术价值": 5,
            "实践效果": 4,
            "文化意义": 3
        },
        "美德": {
            "社会影响": 3,
            "学术价值": 4,
            "实践效果": 3,
            "文化意义": 4
        },
        "真理": {
            "社会影响": 4,
            "学术价值": 5,
            "实践效果": 3,
            "文化意义": 4
        }
    }
    effectiveness_analysis = analyzer.evaluate_application_effectiveness(effectiveness_data, output_path="application_effectiveness.png")
    print("\n概念应用效果评估:")
    for concept, analysis in effectiveness_analysis.items():
        print(f"{concept}: 总体效果 = {analysis['overall_effectiveness']:.2f}, 平均效果 = {analysis['mean_effectiveness']:.2f}")
    
    # 示例5: 生成概念应用热力图
    heatmap_data = {
        "自由": {
            "政治理论": 5,
            "伦理思考": 4,
            "教育实践": 3,
            "艺术创作": 3
        },
        "正义": {
            "政治理论": 5,
            "伦理思考": 5,
            "法律实践": 5,
            "教育实践": 4
        },
        "理性": {
            "科学研究": 5,
            "哲学思考": 5,
            "教育实践": 4,
            "艺术创作": 2
        },
        "美德": {
            "伦理思考": 5,
            "教育实践": 4,
            "政治理论": 3,
            "艺术创作": 3
        }
    }
    analyzer.generate_application_heatmap(heatmap_data, output_path="application_heatmap.png")