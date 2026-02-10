#!/usr/bin/env python3
# 词汇学分析模块

import re
from collections import Counter
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

class VocabularyAnalysis:
    """词汇学分析类"""
    
    def __init__(self, vocabulary, language="english"):
        """
        初始化词汇学分析实例
        
        Args:
            vocabulary (list): 要分析的词汇列表
            language (str): 词汇语言，默认为"english"
        """
        self.vocabulary = vocabulary
        self.language = language.lower()
        self.lemmatizer = WordNetLemmatizer()
        
        # 简化版本：移除spaCy依赖
        self.nlp = None
    
    def analyze_morphology(self):
        """
        分析词汇的形态结构
        
        Returns:
            dict: 包含词汇形态分析结果的字典
        """
        morphology_analysis = {}
        
        for word in self.vocabulary:
            # 分析词形
            analysis = {
                "root": self._extract_root(word),
                "affixes": self._extract_affixes(word),
                "part_of_speech": self._identify_part_of_speech(word),
                "inflections": self._identify_inflections(word)
            }
            morphology_analysis[word] = analysis
        
        return morphology_analysis
    
    def analyze_semantics(self):
        """
        分析词汇的语义
        
        Returns:
            dict: 包含词汇语义分析结果的字典
        """
        semantics_analysis = {}
        
        for word in self.vocabulary:
            # 分析语义
            analysis = {
                "semantic_category": self._identify_semantic_category(word),
                "synonyms": self._find_synonyms(word),
                "antonyms": self._find_antonyms(word),
                "hyponyms": self._find_hyponyms(word),
                "hypernyms": self._find_hypernyms(word),
                "meronyms": self._find_meronyms(word),
                "holonyms": self._find_holonyms(word)
            }
            semantics_analysis[word] = analysis
        
        return semantics_analysis
    
    def analyze_vocabulary_features(self):
        """
        分析词汇集合的特征
        
        Returns:
            dict: 包含词汇集合特征的字典
        """
        # 计算词汇长度分布
        word_lengths = [len(word) for word in self.vocabulary]
        length_counter = Counter(word_lengths)
        
        # 计算词类分布
        pos_distribution = Counter()
        for word in self.vocabulary:
            pos = self._identify_part_of_speech(word)
            pos_distribution[pos] += 1
        
        # 计算词缀分布
        prefix_counter = Counter()
        suffix_counter = Counter()
        for word in self.vocabulary:
            affixes = self._extract_affixes(word)
            for prefix in affixes.get("prefixes", []):
                prefix_counter[prefix] += 1
            for suffix in affixes.get("suffixes", []):
                suffix_counter[suffix] += 1
        
        return {
            "total_words": len(self.vocabulary),
            "unique_words": len(set(self.vocabulary)),
            "avg_word_length": sum(word_lengths) / len(word_lengths) if word_lengths else 0,
            "length_distribution": dict(length_counter),
            "pos_distribution": dict(pos_distribution),
            "prefix_distribution": dict(prefix_counter.most_common(10)),
            "suffix_distribution": dict(suffix_counter.most_common(10))
        }
    
    def _extract_root(self, word):
        """
        提取单词的词根
        
        Args:
            word (str): 单词
            
        Returns:
            str: 词根
        """
        # 使用WordNetLemmatizer提取词根
        # 注意：这是一个简化的方法，实际的词根提取可能更复杂
        lemma = self.lemmatizer.lemmatize(word)
        return lemma
    
    def _extract_affixes(self, word):
        """
        提取单词的词缀
        
        Args:
            word (str): 单词
            
        Returns:
            dict: 包含前缀和后缀的字典
        """
        # 常见前缀和后缀
        prefixes = set(["un", "re", "in", "im", "il", "ir", "dis", "en", "em", "non", "pre", "post", "anti", "auto", "bi", "co", "de", "ex", "inter", "intra", "micro", "mid", "mis", "over", "poly", "sub", "super", "tele", "trans", "under", "uni"])
        suffixes = set(["s", "es", "ed", "ing", "ly", "er", "est", "ment", "ness", "ity", "ty", "al", "ial", "ic", "ical", "ful", "less", "ous", "eous", "ious", "ive", "ative", "itive", "able", "ible", "y", "en", "ify", "fy", "ize", "ise"])
        
        found_prefixes = []
        found_suffixes = []
        
        # 提取前缀
        for prefix in sorted(prefixes, key=len, reverse=True):
            if word.startswith(prefix):
                found_prefixes.append(prefix)
                word = word[len(prefix):]
        
        # 提取后缀
        for suffix in sorted(suffixes, key=len, reverse=True):
            if word.endswith(suffix):
                found_suffixes.append(suffix)
                word = word[:-len(suffix)]
        
        return {
            "prefixes": found_prefixes,
            "suffixes": found_suffixes
        }
    
    def _identify_part_of_speech(self, word):
        """
        识别单词的词性
        
        Args:
            word (str): 单词
            
        Returns:
            str: 词性
        """
        # 使用WordNet识别词性
        try:
            synsets = wordnet.synsets(word)
            if synsets:
                pos = synsets[0].pos()
                pos_map = {
                    "n": "NOUN",
                    "v": "VERB",
                    "a": "ADJ",
                    "r": "ADV"
                }
                return pos_map.get(pos, "UNKNOWN")
        except Exception:
            pass
        
        return "UNKNOWN"
    
    def _identify_inflections(self, word):
        """
        识别单词的屈折变化
        
        Args:
            word (str): 单词
            
        Returns:
            list: 屈折变化类型
        """
        inflections = []
        
        # 检查复数形式
        if word.endswith("s") and not word.endswith("ss"):
            inflections.append("plural")
        
        # 检查过去式
        if word.endswith("ed"):
            inflections.append("past_tense")
        
        # 检查现在分词
        if word.endswith("ing"):
            inflections.append("present_participle")
        
        # 检查比较级
        if word.endswith("er"):
            inflections.append("comparative")
        
        # 检查最高级
        if word.endswith("est"):
            inflections.append("superlative")
        
        return inflections
    
    def _identify_semantic_category(self, word):
        """
        识别单词的语义类别
        
        Args:
            word (str): 单词
            
        Returns:
            str: 语义类别
        """
        # 简化的语义类别识别
        categories = {
            "person": ["man", "woman", "child", "person", "people", "human"],
            "animal": ["dog", "cat", "bird", "fish", "animal"],
            "plant": ["tree", "flower", "plant", "grass", "leaf"],
            "object": ["table", "chair", "book", "pen", "computer"],
            "action": ["run", "walk", "eat", "drink", "write"],
            "quality": ["good", "bad", "happy", "sad", "big", "small"],
            "quantity": ["one", "two", "three", "many", "few", "some"],
            "time": ["time", "day", "night", "year", "month", "hour"],
            "space": ["space", "place", "location", "position", "distance"],
            "abstract": ["love", "hate", "truth", "beauty", "freedom"]
        }
        
        # 使用WordNet查找语义类别
        try:
            synsets = wordnet.synsets(word)
            if synsets:
                # 获取最常见的语义类别
                for category, keywords in categories.items():
                    for keyword in keywords:
                        keyword_synsets = wordnet.synsets(keyword)
                        for synset in synsets:
                            for keyword_synset in keyword_synsets:
                                if synset.wup_similarity(keyword_synset) and synset.wup_similarity(keyword_synset) > 0.8:
                                    return category
        except Exception:
            pass
        
        return "unknown"
    
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
        
        return list(synonyms)[:10]  # 限制返回数量
    
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
        
        return list(antonyms)[:10]  # 限制返回数量
    
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
        
        return list(hyponyms)[:10]  # 限制返回数量
    
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
        
        return list(hypernyms)[:10]  # 限制返回数量
    
    def _find_meronyms(self, word):
        """
        查找单词的部分词
        
        Args:
            word (str): 单词
            
        Returns:
            list: 部分词列表
        """
        meronyms = set()
        
        try:
            synsets = wordnet.synsets(word)
            for synset in synsets:
                for meronym in synset.part_meronyms():
                    meronyms.add(meronym.name().split('.')[0].replace('_', ' '))
        except Exception:
            pass
        
        return list(meronyms)[:10]  # 限制返回数量
    
    def _find_holonyms(self, word):
        """
        查找单词的整体词
        
        Args:
            word (str): 单词
            
        Returns:
            list: 整体词列表
        """
        holonyms = set()
        
        try:
            synsets = wordnet.synsets(word)
            for synset in synsets:
                for holonym in synset.part_holonyms():
                    holonyms.add(holonym.name().split('.')[0].replace('_', ' '))
        except Exception:
            pass
        
        return list(holonyms)[:10]  # 限制返回数量
