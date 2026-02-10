import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from collections import defaultdict

class ConceptVisualizer:
    def __init__(self):
        pass
    
    def visualize_concept_hierarchy(self, hierarchy, output_path=None, figsize=(12, 10), node_size=3000, font_size=10):
        """可视化概念层次结构"""
        # 构建层次网络
        G = nx.DiGraph()
        
        # 递归添加节点和边
        def add_nodes_edges(parent, children, level=0):
            for child, grandchildren in children.items():
                G.add_node(child, level=level+1)
                if parent:
                    G.add_edge(parent, child)
                if grandchildren:
                    add_nodes_edges(child, grandchildren, level+1)
        
        # 添加根节点和子节点
        for root, children in hierarchy.items():
            G.add_node(root, level=0)
            add_nodes_edges(root, children)
        
        # 计算布局
        pos = {}
        levels = defaultdict(list)
        for node, data in G.nodes(data=True):
            level = data.get('level', 0)
            levels[level].append(node)
        
        # 为每个层级分配y坐标
        max_level = max(levels.keys())
        for level, nodes in levels.items():
            y = 1.0 - (level / (max_level + 1))  # 从顶部到底部
            n_nodes = len(nodes)
            for i, node in enumerate(nodes):
                x = (i + 0.5) / n_nodes  # 水平均匀分布
                pos[node] = (x, y)
        
        # 绘制图形
        plt.figure(figsize=figsize)
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, alpha=0.7)
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='#3498db', alpha=0.8)
        
        # 绘制标签
        nx.draw_networkx_labels(G, pos, font_size=font_size, font_weight='bold')
        
        plt.title('Concept Hierarchy Visualization')
        plt.axis('off')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"概念层次结构可视化已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def visualize_concept_evolution(self, concept_timeline, output_path=None, figsize=(14, 8)):
        """可视化概念演变"""
        # 准备数据
        concepts = list(concept_timeline.keys())
        time_periods = sorted(list(set(period for concept in concept_timeline.values() for period in concept.keys())))
        
        # 创建时间-概念矩阵
        matrix = np.zeros((len(concepts), len(time_periods)))
        for i, concept in enumerate(concepts):
            for j, period in enumerate(time_periods):
                if period in concept_timeline[concept]:
                    matrix[i, j] = concept_timeline[concept][period]
        
        # 创建自定义颜色映射
        colors = [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]
        cmap = LinearSegmentedColormap.from_list('evolution_cmap', colors, N=100)
        
        # 绘制热力图
        plt.figure(figsize=figsize)
        plt.imshow(matrix, cmap=cmap, aspect='auto', interpolation='nearest')
        
        # 添加颜色条
        plt.colorbar(label='Concept Significance')
        
        # 设置标签
        plt.xticks(np.arange(len(time_periods)), time_periods, rotation=45, ha='right')
        plt.yticks(np.arange(len(concepts)), concepts)
        
        plt.title('Concept Evolution Over Time')
        plt.xlabel('Time Period')
        plt.ylabel('Concept')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"概念演变可视化已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def visualize_concept_connections(self, concepts, connections, output_path=None, figsize=(12, 10), node_size=3000):
        """可视化概念关联"""
        # 构建网络
        G = nx.Graph()
        
        # 添加节点
        for concept, importance in concepts.items():
            G.add_node(concept, importance=importance)
        
        # 添加边
        for source, target, strength in connections:
            if source in G.nodes and target in G.nodes:
                G.add_edge(source, target, strength=strength)
        
        # 计算布局
        pos = nx.spring_layout(G, k=0.3, iterations=200)
        
        # 准备节点大小和颜色
        node_sizes = [G.nodes[node]['importance'] * node_size for node in G.nodes]
        node_colors = list(range(len(G.nodes)))
        
        # 准备边的宽度
        edge_widths = [edge[2]['strength'] * 2 for edge in G.edges(data=True)]
        
        # 绘制图形
        plt.figure(figsize=figsize)
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.7)
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.viridis, alpha=0.8)
        
        # 绘制标签
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        plt.title('Concept Connections Visualization')
        plt.axis('off')
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"概念关联可视化已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def visualize_concept_comparison(self, concept_data, output_path=None, figsize=(14, 8)):
        """可视化不同哲学流派的概念对比"""
        # 准备数据
        concepts = list(concept_data.keys())
        schools = list(set(school for concept_values in concept_data.values() for school in concept_values.keys()))
        
        # 创建数据矩阵
        n_concepts = len(concepts)
        n_schools = len(schools)
        matrix = np.zeros((n_concepts, n_schools))
        
        for i, concept in enumerate(concepts):
            for j, school in enumerate(schools):
                if school in concept_data[concept]:
                    matrix[i, j] = concept_data[concept][school]
        
        # 绘制分组条形图
        plt.figure(figsize=figsize)
        
        bar_width = 0.8 / n_schools
        indices = np.arange(n_concepts)
        
        colors = plt.cm.Set3(np.linspace(0, 1, n_schools))
        
        for i, (school, color) in enumerate(zip(schools, colors)):
            offset = (i - n_schools/2 + 0.5) * bar_width
            plt.bar(indices + offset, matrix[:, i], bar_width, label=school, color=color, alpha=0.7)
        
        plt.xlabel('Concepts')
        plt.ylabel('Significance')
        plt.title('Concept Comparison Across Philosophical Schools')
        plt.xticks(indices, concepts, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"概念对比可视化已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def visualize_concept_cloud(self, concepts, output_path=None, figsize=(12, 10)):
        """可视化概念云"""
        try:
            from wordcloud import WordCloud
            
            # 准备词频数据
            word_freq = {concept: weight for concept, weight in concepts.items()}
            
            # 创建词云
            wordcloud = WordCloud(width=1200, height=1000, background_color='white', 
                                 colormap='viridis', max_font_size=200, 
                                 min_font_size=20, prefer_horizontal=0.8)
            
            wordcloud.generate_from_frequencies(word_freq)
            
            # 绘制词云
            plt.figure(figsize=figsize)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title('Concept Cloud Visualization')
            
            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                print(f"概念云可视化已保存至: {output_path}")
            else:
                plt.show()
            
            plt.close()
        except ImportError:
            print("需要安装wordcloud库来生成概念云: pip install wordcloud")

if __name__ == "__main__":
    # 示例使用
    visualizer = ConceptVisualizer()
    
    # 示例1: 概念层次结构可视化
    hierarchy = {
        "哲学": {
            "形而上学": {
                "存在论": {},
                "本体论": {},
                "宇宙论": {}
            },
            "认识论": {
                "经验主义": {},
                "理性主义": {},
                "怀疑论": {}
            },
            "伦理学": {
                "功利主义": {},
                "义务论": {},
                "美德伦理学": {}
            }
        }
    }
    visualizer.visualize_concept_hierarchy(hierarchy, output_path="concept_hierarchy.png")
    
    # 示例2: 概念演变可视化
    concept_timeline = {
        "存在": {"古希腊": 5, "中世纪": 3, "近代": 4, "现代": 5},
        "知识": {"古希腊": 4, "中世纪": 3, "近代": 5, "现代": 4},
        "价值": {"古希腊": 3, "中世纪": 4, "近代": 4, "现代": 5},
        "理性": {"古希腊": 5, "中世纪": 2, "近代": 5, "现代": 3},
        "自由": {"古希腊": 2, "中世纪": 1, "近代": 5, "现代": 4}
    }
    visualizer.visualize_concept_evolution(concept_timeline, output_path="concept_evolution.png")
    
    # 示例3: 概念关联可视化
    concepts = {
        "存在": 5,
        "知识": 4,
        "价值": 4,
        "理性": 3,
        "自由": 4,
        "正义": 3,
        "真理": 4
    }
    connections = [
        ("存在", "知识", 0.8),
        ("存在", "价值", 0.6),
        ("知识", "理性", 0.9),
        ("知识", "真理", 0.8),
        ("价值", "自由", 0.7),
        ("价值", "正义", 0.9),
        ("自由", "理性", 0.5),
        ("正义", "真理", 0.6)
    ]
    visualizer.visualize_concept_connections(concepts, connections, output_path="concept_connections.png")
    
    # 示例4: 概念对比可视化
    concept_data = {
        "存在": {"柏拉图主义": 5, "亚里士多德主义": 4, "经验主义": 3, "存在主义": 5},
        "知识": {"柏拉图主义": 4, "亚里士多德主义": 5, "经验主义": 5, "存在主义": 3},
        "价值": {"柏拉图主义": 4, "亚里士多德主义": 4, "经验主义": 3, "存在主义": 5},
        "理性": {"柏拉图主义": 5, "亚里士多德主义": 5, "经验主义": 2, "存在主义": 2},
        "自由": {"柏拉图主义": 2, "亚里士多德主义": 3, "经验主义": 4, "存在主义": 5}
    }
    visualizer.visualize_concept_comparison(concept_data, output_path="concept_comparison.png")
    
    # 示例5: 概念云可视化
    concept_cloud_data = {
        "存在": 100,
        "知识": 90,
        "价值": 85,
        "理性": 80,
        "自由": 75,
        "正义": 70,
        "真理": 65,
        "美德": 60,
        "幸福": 55,
        "意义": 50
    }
    visualizer.visualize_concept_cloud(concept_cloud_data, output_path="concept_cloud.png")