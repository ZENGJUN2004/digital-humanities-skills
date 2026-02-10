#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
论证分析工具
用于分析哲学文本中的论证结构、逻辑关系、推理链条
"""

import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import networkx as nx
import matplotlib.pyplot as plt

class ArgumentAnalyzer:
    """
    论证分析器类
    """
    
    def __init__(self, text_path=None, text_content=None):
        """
        初始化论证分析器
        
        Args:
            text_path (str, optional): 文本文件路径
            text_content (str, optional): 文本内容
        """
        self.text_path = text_path
        self.text_content = text_content
        self.text = None
        self.sentences = []
        self.arguments = []
        self.argument_graph = None
        
        # 加载NLTK资源
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            print(f"加载NLTK资源时出错: {e}")
        
        # 加载文本
        if text_path:
            self.load_text_from_file(text_path)
        elif text_content:
            self.text = text_content
            self.process_text()
    
    def load_text_from_file(self, file_path):
        """
        从文件加载文本
        
        Args:
            file_path (str): 文本文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.text = f.read()
            self.process_text()
            print(f"成功加载文本: {file_path}")
        except Exception as e:
            print(f"加载文本时出错: {e}")
    
    def process_text(self):
        """
        处理文本，进行分句等
        """
        if not self.text:
            return
        
        # 分句
        self.sentences = sent_tokenize(self.text)
    
    def extract_arguments(self):
        """
        提取论证结构
        
        Returns:
            list: 论证列表
        """
        if not self.sentences:
            return []
        
        # 识别论证标记词
        premise_markers = [
            'because', 'since', 'as', 'for', 'given that', 'assuming that',
            'due to', 'owing to', 'on account of', 'in view of', 'considering that',
            'firstly', 'secondly', 'thirdly', 'finally', 'furthermore', 'moreover',
            'additionally', 'in addition', 'besides', 'what is more'
        ]
        
        conclusion_markers = [
            'therefore', 'thus', 'hence', 'consequently', 'as a result', 'so',
            'it follows that', 'we can conclude that', 'thus we see that',
            'in conclusion', 'to conclude', 'finally', 'accordingly', 'henceforth',
            'ergo', 'therefore', 'thereby', 'wherefore'
        ]
        
        # 提取论证
        arguments = []
        current_argument = {
            'premises': [],
            'conclusion': None,
            'inference_type': 'deductive',  # 默认推理类型
            'sentence_indices': []
        }
        
        for i, sentence in enumerate(self.sentences):
            sentence_lower = sentence.lower()
            
            # 检查是否包含结论标记词
            contains_conclusion_marker = any(marker in sentence_lower for marker in conclusion_markers)
            
            # 检查是否包含前提标记词
            contains_premise_marker = any(marker in sentence_lower for marker in premise_markers)
            
            if contains_premise_marker:
                # 这是一个前提
                current_argument['premises'].append(sentence)
                current_argument['sentence_indices'].append(i)
            elif contains_conclusion_marker:
                # 这是一个结论
                current_argument['conclusion'] = sentence
                current_argument['sentence_indices'].append(i)
                
                # 完成当前论证并添加到列表
                if current_argument['premises'] and current_argument['conclusion']:
                    arguments.append(current_argument.copy())
                    # 重置当前论证
                    current_argument = {
                        'premises': [],
                        'conclusion': None,
                        'inference_type': 'deductive',
                        'sentence_indices': []
                    }
            else:
                # 可能是论证的一部分，需要根据上下文判断
                # 这里简单处理，将其添加到当前论证的前提中
                current_argument['premises'].append(sentence)
                current_argument['sentence_indices'].append(i)
        
        # 添加最后一个论证（如果有）
        if current_argument['premises']:
            # 如果没有明确的结论，尝试从前提中推断
            if not current_argument['conclusion'] and len(current_argument['premises']) > 1:
                # 假设最后一个前提是结论
                current_argument['conclusion'] = current_argument['premises'][-1]
                current_argument['premises'] = current_argument['premises'][:-1]
            
            if current_argument['conclusion']:
                arguments.append(current_argument)
        
        self.arguments = arguments
        return arguments
    
    def analyze_argument_structure(self, argument):
        """
        分析论证结构
        
        Args:
            argument (dict): 论证
            
        Returns:
            dict: 论证结构分析结果
        """
        analysis = {
            'premise_count': len(argument['premises']),
            'has_conclusion': bool(argument['conclusion']),
            'inference_type': self.identify_inference_type(argument),
            'logical_structure': self.analyze_logical_structure(argument),
            'strength': self.evaluate_argument_strength(argument)
        }
        
        return analysis
    
    def identify_inference_type(self, argument):
        """
        识别推理类型
        
        Args:
            argument (dict): 论证
            
        Returns:
            str: 推理类型
        """
        # 这里使用简单的规则来识别推理类型
        # 实际应用中可以使用更复杂的方法
        
        conclusion = argument.get('conclusion', '').lower()
        
        # 归纳推理标记词
        inductive_markers = ['probably', 'likely', 'most likely', 'chances are',
                           'it is probable that', 'it is likely that', 'we can infer that']
        
        # 演绎推理标记词
        deductive_markers = ['necessarily', 'must', 'certainly', 'absolutely',
                            'it necessarily follows that', 'it must be that']
        
        # 类比推理标记词
        analogical_markers = ['like', 'as', 'similar to', 'analogous to',
                            'by analogy', 'in the same way', 'just as']
        
        if any(marker in conclusion for marker in inductive_markers):
            return 'inductive'
        elif any(marker in conclusion for marker in deductive_markers):
            return 'deductive'
        elif any(marker in conclusion for marker in analogical_markers):
            return 'analogical'
        else:
            # 默认推理类型
            return 'deductive'
    
    def analyze_logical_structure(self, argument):
        """
        分析逻辑结构
        
        Args:
            argument (dict): 论证
            
        Returns:
            str: 逻辑结构
        """
        premises = argument.get('premises', [])
        
        if len(premises) == 0:
            return 'no premises'
        elif len(premises) == 1:
            return 'single premise'
        else:
            # 检查是否是连锁论证
            is_chain = any('therefore' in premise.lower() or 'thus' in premise.lower() for premise in premises)
            if is_chain:
                return 'chain argument'
            else:
                return 'convergent argument'
    
    def evaluate_argument_strength(self, argument):
        """
        评估论证强度
        
        Args:
            argument (dict): 论证
            
        Returns:
            str: 论证强度
        """
        premises = argument.get('premises', [])
        conclusion = argument.get('conclusion', '')
        
        # 简单的强度评估
        if not premises or not conclusion:
            return 'weak'
        
        # 检查前提数量
        if len(premises) >= 3:
            return 'strong'
        elif len(premises) >= 2:
            return 'moderate'
        else:
            return 'weak'
    
    def build_argument_graph(self):
        """
        构建论证图谱
        
        Returns:
            networkx.DiGraph: 论证图谱
        """
        if not self.arguments:
            self.extract_arguments()
        
        # 创建有向图
        G = nx.DiGraph()
        
        # 添加节点和边
        for i, argument in enumerate(self.arguments):
            # 添加论证节点
            argument_node = f'Argument {i+1}'
            G.add_node(argument_node, type='argument')
            
            # 添加前提节点
            for j, premise in enumerate(argument['premises']):
                premise_node = f'Premise {i+1}.{j+1}'
                G.add_node(premise_node, type='premise', text=premise)
                G.add_edge(premise_node, argument_node, type='supports')
            
            # 添加结论节点
            if argument['conclusion']:
                conclusion_node = f'Conclusion {i+1}'
                G.add_node(conclusion_node, type='conclusion', text=argument['conclusion'])
                G.add_edge(argument_node, conclusion_node, type='leads_to')
        
        self.argument_graph = G
        return G
    
    def visualize_arguments(self, output_path=None):
        """
        可视化论证结构
        
        Args:
            output_path (str, optional): 输出路径
            
        Returns:
            matplotlib.figure.Figure: 可视化图表
        """
        if not self.argument_graph:
            self.build_argument_graph()
        
        try:
            # 创建图形
            plt.figure(figsize=(12, 8))
            
            # 使用层次布局
            pos = nx.spring_layout(self.argument_graph, k=0.3, iterations=50)
            
            # 绘制节点
            node_types = nx.get_node_attributes(self.argument_graph, 'type')
            node_colors = []
            for node, node_type in node_types.items():
                if node_type == 'argument':
                    node_colors.append('lightblue')
                elif node_type == 'premise':
                    node_colors.append('lightgreen')
                elif node_type == 'conclusion':
                    node_colors.append('lightcoral')
                else:
                    node_colors.append('lightgray')
            
            nx.draw_networkx_nodes(
                self.argument_graph, pos, node_size=3000, node_color=node_colors
            )
            
            # 绘制边
            nx.draw_networkx_edges(
                self.argument_graph, pos, edge_color='gray', arrows=True, arrowstyle='->'
            )
            
            # 绘制标签
            labels = {node: node for node in self.argument_graph.nodes()}
            nx.draw_networkx_labels(
                self.argument_graph, pos, labels=labels, font_size=10
            )
            
            # 设置标题
            plt.title('Argument Structure Visualization')
            plt.axis('off')
            plt.tight_layout()
            
            # 保存图表
            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                print(f"成功保存论证可视化到: {output_path}")
            
            return plt.gcf()
        except Exception as e:
            print(f"可视化论证时出错: {e}")
            return None
    
    def generate_argument_summary(self, argument_index):
        """
        生成论证摘要
        
        Args:
            argument_index (int): 论证索引
            
        Returns:
            str: 论证摘要
        """
        if not self.arguments or argument_index >= len(self.arguments):
            return "论证不存在"
        
        argument = self.arguments[argument_index]
        analysis = self.analyze_argument_structure(argument)
        
        summary = f"论证 {argument_index + 1}:\n"
        summary += "=" * 50 + "\n"
        summary += "前提:\n"
        for i, premise in enumerate(argument['premises']):
            summary += f"  {i+1}. {premise}\n"
        
        if argument['conclusion']:
            summary += "\n结论:\n"
            summary += f"  {argument['conclusion']}\n"
        
        summary += "\n分析:\n"
        summary += f"  推理类型: {analysis['inference_type']}\n"
        summary += f"  逻辑结构: {analysis['logical_structure']}\n"
        summary += f"  论证强度: {analysis['strength']}\n"
        summary += f"  前提数量: {analysis['premise_count']}\n"
        
        return summary
    
    def save_analysis(self, output_path):
        """
        保存分析结果
        
        Args:
            output_path (str): 输出路径
        """
        try:
            if not self.arguments:
                self.extract_arguments()
            
            # 确保输出目录存在
            import os
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 保存分析结果
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("论证分析结果\n")
                f.write("=" * 50 + "\n\n")
                
                for i, argument in enumerate(self.arguments):
                    f.write(self.generate_argument_summary(i))
                    f.write("\n" + "-" * 50 + "\n\n")
            
            print(f"成功保存分析结果到: {output_path}")
        except Exception as e:
            print(f"保存分析结果时出错: {e}")
