import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import json

class SemanticNetworkAnalyzer:
    def __init__(self):
        self.network = nx.Graph()
    
    def build_network_from_text(self, text, window_size=2):
        """从文本构建语义网络"""
        # 简单的文本处理
        words = text.lower().split()
        words = [word.strip('.,!?:;"()[]') for word in words]
        words = [word for word in words if word]
        
        # 构建共现网络
        for i, word in enumerate(words):
            if word not in self.network.nodes:
                self.network.add_node(word)
            
            # 窗口内的共现关系
            for j in range(i+1, min(i+window_size+1, len(words))):
                neighbor = words[j]
                if neighbor not in self.network.nodes:
                    self.network.add_node(neighbor)
                
                if self.network.has_edge(word, neighbor):
                    self.network[word][neighbor]['weight'] += 1
                else:
                    self.network.add_edge(word, neighbor, weight=1)
        
        return self.network
    
    def build_network_from_concepts(self, concepts, relationships):
        """从概念和关系构建语义网络"""
        # 添加概念节点
        for concept in concepts:
            self.network.add_node(concept)
        
        # 添加关系边
        for source, target, relation in relationships:
            if source in self.network.nodes and target in self.network.nodes:
                self.network.add_edge(source, target, relation=relation)
        
        return self.network
    
    def analyze_network_features(self):
        """分析网络特征"""
        features = {
            'nodes': len(self.network.nodes),
            'edges': len(self.network.edges),
            'density': nx.density(self.network),
            'average_clustering': nx.average_clustering(self.network),
            'transitivity': nx.transitivity(self.network)
        }
        
        if nx.is_connected(self.network):
            features['average_shortest_path_length'] = nx.average_shortest_path_length(self.network)
        
        return features
    
    def calculate_centrality(self):
        """计算网络中心性"""
        centrality = {
            'degree_centrality': nx.degree_centrality(self.network),
            'betweenness_centrality': nx.betweenness_centrality(self.network),
            'closeness_centrality': nx.closeness_centrality(self.network),
            'eigenvector_centrality': nx.eigenvector_centrality(self.network, max_iter=1000) if len(self.network) > 0 else {}
        }
        
        return centrality
    
    def identify_communities(self):
        """识别网络社区"""
        try:
            # 使用贪婪模块度最大化算法
            communities = list(nx.community.greedy_modularity_communities(self.network))
            return communities
        except Exception as e:
            print(f"社区识别失败: {e}")
            return []
    
    def visualize_network(self, output_path=None, figsize=(12, 10), node_size=300, font_size=8):
        """可视化语义网络"""
        plt.figure(figsize=figsize)
        
        # 计算布局
        pos = nx.spring_layout(self.network, k=0.15, iterations=200)
        
        # 绘制节点
        nx.draw_networkx_nodes(self.network, pos, node_size=node_size, alpha=0.7)
        
        # 绘制边
        nx.draw_networkx_edges(self.network, pos, alpha=0.3)
        
        # 绘制标签
        nx.draw_networkx_labels(self.network, pos, font_size=font_size)
        
        plt.title('Semantic Network Visualization')
        plt.axis('off')
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"网络可视化已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def export_network(self, output_path, format='graphml'):
        """导出网络为不同格式"""
        try:
            if format == 'graphml':
                nx.write_graphml(self.network, output_path)
            elif format == 'gexf':
                nx.write_gexf(self.network, output_path)
            elif format == 'json':
                # 自定义JSON格式
                network_data = {
                    'nodes': list(self.network.nodes),
                    'edges': [(u, v, d) for u, v, d in self.network.edges(data=True)]
                }
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(network_data, f, ensure_ascii=False, indent=2)
            print(f"网络已导出至: {output_path}")
        except Exception as e:
            print(f"网络导出失败: {e}")
    
    def import_network(self, input_path, format='graphml'):
        """从文件导入网络"""
        try:
            if format == 'graphml':
                self.network = nx.read_graphml(input_path)
            elif format == 'gexf':
                self.network = nx.read_gexf(input_path)
            elif format == 'json':
                # 自定义JSON格式
                with open(input_path, 'r', encoding='utf-8') as f:
                    network_data = json.load(f)
                self.network = nx.Graph()
                for node in network_data['nodes']:
                    self.network.add_node(node)
                for u, v, d in network_data['edges']:
                    self.network.add_edge(u, v, **d)
            print(f"网络已从: {input_path} 导入")
        except Exception as e:
            print(f"网络导入失败: {e}")

if __name__ == "__main__":
    # 示例使用
    analyzer = SemanticNetworkAnalyzer()
    
    # 从文本构建网络
    sample_text = "哲学是对基本和普遍问题的研究，包括存在、知识、价值、理性、心灵和语言等。哲学的方法包括质疑、批判性讨论、理性论证和系统阐述。"
    analyzer.build_network_from_text(sample_text)
    
    # 分析网络特征
    features = analyzer.analyze_network_features()
    print("网络特征:")
    for key, value in features.items():
        print(f"{key}: {value}")
    
    # 计算中心性
    centrality = analyzer.calculate_centrality()
    print("\n中心性:")
    for key, values in centrality.items():
        print(f"\n{key}:")
        sorted_values = sorted(values.items(), key=lambda x: x[1], reverse=True)[:5]
        for node, value in sorted_values:
            print(f"{node}: {value:.4f}")
    
    # 识别社区
    communities = analyzer.identify_communities()
    print("\n社区:")
    for i, community in enumerate(communities):
        print(f"社区 {i+1}: {list(community)}")
    
    # 可视化网络
    analyzer.visualize_network(output_path="semantic_network.png")
    
    # 导出网络
    analyzer.export_network("semantic_network.graphml")
    analyzer.export_network("semantic_network.json", format="json")