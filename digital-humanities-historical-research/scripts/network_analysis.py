import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag

class NetworkAnalysis:
    def __init__(self, texts):
        """
        Initialize NetworkAnalysis with historical texts
        texts: list of historical text strings
        """
        self.texts = texts
        self.graph = nx.Graph()
    
    def extract_relationships(self):
        """
        Extract relationships between historical figures from texts
        """
        relationships = []
        
        for text in self.texts:
            sentences = sent_tokenize(text)
            for sentence in sentences:
                # Extract potential relationships
                # Simple heuristic: look for named entities connected by relational verbs
                tokens = word_tokenize(sentence)
                tagged_tokens = pos_tag(tokens)
                
                # Extract proper nouns (potential entities)
                entities = []
                i = 0
                while i < len(tagged_tokens):
                    word, tag = tagged_tokens[i]
                    if word.istitle() and tag in ['NNP', 'NNPS']:
                        # Multi-word entity
                        entity = word
                        j = i + 1
                        while j < len(tagged_tokens) and tagged_tokens[j][0].istitle() and tagged_tokens[j][1] in ['NNP', 'NNPS']:
                            entity += ' ' + tagged_tokens[j][0]
                            j += 1
                        entities.append(entity)
                        i = j
                    else:
                        i += 1
                
                # If we have multiple entities in the sentence, assume relationships
                if len(entities) >= 2:
                    # Create edges between all pairs of entities
                    for i in range(len(entities)):
                        for j in range(i + 1, len(entities)):
                            relationships.append((entities[i], entities[j]))
        
        return relationships
    
    def build_network(self):
        """
        Build social network from extracted relationships
        """
        relationships = self.extract_relationships()
        
        # Count relationship frequencies
        relationship_counts = defaultdict(int)
        for source, target in relationships:
            if source != target:
                # Ensure consistent ordering
                if source > target:
                    source, target = target, source
                relationship_counts[(source, target)] += 1
        
        # Add nodes and edges to graph
        for (source, target), weight in relationship_counts.items():
            self.graph.add_node(source)
            self.graph.add_node(target)
            self.graph.add_edge(source, target, weight=weight)
        
        return self.graph
    
    def analyze_network(self):
        """
        Analyze network properties
        """
        if not self.graph.nodes():
            self.build_network()
        
        analysis = {
            'nodes': len(self.graph.nodes()),
            'edges': len(self.graph.edges()),
            'density': nx.density(self.graph),
            'connected_components': nx.number_connected_components(self.graph),
            'centrality': {
                'degree': nx.degree_centrality(self.graph),
                'betweenness': nx.betweenness_centrality(self.graph),
                'closeness': nx.closeness_centrality(self.graph)
            },
            'communities': self.detect_communities()
        }
        
        return analysis
    
    def detect_communities(self):
        """
        Detect communities in the network
        """
        # Use greedy modularity community detection
        try:
            from networkx.algorithms.community import greedy_modularity_communities
            communities = list(greedy_modularity_communities(self.graph))
            # Convert sets to lists for easier handling
            return [list(community) for community in communities]
        except ImportError:
            # Fallback to connected components
            return list(nx.connected_components(self.graph))
    
    def visualize_network(self, output_file=None):
        """
        Visualize the network
        """
        if not self.graph.nodes():
            self.build_network()
        
        # Set up visualization
        plt.figure(figsize=(12, 10))
        
        # Use spring layout for better visualization
        pos = nx.spring_layout(self.graph, k=0.3, iterations=50)
        
        # Draw nodes with size based on degree
        degrees = dict(self.graph.degree())
        node_sizes = [v * 100 for v in degrees.values()]
        nx.draw_networkx_nodes(self.graph, pos, node_size=node_sizes, node_color='lightblue')
        
        # Draw edges with width based on weight
        edges = self.graph.edges(data=True)
        edge_weights = [d['weight'] for (u, v, d) in edges]
        nx.draw_networkx_edges(self.graph, pos, width=edge_weights, edge_color='gray')
        
        # Draw labels for important nodes (high degree)
        important_nodes = {k: v for k, v in degrees.items() if v > 1}
        nx.draw_networkx_labels(self.graph, pos, labels={node: node for node in important_nodes})
        
        plt.title('Historical Figure Network')
        plt.axis('off')
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
        
        return plt
    
    def identify_key_figures(self, top_n=5):
        """
        Identify key figures in the network based on centrality measures
        """
        if not self.graph.nodes():
            self.build_network()
        
        # Calculate centrality measures
        degree_centrality = nx.degree_centrality(self.graph)
        betweenness_centrality = nx.betweenness_centrality(self.graph)
        closeness_centrality = nx.closeness_centrality(self.graph)
        
        # Combine centrality measures
        key_figures = {}
        for node in self.graph.nodes():
            # Weighted combination of centrality measures
            score = (degree_centrality[node] * 0.4 + 
                     betweenness_centrality[node] * 0.4 + 
                     closeness_centrality[node] * 0.2)
            key_figures[node] = score
        
        # Sort by score and return top n
        sorted_figures = sorted(key_figures.items(), key=lambda x: x[1], reverse=True)
        return sorted_figures[:top_n]
    
    def analyze_relationship_strength(self):
        """
        Analyze the strength of relationships in the network
        """
        if not self.graph.nodes():
            self.build_network()
        
        # Extract edge weights
        edge_weights = []
        for u, v, d in self.graph.edges(data=True):
            edge_weights.append((u, v, d.get('weight', 1)))
        
        # Sort by weight
        edge_weights.sort(key=lambda x: x[2], reverse=True)
        
        return edge_weights
    
    def export_network(self, file_path, format='graphml'):
        """
        Export network to file
        """
        if not self.graph.nodes():
            self.build_network()
        
        if format == 'graphml':
            nx.write_graphml(self.graph, file_path)
        elif format == 'gexf':
            nx.write_gexf(self.graph, file_path)
        elif format == 'gml':
            nx.write_gml(self.graph, file_path)
        elif format == 'json':
            import json
            # Convert graph to JSON format
            graph_data = {
                'nodes': [{'id': node} for node in self.graph.nodes()],
                'links': [{'source': u, 'target': v, 'weight': d.get('weight', 1)} 
                         for u, v, d in self.graph.edges(data=True)]
            }
            with open(file_path, 'w') as f:
                json.dump(graph_data, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
