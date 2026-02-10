#!/usr/bin/env python3
# 语法学分析模块

import re
from nltk.tokenize import word_tokenize
from nltk.parse import CoreNLPParser
import spacy

class GrammarAnalysis:
    """语法学分析类"""
    
    def __init__(self, sentence, language="english"):
        """
        初始化语法学分析实例
        
        Args:
            sentence (str): 要分析的句子
            language (str): 句子语言，默认为"english"
        """
        self.sentence = sentence
        self.language = language.lower()
        
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
        
        # 初始化CoreNLP解析器（备选）
        self.parser = None
        self.dep_parser = None
        try:
            self.parser = CoreNLPParser(url='http://localhost:9000')
            self.dep_parser = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
        except Exception as e:
            print(f"警告: 无法初始化CoreNLP解析器: {e}")
    
    def analyze_constituency(self):
        """
        分析句子的短语结构
        
        Returns:
            str: 短语结构树
        """
        # 使用spaCy进行短语结构分析
        if self.nlp:
            try:
                doc = self.nlp(self.sentence)
                return self._format_constituency_tree(doc)
            except Exception as e:
                print(f"spaCy短语结构分析失败: {e}")
        
        # 使用CoreNLP作为备选
        if self.parser:
            try:
                parse_trees = list(self.parser.parse(self.sentence.split()))
                if parse_trees:
                    return str(parse_trees[0])
            except Exception as e:
                print(f"CoreNLP短语结构分析失败: {e}")
        
        # 简化的短语结构分析
        return self._simplified_constituency_analysis()
    
    def analyze_dependency(self):
        """
        分析句子的依存关系
        
        Returns:
            list: 依存关系列表
        """
        dependencies = []
        
        # 使用spaCy进行依存关系分析
        if self.nlp:
            try:
                doc = self.nlp(self.sentence)
                for token in doc:
                    dependency = {
                        "form": token.text,
                        "lemma": token.lemma_,
                        "pos": token.pos_,
                        "dep": token.dep_,
                        "head": token.head.text,
                        "head_pos": token.head.pos_,
                        "children": [child.text for child in token.children]
                    }
                    dependencies.append(dependency)
                return dependencies
            except Exception as e:
                print(f"spaCy依存关系分析失败: {e}")
        
        # 使用CoreNLP作为备选
        if self.dep_parser:
            try:
                parse_result = list(self.dep_parser.raw_parse(self.sentence))
                if parse_result:
                    for governor, dep, dependent in parse_result[0].triples():
                        dependency = {
                            "form": dependent[0],
                            "lemma": dependent[0],
                            "pos": dependent[1],
                            "dep": dep,
                            "head": governor[0],
                            "head_pos": governor[1],
                            "children": []
                        }
                        dependencies.append(dependency)
                    return dependencies
            except Exception as e:
                print(f"CoreNLP依存关系分析失败: {e}")
        
        return dependencies
    
    def analyze_constituents(self):
        """
        分析句子的成分
        
        Returns:
            dict: 包含句子成分的字典
        """
        constituents = {
            "subject": [],
            "predicate": [],
            "object": [],
            "adverbial": [],
            "adjective": []
        }
        
        # 使用spaCy进行成分分析
        if self.nlp:
            try:
                doc = self.nlp(self.sentence)
                for token in doc:
                    # 识别主语（nsubj, nsubjpass）
                    if token.dep_ in ['nsubj', 'nsubjpass']:
                        constituents["subject"].append(token.text)
                    # 识别谓语（ROOT, VERB）
                    elif token.dep_ == 'ROOT' or token.pos_ == 'VERB':
                        constituents["predicate"].append(token.text)
                    # 识别宾语（dobj, pobj, attr）
                    elif token.dep_ in ['dobj', 'pobj', 'attr']:
                        constituents["object"].append(token.text)
                    # 识别状语（advmod, prep）
                    elif token.dep_ in ['advmod', 'prep']:
                        constituents["adverbial"].append(token.text)
                    # 识别定语（amod）
                    elif token.dep_ == 'amod':
                        constituents["adjective"].append(token.text)
            except Exception as e:
                print(f"spaCy成分分析失败: {e}")
        
        return constituents
    
    def analyze_sentence_pattern(self):
        """
        分析句子的句型
        
        Returns:
            str: 句型
        """
        # 检查是否为疑问句
        if any(pattern in self.sentence for pattern in ['?', 'what', 'when', 'where', 'who', 'why', 'how', 'do ', 'does ', 'did ', 'is ', 'are ', 'was ', 'were ', 'have ', 'has ', 'had ']):
            return "interrogative"
        
        # 检查是否为祈使句
        if self.sentence.strip().endswith('!') or self.sentence.strip().startswith(('please', 'let', 'don\'t', 'do not')):
            return "imperative"
        
        # 检查是否为感叹句
        if self.sentence.strip().endswith('!') or any(word in self.sentence.lower() for word in ['what a', 'how', 'wow', 'amazing', 'fantastic']):
            return "exclamatory"
        
        # 陈述句
        return "declarative"
    
    def analyze_morphology(self):
        """
        分析句子中单词的形态
        
        Returns:
            dict: 包含单词形态分析的字典
        """
        morphology = {}
        
        # 使用spaCy进行形态分析
        if self.nlp:
            try:
                doc = self.nlp(self.sentence)
                for token in doc:
                    morphology[token.text] = {
                        "lemma": token.lemma_,
                        "pos": token.pos_,
                        "tag": token.tag_,
                        "morph": token.morph.to_dict()
                    }
            except Exception as e:
                print(f"spaCy形态分析失败: {e}")
        
        return morphology
    
    def _format_constituency_tree(self, doc):
        """
        格式化spaCy的分析结果为短语结构树
        
        Args:
            doc: spaCy文档对象
            
        Returns:
            str: 短语结构树
        """
        # 简化的短语结构树格式化
        def build_tree(token, indent=0):
            prefix = "  " * indent
            children = list(token.children)
            if children:
                tree = f"{prefix}({token.pos_} {token.text}\n"
                for child in children:
                    tree += build_tree(child, indent + 1)
                tree += f"{prefix})"
            else:
                tree = f"{prefix}({token.pos_} {token.text})"
            return tree
        
        root = [token for token in doc if token.dep_ == 'ROOT'][0]
        return build_tree(root)
    
    def _simplified_constituency_analysis(self):
        """
        简化的短语结构分析
        
        Returns:
            str: 简化的短语结构树
        """
        # 非常简化的短语结构分析
        words = word_tokenize(self.sentence)
        if not words:
            return "(S)"
        
        # 简单的NP-VP结构
        tree = "(S\n"
        
        # 假设前半部分是NP（名词短语），后半部分是VP（动词短语）
        mid_point = len(words) // 2
        
        tree += f"  (NP {' '.join(words[:mid_point])})\n"
        tree += f"  (VP {' '.join(words[mid_point:])})\n"
        tree += ")"
        
        return tree
