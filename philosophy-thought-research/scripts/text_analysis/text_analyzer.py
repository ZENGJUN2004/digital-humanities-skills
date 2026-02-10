#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文本分析工具
用于哲学文本的分析、概念提取、论证分析
"""

import os
import re
import nltk
import networkx as nx
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter, defaultdict

# 初始化全局变量
has_spacy = False
spacy = None
has_textblob = False
TextBlob = None
has_gensim = False
corpora = None
models = None

# 延迟导入函数
def import_spacy():
    """
    尝试导入spacy
    """
    global has_spacy, spacy
    try:
        import spacy
        has_spacy = True
    except ImportError as e:
        print(f"导入spacy时出错: {e}")
        print("spaCy功能将不可用，但其他功能仍然可以使用")
        has_spacy = False
        spacy = None

def import_textblob():
    """
    尝试导入textblob
    """
    global has_textblob, TextBlob
    try:
        from textblob import TextBlob
        has_textblob = True
    except ImportError as e:
        print(f"导入textblob时出错: {e}")
        print("TextBlob功能将不可用，但其他功能仍然可以使用")
        has_textblob = False
        TextBlob = None

def import_gensim():
    """
    尝试导入gensim
    """
    global has_gensim, corpora, models
    try:
        from gensim import corpora, models
        has_gensim = True
    except ImportError as e:
        print(f"导入gensim时出错: {e}")
        print("Gensim功能将不可用，但其他功能仍然可以使用")
        has_gensim = False
        corpora = None
        models = None

class TextAnalyzer:
    """
    文本分析器类
    """
    
    def __init__(self, text_path=None, text_content=None):
        """
        初始化文本分析器
        
        Args:
            text_path (str, optional): 文本文件路径
            text_content (str, optional): 文本内容
        """
        self.text_path = text_path
        self.text_content = text_content
        self.text = None
        self.sentences = []
        self.tokens = []
        self.lemmatized_tokens = []
        self.named_entities = []
        
        # 加载NLTK资源
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            print(f"加载NLTK资源时出错: {e}")
        
        # 延迟导入可选模块
        import_spacy()
        import_textblob()
        import_gensim()
        
        # 加载spaCy模型
        self.nlp = None
        if has_spacy:
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except Exception as e:
                print(f"加载spaCy模型时出错: {e}")
                print("spaCy功能将不可用，但其他功能仍然可以使用")
                self.nlp = None
        else:
            print("spaCy未导入，相关功能将不可用")
        
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
        处理文本，进行分词、词性标注等
        """
        if not self.text:
            return
        
        # 分句
        self.sentences = sent_tokenize(self.text)
        
        # 分词
        self.tokens = word_tokenize(self.text)
        
        # 去除停用词和标点
        stop_words = set(stopwords.words('english'))
        self.tokens = [token for token in self.tokens if token.isalpha() and token.lower() not in stop_words]
        
        # 词形还原
        lemmatizer = WordNetLemmatizer()
        self.lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in self.tokens]
        
        # 命名实体识别
        if self.nlp:
            doc = self.nlp(self.text)
            self.named_entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    def analyze(self):
        """
        分析文本
        
        Returns:
            dict: 文本分析结果
        """
        if not self.text:
            return {"error": "文本未加载"}
        
        analysis = {
            "keywords": self.extract_keywords(),
            "topics": self.extract_topics(),
            "sentiment": self.analyze_sentiment(),
            "word_frequency": self.calculate_word_frequency(),
            "sentence_count": len(self.sentences),
            "token_count": len(self.tokens),
            "unique_tokens": len(set(self.lemmatized_tokens)),
            "named_entities": self.named_entities[:10]  # 只返回前10个命名实体
        }
        
        return analysis
    
    def extract_keywords(self, top_n=20):
        """
        提取关键词
        
        Args:
            top_n (int): 返回前n个关键词
            
        Returns:
            list: 关键词列表
        """
        # 计算词频
        word_freq = Counter(self.lemmatized_tokens)
        
        # 返回前n个高频词
        return [(word, freq) for word, freq in word_freq.most_common(top_n)]
    
    def extract_concepts(self, top_n=20):
        """
        提取概念
        
        Args:
            top_n (int): 返回前n个概念
            
        Returns:
            list: 概念列表
        """
        # 这里使用关键词作为概念的近似
        # 实际应用中可以使用更复杂的概念提取算法
        keywords = self.extract_keywords(top_n)
        return [word for word, freq in keywords]
    
    def extract_topics(self, num_topics=5, num_words=10):
        """
        提取主题
        
        Args:
            num_topics (int): 主题数量
            num_words (int): 每个主题的词数
            
        Returns:
            list: 主题列表
        """
        if not has_gensim:
            print("Gensim未导入，主题提取功能不可用")
            return []
        
        try:
            # 准备语料库
            texts = [self.lemmatized_tokens]
            dictionary = corpora.Dictionary(texts)
            corpus = [dictionary.doc2bow(text) for text in texts]
            
            # 训练LDA模型
            lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
            
            # 提取主题
            topics = []
            for topic_id, topic in lda_model.print_topics(num_words=num_words):
                # 解析主题词
                topic_words = re.findall(r'"(.*?)"', topic)
                topics.append({
                    "topic_id": topic_id,
                    "words": topic_words
                })
            
            return topics
        except Exception as e:
            print(f"提取主题时出错: {e}")
            return []
    
    def analyze_sentiment(self):
        """
        分析情感
        
        Returns:
            dict: 情感分析结果
        """
        if not has_textblob:
            print("TextBlob未导入，情感分析功能不可用")
            return {"polarity": 0.0, "subjectivity": 0.0}
        
        try:
            blob = TextBlob(self.text)
            sentiment = blob.sentiment
            
            return {
                "polarity": sentiment.polarity,  # -1到1之间的情感极性
                "subjectivity": sentiment.subjectivity  # 0到1之间的主观性
            }
        except Exception as e:
            print(f"情感分析时出错: {e}")
            return {"polarity": 0.0, "subjectivity": 0.0}
    
    def calculate_word_frequency(self):
        """
        计算词频
        
        Returns:
            dict: 词频字典
        """
        return dict(Counter(self.lemmatized_tokens))
    
    def build_semantic_network(self, window_size=5):
        """
        构建语义网络
        
        Args:
            window_size (int): 窗口大小
            
        Returns:
            networkx.Graph: 语义网络
        """
        try:
            # 创建图
            G = nx.Graph()
            
            # 计算共现
            co_occurrence = defaultdict(int)
            
            # 滑动窗口计算共现
            for i in range(len(self.lemmatized_tokens) - window_size + 1):
                window = self.lemmatized_tokens[i:i+window_size]
                # 计算窗口内词的共现
                for j in range(len(window)):
                    for k in range(j+1, len(window)):
                        word1, word2 = window[j], window[k]
                        if word1 != word2:
                            # 确保词对的顺序一致
                            if word1 > word2:
                                word1, word2 = word2, word1
                            co_occurrence[(word1, word2)] += 1
            
            # 添加节点和边
            for (word1, word2), weight in co_occurrence.items():
                # 只添加权重大于1的边
                if weight > 1:
                    # 添加节点
                    if word1 not in G:
                        G.add_node(word1)
                    if word2 not in G:
                        G.add_node(word2)
                    # 添加边
                    G.add_edge(word1, word2, weight=weight)
            
            return G
        except Exception as e:
            print(f"构建语义网络时出错: {e}")
            return nx.Graph()
    
    def analyze_semantic_network(self, network=None):
        """
        分析语义网络
        
        Args:
            network (networkx.Graph, optional): 语义网络
            
        Returns:
            dict: 网络分析结果
        """
        if network is None:
            network = self.build_semantic_network()
        
        try:
            # 计算网络统计信息
            stats = {
                "nodes": network.number_of_nodes(),
                "edges": network.number_of_edges(),
                "density": nx.density(network),
                "average_clustering": nx.average_clustering(network),
                "average_degree": sum(dict(network.degree()).values()) / network.number_of_nodes() if network.number_of_nodes() > 0 else 0,
                "centrality": self.calculate_centrality(network)
            }
            
            return stats
        except Exception as e:
            print(f"分析语义网络时出错: {e}")
            return {}
    
    def calculate_centrality(self, network, top_n=10):
        """
        计算中心性
        
        Args:
            network (networkx.Graph): 语义网络
            top_n (int): 返回前n个节点
            
        Returns:
            dict: 中心性分析结果
        """
        try:
            # 度中心性
            degree_centrality = nx.degree_centrality(network)
            top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]
            
            # 中介中心性
            betweenness_centrality = nx.betweenness_centrality(network)
            top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]
            
            # 接近中心性
            closeness_centrality = nx.closeness_centrality(network)
            top_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]
            
            return {
                "degree_centrality": top_degree,
                "betweenness_centrality": top_betweenness,
                "closeness_centrality": top_closeness
            }
        except Exception as e:
            print(f"计算中心性时出错: {e}")
            return {}
    
    def find_concept_relations(self, concept, network=None):
        """
        查找概念的关系
        
        Args:
            concept (str): 概念
            network (networkx.Graph, optional): 语义网络
            
        Returns:
            list: 概念关系列表
        """
        if network is None:
            network = self.build_semantic_network()
        
        try:
            # 查找与概念直接相连的节点
            neighbors = list(network.neighbors(concept))
            
            # 构建关系列表
            relations = []
            for neighbor in neighbors:
                weight = network[concept][neighbor].get('weight', 1)
                relations.append({
                    "related_concept": neighbor,
                    "strength": weight
                })
            
            # 按关系强度排序
            relations.sort(key=lambda x: x['strength'], reverse=True)
            
            return relations
        except Exception as e:
            print(f"查找概念关系时出错: {e}")
            return []
    
    def generate_concept_summary(self, concept, max_sentences=3):
        """
        生成概念摘要
        
        Args:
            concept (str): 概念
            max_sentences (int): 最大句子数
            
        Returns:
            str: 概念摘要
        """
        try:
            # 查找包含概念的句子
            concept_sentences = []
            for sentence in self.sentences:
                if concept.lower() in sentence.lower():
                    concept_sentences.append(sentence)
                    if len(concept_sentences) >= max_sentences:
                        break
            
            # 合并句子
            summary = ' '.join(concept_sentences)
            return summary
        except Exception as e:
            print(f"生成概念摘要时出错: {e}")
            return ""
    
    def save_analysis(self, output_path):
        """
        保存分析结果
        
        Args:
            output_path (str): 输出路径
        """
        try:
            analysis = self.analyze()
            
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 保存为文本文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("文本分析结果\n")
                f.write("="*50 + "\n")
                
                f.write(f"句子数: {analysis['sentence_count']}\n")
                f.write(f"词数: {analysis['token_count']}\n")
                f.write(f"唯一词数: {analysis['unique_tokens']}\n")
                f.write(f"情感极性: {analysis['sentiment']['polarity']}\n")
                f.write(f"主观性: {analysis['sentiment']['subjectivity']}\n\n")
                
                f.write("关键词:\n")
                for word, freq in analysis['keywords']:
                    f.write(f"  {word}: {freq}\n")
                
                f.write("\n主题:\n")
                for topic in analysis['topics']:
                    f.write(f"  主题 {topic['topic_id']}: {', '.join(topic['words'])}\n")
                
                f.write("\n命名实体:\n")
                for entity, label in analysis['named_entities']:
                    f.write(f"  {entity} ({label})\n")
            
            print(f"成功保存分析结果到: {output_path}")
        except Exception as e:
            print(f"保存分析结果时出错: {e}")
