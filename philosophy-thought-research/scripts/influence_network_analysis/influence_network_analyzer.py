import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import json

class InfluenceNetworkAnalyzer:
    def __init__(self):
        self.network = nx.DiGraph()
    
    def build_influence_network(self, influencers, relationships):
        """构建影响网络"""
        # 添加影响者节点
        for influencer, attributes in influencers.items():
            self.network.add_node(influencer, **attributes)
        
        # 添加影响关系边
        for source, target, weight, relation in relationships:
            if source in self.network.nodes and target in self.network.nodes:
                self.network.add_edge(source, target, weight=weight, relation=relation)
        
        return self.network
    
    def build_network_from_text(self, text_data, threshold=0.3):
        """从文本数据构建影响网络"""
        # 简单的文本处理和影响关系提取
        # 这里是一个示例实现，实际应用中可能需要更复杂的NLP技术
        
        # 假设text_data是一个字典，键是哲学家，值是包含他们思想和影响的文本
        for philosopher, text in text_data.items():
            self.network.add_node(philosopher)
        
        # 简单的共现分析来提取影响关系
        philosophers = list(text_data.keys())
        for i, phil1 in enumerate(philosophers):
            for j, phil2 in enumerate(philosophers):
                if i != j:
                    # 简单的文本相似度计算（示例）
                    text1 = text_data[phil1].lower()
                    text2 = text_data[phil2].lower()
                    
                    # 计算共同词的比例
                    words1 = set(text1.split())
                    words2 = set(text2.split())
                    common_words = words1.intersection(words2)
                    similarity = len(common_words) / min(len(words1), len(words2)) if min(len(words1), len(words2)) > 0 else 0
                    
                    if similarity > threshold:
                        self.network.add_edge(phil1, phil2, weight=similarity, relation="influence")
        
        return self.network
    
    def analyze_network_properties(self):
        """
        分析网络属性
        """
        properties = {
            'nodes': len(self.network.nodes),
            'edges': len(self.network.edges),
            'density': nx.density(self.network),
            'average_clustering': nx.average_clustering(self.network.to_undirected()),
            'transitivity': nx.transitivity(self.network.to_undirected())
        }
        
        try:
            if nx.is_strongly_connected(self.network):
                properties['average_shortest_path_length'] = nx.average_shortest_path_length(self.network)
        except nx.NetworkXError:
            # 如果图不是强连通的，跳过平均最短路径长度的计算
            pass
        
        return properties
    
    def identify_key_influencers(self, top_n=10):
        """
        识别关键影响者
        """
        # 计算各种中心性
        centrality = {
            'degree_centrality': nx.degree_centrality(self.network),
            'in_degree_centrality': nx.in_degree_centrality(self.network),
            'out_degree_centrality': nx.out_degree_centrality(self.network),
            'betweenness_centrality': nx.betweenness_centrality(self.network),
            'eigenvector_centrality': {}
        }
        
        # 尝试计算特征向量中心性，处理非强连通图的情况
        try:
            if len(self.network) > 0:
                centrality['eigenvector_centrality'] = nx.eigenvector_centrality(self.network, max_iter=1000, tol=1e-06)
        except nx.NetworkXError:
            # 如果图不是强连通的，使用近似方法
            pass
        
        # 综合排名
        key_influencers = {}
        for node in self.network.nodes:
            score = 0
            if node in centrality['degree_centrality']:
                score += centrality['degree_centrality'][node] * 0.2
            if node in centrality['in_degree_centrality']:
                score += centrality['in_degree_centrality'][node] * 0.3
            if node in centrality['out_degree_centrality']:
                score += centrality['out_degree_centrality'][node] * 0.2
            if node in centrality['betweenness_centrality']:
                score += centrality['betweenness_centrality'][node] * 0.2
            if node in centrality['eigenvector_centrality']:
                score += centrality['eigenvector_centrality'][node] * 0.1
            key_influencers[node] = score
        
        # 排序并返回前N个
        sorted_influencers = sorted(key_influencers.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        return {
            'centrality': centrality,
            'key_influencers': sorted_influencers
        }
    
    def analyze_influence_paths(self, source, target, max_paths=5):
        """分析影响路径"""
        try:
            # 查找所有简单路径
            all_paths = list(nx.all_simple_paths(self.network, source=source, target=target))
            
            # 按路径长度排序
            all_paths.sort(key=len)
            
            # 选择前N个最短路径
            shortest_paths = all_paths[:max_paths]
            
            # 计算路径权重
            path_weights = []
            for path in shortest_paths:
                weight = 1.0
                for i in range(len(path)-1):
                    edge_weight = self.network[path[i]][path[i+1]].get('weight', 1.0)
                    weight *= edge_weight
                path_weights.append((path, weight))
            
            # 按权重排序
            path_weights.sort(key=lambda x: x[1], reverse=True)
            
            return path_weights
        except nx.NetworkXNoPath:
            return []
        except Exception as e:
            print(f"分析影响路径时出错: {e}")
            return []
    
    def analyze_influence_communities(self):
        """分析影响社区"""
        try:
            # 使用Louvain算法检测社区
            communities = list(nx.community.greedy_modularity_communities(self.network.to_undirected()))
            
            # 分析每个社区的特征
            community_analysis = {}
            for i, community in enumerate(communities):
                subgraph = self.network.subgraph(community)
                community_analysis[f"Community {i+1}"] = {
                    'members': list(community),
                    'size': len(community),
                    'density': nx.density(subgraph),
                    'edges': len(subgraph.edges)
                }
            
            return community_analysis
        except Exception as e:
            print(f"分析影响社区时出错: {e}")
            return {}
    
    def visualize_influence_network(self, output_path=None, figsize=(16, 12), node_size=3000, font_size=10):
        """可视化影响网络"""
        plt.figure(figsize=figsize)
        
        # 计算布局
        pos = nx.spring_layout(self.network, k=0.15, iterations=200)
        
        # 绘制节点
        node_sizes = [nx.degree(self.network, node) * 1000 for node in self.network.nodes]
        nx.draw_networkx_nodes(self.network, pos, node_size=node_sizes, alpha=0.7, node_color='#3498db')
        
        # 绘制边
        edge_weights = [self.network[u][v].get('weight', 1.0) for u, v in self.network.edges]
        nx.draw_networkx_edges(self.network, pos, width=[w*2 for w in edge_weights], alpha=0.5, edge_color='#7f8c8d', arrowsize=20)
        
        # 绘制标签
        nx.draw_networkx_labels(self.network, pos, font_size=font_size, font_weight='bold')
        
        plt.title('Influence Network Visualization')
        plt.axis('off')
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"影响网络可视化已保存至: {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def visualize_influence_paths(self, paths, output_path=None, figsize=(14, 10)):
        """可视化影响路径"""
        # 构建路径子图
        path_edges = []
        for path, _ in paths:
            for i in range(len(path)-1):
                path_edges.append((path[i], path[i+1]))
        
        subgraph = self.network.edge_subgraph(path_edges)
        
        plt.figure(figsize=figsize)
        
        # 计算布局
        pos = nx.spring_layout(subgraph, k=0.2, iterations=200)
        
        # 绘制节点
        nx.draw_networkx_nodes(subgraph, pos, node_size=4000, alpha=0.8, node_color='#e74c3c')
        
        # 绘制边
        edge_weights = [subgraph[u][v].get('weight', 1.0) for u, v in subgraph.edges]
        nx.draw_networkx_edges(subgraph, pos, width=[w*3 for w in edge_weights], alpha=0.8, edge_color='#c0392b', arrowsize=25)
        
        # 绘制标签
        nx.draw_networkx_labels(subgraph, pos, font_size=12, font_weight='bold')
        
        plt.title('Influence Paths Visualization')
        plt.axis('off')
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"影响路径可视化已保存至: {output_path}")
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
                    'nodes': [{'id': node, **self.network.nodes[node]} for node in self.network.nodes],
                    'edges': [{'source': u, 'target': v, **self.network[u][v]} for u, v in self.network.edges]
                }
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(network_data, f, ensure_ascii=False, indent=2)
            print(f"网络已导出至: {output_path}")
        except Exception as e:
            print(f"导出网络时出错: {e}")
    
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
                self.network = nx.DiGraph()
                for node in network_data['nodes']:
                    node_id = node.pop('id')
                    self.network.add_node(node_id, **node)
                for edge in network_data['edges']:
                    source = edge.pop('source')
                    target = edge.pop('target')
                    self.network.add_edge(source, target, **edge)
            print(f"网络已从: {input_path} 导入")
        except Exception as e:
            print(f"导入网络时出错: {e}")

if __name__ == "__main__":
    # 示例使用
    analyzer = InfluenceNetworkAnalyzer()
    
    # 示例1: 构建影响网络
    influencers = {
        "柏拉图": {"era": "古希腊", "school": "柏拉图主义"},
        "亚里士多德": {"era": "古希腊", "school": "亚里士多德主义"},
        "笛卡尔": {"era": "近代", "school": "理性主义"},
        "洛克": {"era": "近代", "school": "经验主义"},
        "康德": {"era": "近代", "school": "德国唯心主义"},
        "黑格尔": {"era": "近代", "school": "德国唯心主义"},
        "尼采": {"era": "现代", "school": "存在主义"},
        "胡塞尔": {"era": "现代", "school": "现象学"},
        "海德格尔": {"era": "现代", "school": "存在主义"},
        "萨特": {"era": "现代", "school": "存在主义"}
    }
    
    relationships = [
        ("柏拉图", "亚里士多德", 0.9, "teacher"),
        ("亚里士多德", "笛卡尔", 0.6, "influence"),
        ("笛卡尔", "康德", 0.8, "influence"),
        ("洛克", "康德", 0.7, "influence"),
        ("康德", "黑格尔", 0.9, "influence"),
        ("黑格尔", "尼采", 0.7, "influence"),
        ("笛卡尔", "胡塞尔", 0.6, "influence"),
        ("胡塞尔", "海德格尔", 0.9, "teacher"),
        ("海德格尔", "萨特", 0.8, "influence"),
        ("尼采", "萨特", 0.7, "influence")
    ]
    
    analyzer.build_influence_network(influencers, relationships)
    
    # 示例2: 分析网络属性
    properties = analyzer.analyze_network_properties()
    print("网络属性:")
    for key, value in properties.items():
        print(f"{key}: {value}")
    
    # 示例3: 识别关键影响者
    key_influencers = analyzer.identify_key_influencers()
    print("\n关键影响者:")
    for influencer, score in key_influencers['key_influencers']:
        print(f"{influencer}: {score:.4f}")
    
    # 示例4: 分析影响路径
    paths = analyzer.analyze_influence_paths("柏拉图", "萨特")
    print("\n影响路径 (柏拉图 -> 萨特):")
    for path, weight in paths:
        print(f"路径: {' -> '.join(path)}, 权重: {weight:.4f}")
    
    # 示例5: 分析影响社区
    communities = analyzer.analyze_influence_communities()
    print("\n影响社区:")
    for community, analysis in communities.items():
        print(f"{community}: {analysis['members']}")
    
    # 示例6: 可视化影响网络
    analyzer.visualize_influence_network(output_path="influence_network.png")
    
    # 示例7: 可视化影响路径
    if paths:
        analyzer.visualize_influence_paths(paths, output_path="influence_paths.png")
    
    # 示例8: 导出网络
    analyzer.export_network("influence_network.graphml")
    analyzer.export_network("influence_network.json", format="json")