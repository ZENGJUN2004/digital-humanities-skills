#!/usr/bin/env python3
# 语义学分析模块

from collections import defaultdict
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import spacy
import networkx as nx

class SemanticsAnalysis:
    """语义学分析类"""
    
    def __init__(self, text, language="english"):
        """
        初始化语义学分析实例
        
        Args:
            text (str): 要分析的文本
            language (str): 文本语言，默认为"english"
        """
        self.text = text
        self.language = language.lower()
        self.lemmatizer = WordNetLemmatizer()
        
        # 加载对应的spaCy模型
        self.nlp = None
        try:
            model_map = {
                "english": "en_core_web_sm",
                "chinese": "zh_core_web_sm",
                "french": "fr_core_news_sm",
                "german": "de_core_news_sm",
                "spanish": "es_core_news_sm"
            }
            if self.language in model_map:
                self.nlp = spacy.load(model_map[self.language])
        except Exception as e:
            print(f"警告: 无法加载spaCy模型: {e}")
    
    def analyze_semantic_relations(self):
        """
        分析文本中的语义关系
        
        Returns:
            dict: 包含语义关系的字典
        """
        semantic_relations = {
            "synonymy": [],  # 同义关系
            "antonymy": [],  # 反义关系
            "hyponymy": [],  # 上下义关系
            "meronymy": [],  # 整体部分关系
            "holonymy": [],  # 部分整体关系
            "troponymy": [],  # 动作细化关系
            "causation": []   # 因果关系
        }
        
        # 使用spaCy和WordNet分析语义关系
        if self.nlp:
            try:
                doc = self.nlp(self.text)
                tokens = [token for token in doc if token.is_alpha]
                
                # 分析词对之间的语义关系
                for i, token1 in enumerate(tokens):
                    for token2 in tokens[i+1:]:
                        # 分析同义关系
                        synonyms1 = self._find_synonyms(token1.text)
                        if token2.text in synonyms1:
                            semantic_relations["synonymy"].append((token1.text, token2.text))
                        
                        # 分析反义关系
                        antonyms1 = self._find_antonyms(token1.text)
                        if token2.text in antonyms1:
                            semantic_relations["antonymy"].append((token1.text, token2.text))
                        
                        # 分析上下义关系
                        hyponyms1 = self._find_hyponyms(token1.text)
                        if token2.text in hyponyms1:
                            semantic_relations["hyponymy"].append((token1.text, token2.text))
                        
                        hypernyms1 = self._find_hypernyms(token1.text)
                        if token2.text in hypernyms1:
                            semantic_relations["hyponymy"].append((token2.text, token1.text))
            except Exception as e:
                print(f"语义关系分析失败: {e}")
        
        return semantic_relations
    
    def build_semantic_network(self):
        """
        构建文本的语义网络
        
        Returns:
            nx.Graph: 语义网络图
        """
        G = nx.Graph()
        
        # 使用spaCy分析文本
        if self.nlp:
            try:
                doc = self.nlp(self.text)
                tokens = [token for token in doc if token.is_alpha and len(token.text) > 2]
                
                # 添加节点
                for token in tokens:
                    G.add_node(token.text, pos=token.pos_)
                
                # 添加边（基于共现关系）
                window_size = 3
                for i, token1 in enumerate(tokens):
                    for j in range(max(0, i-window_size), min(len(tokens), i+window_size+1)):
                        if i != j:
                            token2 = tokens[j]
                            if not G.has_edge(token1.text, token2.text):
                                G.add_edge(token1.text, token2.text, weight=1)
                            else:
                                G[token1.text][token2.text]['weight'] += 1
                
                # 添加语义关系边
                semantic_relations = self.analyze_semantic_relations()
                for relation_type, relations in semantic_relations.items():
                    for relation in relations:
                        if len(relation) == 2:
                            word1, word2 = relation
                            if G.has_node(word1) and G.has_node(word2):
                                G.add_edge(word1, word2, relation=relation_type)
            except Exception as e:
                print(f"语义网络构建失败: {e}")
        
        return G
    
    def analyze_frame_semantics(self):
        """
        分析文本的框架语义
        
        Returns:
            dict: 包含框架语义分析结果的字典
        """
        frame_semantics = {
            "frames": [],  # 识别的框架
            "frame_elements": []  # 框架元素
        }
        
        # 简化的框架语义分析
        # 实际应用中可以使用FrameNet或PropBank
        frame_triggers = {
            "motion": ["go", "come", "move", "run", "walk", "travel"],
            "change": ["change", "become", "turn", "transform", "convert"],
            "causation": ["cause", "make", "create", "produce", "generate"],
            "perception": ["see", "hear", "feel", "smell", "taste"],
            "emotion": ["feel", "love", "hate", "like", "dislike", "fear"],
            "communication": ["say", "tell", "speak", "talk", "communicate"],
            "action": ["do", "act", "perform", "execute", "carry out"]
        }
        
        # 识别框架
        text_lower = self.text.lower()
        for frame, triggers in frame_triggers.items():
            for trigger in triggers:
                if trigger in text_lower:
                    frame_semantics["frames"].append(frame)
                    break
        
        # 去重
        frame_semantics["frames"] = list(set(frame_semantics["frames"]))
        
        return frame_semantics
    
    def analyze_conceptual_metaphors(self):
        """
        分析文本中的概念隐喻
        
        Returns:
            list: 概念隐喻列表
        """
        conceptual_metaphors = []
        
        # 简化的概念隐喻识别
        metaphor_patterns = {
            "TIME_IS_MONEY": ["spend time", "waste time", "save time", "invest time", "time is precious"],
            "LOVE_IS_A_JOURNEY": ["relationship is a journey", "we're at a crossroads", "we're on the right track", "we've come a long way"],
            "ARGUMENT_IS_WAR": ["win an argument", "lose an argument", "attack position", "defend position", "shoot down ideas"],
            "IDEAS_ARE_FOOD": ["digest ideas", "swallow ideas", "chew on ideas", "spit out ideas"],
            "MIND_IS_A_COMPUTER": ["process information", "store memories", "retrieve information", "compute answers"]
        }
        
        text_lower = self.text.lower()
        for metaphor, patterns in metaphor_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    conceptual_metaphors.append(metaphor)
                    break
        
        return conceptual_metaphors
    
    def analyze_semantic_roles(self):
        """
        分析文本中的语义角色
        
        Returns:
            list: 语义角色列表
        """
        semantic_roles = []
        
        # 使用spaCy分析语义角色
        if self.nlp:
            try:
                doc = self.nlp(self.text)
                for token in doc:
                    if token.pos_ == "VERB":
                        verb = token.text
                        roles = {
                            "verb": verb,
                            "agent": [],  # 施事
                            "patient": [],  # 受事
                            "theme": [],  # 主题
                            "goal": [],  # 目标
                            "source": [],  # 来源
                            "instrument": [],  # 工具
                            "location": []  # 地点
                        }
                        
                        # 分析依存关系，识别语义角色
                        for child in token.children:
                            if child.dep_ == "nsubj":
                                roles["agent"].append(child.text)
                            elif child.dep_ == "dobj":
                                roles["patient"].append(child.text)
                            elif child.dep_ == "pobj" and child.head.dep_ == "prep":
                                prep = child.head.text
                                if prep in ["to", "toward"]:
                                    roles["goal"].append(child.text)
                                elif prep in ["from", "out of"]:
                                    roles["source"].append(child.text)
                                elif prep in ["with", "using"]:
                                    roles["instrument"].append(child.text)
                                elif prep in ["in", "at", "on", "under"]:
                                    roles["location"].append(child.text)
                        
                        semantic_roles.append(roles)
            except Exception as e:
                print(f"语义角色分析失败: {e}")
        
        return semantic_roles
    
    def _find_synonyms(self, word):
        """
        查找单词的同义词
        
        Args:
            word (str): 单词
            
        Returns:
            list: 同义词列表
        """
        synonyms = set()
        
        try:
            synsets = wordnet.synsets(word)
            for synset in synsets:
                for lemma in synset.lemmas():
                    synonym = lemma.name()
                    if synonym != word:
                        synonyms.add(synonym.replace('_', ' '))
        except Exception:
            pass
        
        return list(synonyms)
    
    def _find_antonyms(self, word):
        """
        查找单词的反义词
        
        Args:
            word (str): 单词
            
        Returns:
            list: 反义词列表
        """
        antonyms = set()
        
        try:
            synsets = wordnet.synsets(word)
            for synset in synsets:
                for lemma in synset.lemmas():
                    if lemma.antonyms():
                        for antonym in lemma.antonyms():
                            antonyms.add(antonym.name().replace('_', ' '))
        except Exception:
            pass
        
        return list(antonyms)
    
    def _find_hyponyms(self, word):
        """
        查找单词的下位词
        
        Args:
            word (str): 单词
            
        Returns:
            list: 下位词列表
        """
        hyponyms = set()
        
        try:
            synsets = wordnet.synsets(word)
            for synset in synsets:
                for hyponym in synset.hyponyms():
                    hyponyms.add(hyponym.name().split('.')[0].replace('_', ' '))
        except Exception:
            pass
        
        return list(hyponyms)
    
    def _find_hypernyms(self, word):
        """
        查找单词的上位词
        
        Args:
            word (str): 单词
            
        Returns:
            list: 上位词列表
        """
        hypernyms = set()
        
        try:
            synsets = wordnet.synsets(word)
            for synset in synsets:
                for hypernym in synset.hypernyms():
                    hypernyms.add(hypernym.name().split('.')[0].replace('_', ' '))
        except Exception:
            pass
        
        return list(hypernyms)
