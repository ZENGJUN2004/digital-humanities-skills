import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from scipy import stats

class CrossCulturalAnalyzer:
    def __init__(self):
        pass
    
    def compare_concepts_across_cultures(self, concept_data, output_path=None, figsize=(14, 8)):
        """比较不同文化中的概念"""
        # 准备数据
        cultures = list(concept_data.keys())
        concepts = list(set(concept for culture in concept_data.values() for concept in culture.keys()))
        
        # 创建概念-文化矩阵
        n_concepts = len(concepts)
        n_cultures = len(cultures)
        matrix = np.zeros((n_concepts, n_cultures))
        
        for i, concept in enumerate(concepts):
            for j, culture in enumerate(cultures):
                if concept in concept_data[culture]:
                    matrix[i, j] = concept_data[culture][concept]
        
        # 分析概念在不同文化中的重要性
        concept_analysis = {}
        for i, concept in enumerate(concepts):
            values = matrix[i, :]
            mean_importance = np.mean(values)
            std_importance = np.std(values)
            variance = np.var(values)
            concept_analysis[concept] = {
                'mean_importance': mean_importance,
                'std_importance': std_importance,
                'variance': variance,
                'values': values.tolist()
            }
        
        # 绘制热力图
        plt.figure(figsize=figsize)
        sns.heatmap(matrix, annot=True, cmap='viridis', xticklabels=cultures, yticklabels=concepts, cbar_kws={'label': 'Importance'})
        plt.title('Concept Importance Across Cultures')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"跨文化概念比较已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return concept_analysis
    
    def analyze_philosophical_similarities(self, philosophy_data, output_path=None, figsize=(12, 10)):
        """分析不同文化哲学的相似性"""
        # 准备数据
        philosophies = list(philosophy_data.keys())
        concepts = list(set(concept for phil in philosophy_data.values() for concept in phil.keys()))
        
        # 创建哲学-概念矩阵
        n_philosophies = len(philosophies)
        n_concepts = len(concepts)
        matrix = np.zeros((n_philosophies, n_concepts))
        
        for i, phil in enumerate(philosophies):
            for j, concept in enumerate(concepts):
                if concept in philosophy_data[phil]:
                    matrix[i, j] = philosophy_data[phil][concept]
        
        # 计算相似性矩阵
        similarity_matrix = np.zeros((n_philosophies, n_philosophies))
        for i in range(n_philosophies):
            for j in range(n_philosophies):
                # 计算皮尔逊相关系数
                correlation, _ = stats.pearsonr(matrix[i, :], matrix[j, :])
                similarity_matrix[i, j] = correlation
        
        # 绘制相似性热力图
        plt.figure(figsize=figsize)
        sns.heatmap(similarity_matrix, annot=True, cmap='coolwarm', xticklabels=philosophies, yticklabels=philosophies, vmin=-1, vmax=1)
        plt.title('Philosophical Similarities Across Cultures')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"哲学相似性分析已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return similarity_matrix
    
    def analyze_conceptual_overlap(self, culture_data, output_path=None, figsize=(12, 8)):
        """分析不同文化中概念的重叠"""
        # 准备数据
        cultures = list(culture_data.keys())
        
        # 计算概念重叠
        overlap_analysis = {}
        
        # 计算每对文化之间的概念重叠
        for i, culture1 in enumerate(cultures):
            for j, culture2 in enumerate(cultures):
                if i < j:
                    concepts1 = set(culture_data[culture1].keys())
                    concepts2 = set(culture_data[culture2].keys())
                    
                    # 计算共同概念
                    common_concepts = concepts1.intersection(concepts2)
                    
                    # 计算重叠率
                    overlap_ratio = len(common_concepts) / min(len(concepts1), len(concepts2)) if min(len(concepts1), len(concepts2)) > 0 else 0
                    
                    # 计算Jaccard相似度
                    jaccard_similarity = len(common_concepts) / len(concepts1.union(concepts2)) if len(concepts1.union(concepts2)) > 0 else 0
                    
                    overlap_analysis[(culture1, culture2)] = {
                        'common_concepts': list(common_concepts),
                        'overlap_ratio': overlap_ratio,
                        'jaccard_similarity': jaccard_similarity,
                        'count_common': len(common_concepts),
                        'count_culture1': len(concepts1),
                        'count_culture2': len(concepts2)
                    }
        
        # 绘制概念重叠矩阵
        n_cultures = len(cultures)
        overlap_matrix = np.zeros((n_cultures, n_cultures))
        
        for i, culture1 in enumerate(cultures):
            for j, culture2 in enumerate(cultures):
                if i == j:
                    overlap_matrix[i, j] = 1.0
                elif i < j:
                    overlap_matrix[i, j] = overlap_analysis[(culture1, culture2)]['jaccard_similarity']
                    overlap_matrix[j, i] = overlap_analysis[(culture1, culture2)]['jaccard_similarity']
        
        plt.figure(figsize=figsize)
        sns.heatmap(overlap_matrix, annot=True, cmap='viridis', xticklabels=cultures, yticklabels=cultures, vmin=0, vmax=1, cbar_kws={'label': 'Jaccard Similarity'})
        plt.title('Conceptual Overlap Across Cultures')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"概念重叠分析已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return overlap_analysis
    
    def visualize_cultural_comparison(self, comparison_data, output_path=None, figsize=(14, 8)):
        """可视化文化比较"""
        # 准备数据
        categories = list(comparison_data.keys())
        cultures = list(comparison_data[categories[0]].keys())
        
        # 创建数据矩阵
        n_categories = len(categories)
        n_cultures = len(cultures)
        matrix = np.zeros((n_categories, n_cultures))
        
        for i, category in enumerate(categories):
            for j, culture in enumerate(cultures):
                matrix[i, j] = comparison_data[category][culture]
        
        # 绘制分组条形图
        plt.figure(figsize=figsize)
        
        bar_width = 0.8 / n_cultures
        indices = np.arange(n_categories)
        
        colors = plt.cm.Set3(np.linspace(0, 1, n_cultures))
        
        for i, (culture, color) in enumerate(zip(cultures, colors)):
            offset = (i - n_cultures/2 + 0.5) * bar_width
            plt.bar(indices + offset, matrix[:, i], bar_width, label=culture, color=color, alpha=0.7)
        
        plt.title('Cultural Comparison')
        plt.xlabel('Category')
        plt.ylabel('Value')
        plt.xticks(indices, categories, rotation=45, ha='right')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"文化比较可视化已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def analyze_philosophical_themes(self, theme_data, output_path=None, figsize=(14, 10)):
        """分析不同文化中的哲学主题"""
        # 准备数据
        themes = list(theme_data.keys())
        cultures = list(set(culture for theme in theme_data.values() for culture in theme.keys()))
        
        # 创建主题-文化矩阵
        n_themes = len(themes)
        n_cultures = len(cultures)
        matrix = np.zeros((n_themes, n_cultures))
        
        for i, theme in enumerate(themes):
            for j, culture in enumerate(cultures):
                if culture in theme_data[theme]:
                    matrix[i, j] = theme_data[theme][culture]
        
        # 分析主题在不同文化中的分布
        theme_analysis = {}
        for i, theme in enumerate(themes):
            values = matrix[i, :]
            dominant_culture = cultures[np.argmax(values)] if np.max(values) > 0 else None
            theme_analysis[theme] = {
                'dominant_culture': dominant_culture,
                'values': values.tolist()
            }
        
        # 绘制热力图
        plt.figure(figsize=figsize)
        sns.heatmap(matrix, annot=True, cmap='viridis', xticklabels=cultures, yticklabels=themes, cbar_kws={'label': 'Significance'})
        plt.title('Philosophical Themes Across Cultures')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"哲学主题分析已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return theme_analysis
    
    def generate_cultural_distance_map(self, culture_data, output_path=None, figsize=(12, 10)):
        """生成文化距离地图"""
        # 准备数据
        cultures = list(culture_data.keys())
        
        # 计算文化距离矩阵
        n_cultures = len(cultures)
        distance_matrix = np.zeros((n_cultures, n_cultures))
        
        for i in range(n_cultures):
            for j in range(n_cultures):
                if i != j:
                    # 计算欧氏距离
                    values1 = list(culture_data[cultures[i]].values())
                    values2 = list(culture_data[cultures[j]].values())
                    
                    # 确保维度一致
                    min_len = min(len(values1), len(values2))
                    values1 = values1[:min_len]
                    values2 = values2[:min_len]
                    
                    distance = np.linalg.norm(np.array(values1) - np.array(values2))
                    distance_matrix[i, j] = distance
        
        # 绘制距离热力图
        plt.figure(figsize=figsize)
        sns.heatmap(distance_matrix, annot=True, cmap='coolwarm', xticklabels=cultures, yticklabels=cultures, cbar_kws={'label': 'Distance'})
        plt.title('Cultural Distance Map')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"文化距离地图已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
        
        return distance_matrix

if __name__ == "__main__":
    # 示例使用
    analyzer = CrossCulturalAnalyzer()
    
    # 示例1: 比较不同文化中的概念
    concept_data = {
        "西方哲学": {
            "存在": 5,
            "知识": 5,
            "理性": 5,
            "自由": 4,
            "正义": 4
        },
        "中国哲学": {
            "道": 5,
            "德": 5,
            "仁": 5,
            "义": 4,
            "礼": 4
        },
        "印度哲学": {
            "梵": 5,
            "自我": 5,
            "解脱": 5,
            "业": 4,
            "轮回": 4
        }
    }
    concept_analysis = analyzer.compare_concepts_across_cultures(concept_data, output_path="cross_cultural_concepts.png")
    print("\n跨文化概念分析:")
    for concept, analysis in concept_analysis.items():
        print(f"{concept}: 平均重要性 = {analysis['mean_importance']:.2f}, 标准差 = {analysis['std_importance']:.2f}")
    
    # 示例2: 分析不同文化哲学的相似性
    philosophy_data = {
        "西方哲学": {
            "存在": 5,
            "知识": 5,
            "理性": 5,
            "自由": 4,
            "正义": 4
        },
        "中国哲学": {
            "道": 5,
            "德": 5,
            "仁": 5,
            "义": 4,
            "礼": 4
        },
        "印度哲学": {
            "梵": 5,
            "自我": 5,
            "解脱": 5,
            "业": 4,
            "轮回": 4
        },
        "伊斯兰哲学": {
            "真主": 5,
            "知识": 5,
            "理性": 4,
            "正义": 5,
            "道德": 4
        }
    }
    similarity_matrix = analyzer.analyze_philosophical_similarities(philosophy_data, output_path="philosophical_similarities.png")
    print("\n哲学相似性矩阵:")
    print(similarity_matrix)
    
    # 示例3: 分析不同文化中概念的重叠
    culture_data = {
        "西方哲学": {
            "存在": 5,
            "知识": 5,
            "理性": 5,
            "自由": 4,
            "正义": 4
        },
        "中国哲学": {
            "道": 5,
            "德": 5,
            "仁": 5,
            "义": 4,
            "礼": 4
        },
        "印度哲学": {
            "梵": 5,
            "自我": 5,
            "解脱": 5,
            "业": 4,
            "轮回": 4
        }
    }
    overlap_analysis = analyzer.analyze_conceptual_overlap(culture_data, output_path="conceptual_overlap.png")
    print("\n概念重叠分析:")
    for pair, analysis in overlap_analysis.items():
        print(f"{pair[0]} vs {pair[1]}: Jaccard相似度 = {analysis['jaccard_similarity']:.4f}, 共同概念数 = {analysis['count_common']}")
    
    # 示例4: 可视化文化比较
    comparison_data = {
        "形而上学": {
            "西方哲学": 5,
            "中国哲学": 4,
            "印度哲学": 5
        },
        "认识论": {
            "西方哲学": 5,
            "中国哲学": 3,
            "印度哲学": 4
        },
        "伦理学": {
            "西方哲学": 4,
            "中国哲学": 5,
            "印度哲学": 4
        },
        "政治哲学": {
            "西方哲学": 4,
            "中国哲学": 5,
            "印度哲学": 3
        }
    }
    analyzer.visualize_cultural_comparison(comparison_data, output_path="cultural_comparison.png")
    
    # 示例5: 分析不同文化中的哲学主题
    theme_data = {
        "宇宙论": {
            "西方哲学": 4,
            "中国哲学": 5,
            "印度哲学": 5
        },
        "人生哲学": {
            "西方哲学": 4,
            "中国哲学": 5,
            "印度哲学": 5
        },
        "方法论": {
            "西方哲学": 5,
            "中国哲学": 3,
            "印度哲学": 3
        },
        "价值论": {
            "西方哲学": 4,
            "中国哲学": 5,
            "印度哲学": 4
        }
    }
    theme_analysis = analyzer.analyze_philosophical_themes(theme_data, output_path="philosophical_themes.png")
    print("\n哲学主题分析:")
    for theme, analysis in theme_analysis.items():
        print(f"{theme}: 主导文化 = {analysis['dominant_culture']}")
    
    # 示例6: 生成文化距离地图
    distance_data = {
        "西方哲学": {
            "形而上学": 5,
            "认识论": 5,
            "伦理学": 4,
            "政治哲学": 4
        },
        "中国哲学": {
            "形而上学": 4,
            "认识论": 3,
            "伦理学": 5,
            "政治哲学": 5
        },
        "印度哲学": {
            "形而上学": 5,
            "认识论": 4,
            "伦理学": 4,
            "政治哲学": 3
        }
    }
    distance_matrix = analyzer.generate_cultural_distance_map(distance_data, output_path="cultural_distance_map.png")
    print("\n文化距离矩阵:")
    print(distance_matrix)