#!/usr/bin/env python3
# 历史语言学分析模块

import re
from collections import defaultdict
import networkx as nx

class HistoricalLinguisticsAnalysis:
    """历史语言学分析类"""
    
    def __init__(self, data, language="english"):
        """
        初始化历史语言学分析实例
        
        Args:
            data (dict): 历史语言数据
            language (str): 语言名称，默认为"english"
        """
        self.data = data or {}
        self.language = language.lower()
    
    def analyze_sound_change(self):
        """
        分析语音的历史变化
        
        Returns:
            dict: 语音变化分析结果
        """
        sound_changes = {
            "vowel_shift": [],  # 元音大转移
            "consonant_change": [],  # 辅音变化
            "assimilation": [],  # 同化
            "dissimilation": [],  # 异化
            "epenthesis": [],  # 增音
            "elision": [],  # 省略
            "metathesis": [],  # 换位
            "lenition": [],  # 弱化
            "fortition" : []   # 强化
        }
        
        # 常见语音变化模式
        sound_change_patterns = {
            "vowel_shift": [
                ("iː", "aɪ", "中古英语到现代英语的长i变为ai"),
                ("uː", "aʊ", "中古英语到现代英语的长u变为au"),
                ("eː", "iː", "中古英语到现代英语的长e变为iː"),
                ("oː", "uː", "中古英语到现代英语的长o变为uː")
            ],
            "consonant_change": [
                ("θ", "ð", "清齿擦音变为浊齿擦音"),
                ("ð", "d", "浊齿擦音变为浊齿塞音"),
                ("ɡ", "j", "硬颚塞音变为硬颚近音"),
                ("k", "tʃ", "软颚塞音变为龈颚塞擦音")
            ],
            "assimilation": [
                ("n", "m", "在双唇音前的鼻音同化"),
                ("s", "ʃ", "在硬颚音前的擦音同化"),
                ("t", "ts", "在齿音前的塞音同化")
            ],
            "dissimilation": [
                ("l", "r", "流音异化"),
                ("m", "n", "鼻音异化")
            ],
            "epenthesis": [
                ("", "ə", "插入中元音"),
                ("", "t", "插入塞音")
            ],
            "elision": [
                ("ə", "", "省略中元音"),
                ("t", "", "省略塞音")
            ],
            "metathesis": [
                ("rl", "lr", "流音换位"),
                ("sk", "ks", "塞音+擦音换位")
            ],
            "lenition": [
                ("p", "β", "双唇塞音弱化为双唇擦音"),
                ("t", "ð", "齿塞音弱化为齿擦音"),
                ("k", "ɣ", "软颚塞音弱化为软颚擦音")
            ],
            "fortition": [
                ("β", "b", "双唇擦音强化为双唇塞音"),
                ("ð", "d", "齿擦音强化为齿塞音"),
                ("ɣ", "g", "软颚擦音强化为软颚塞音")
            ]
        }
        
        # 分析语音变化
        if "sound_changes" in self.data:
            for change in self.data["sound_changes"]:
                for change_type, patterns in sound_change_patterns.items():
                    for old_sound, new_sound, description in patterns:
                        if change.get("old_sound") == old_sound and change.get("new_sound") == new_sound:
                            sound_changes[change_type].append({
                                "old_sound": old_sound,
                                "new_sound": new_sound,
                                "description": description,
                                "period": change.get("period", "unknown")
                            })
        
        return sound_changes
    
    def analyze_morphological_change(self):
        """
        分析形态的历史变化
        
        Returns:
            dict: 形态变化分析结果
        """
        morphological_changes = {
            "inflectional": [],  # 屈折变化
            "derivational": [],  # 派生变化
            "compounding": [],   # 复合变化
            "grammaticalization": []  # 语法化
        }
        
        # 分析形态变化
        if "morphological_changes" in self.data:
            for change in self.data["morphological_changes"]:
                change_type = change.get("type", "unknown")
                if change_type in morphological_changes:
                    morphological_changes[change_type].append({
                        "description": change.get("description", ""),
                        "old_form": change.get("old_form", ""),
                        "new_form": change.get("new_form", ""),
                        "period": change.get("period", "unknown")
                    })
        
        return morphological_changes
    
    def analyze_lexical_change(self):
        """
        分析词汇的历史变化
        
        Returns:
            dict: 词汇变化分析结果
        """
        lexical_changes = {
            "semantic_change": [],  # 语义变化
            "borrowing": [],        # 借词
            "neologism": [],        # 新词
            "archaism": []          # 古语
        }
        
        # 语义变化类型
        semantic_change_types = {
            "extension": "语义扩大",
            "narrowing": "语义缩小",
            "amelioration": "语义扬升",
            "pejoration": "语义贬降",
            "metaphor": "隐喻扩展",
            "metonymy": "转喻扩展"
        }
        
        # 分析词汇变化
        if "lexical_changes" in self.data:
            for change in self.data["lexical_changes"]:
                change_type = change.get("type", "unknown")
                if change_type in lexical_changes:
                    lexical_changes[change_type].append({
                        "word": change.get("word", ""),
                        "old_meaning": change.get("old_meaning", ""),
                        "new_meaning": change.get("new_meaning", ""),
                        "period": change.get("period", "unknown"),
                        "source": change.get("source", "unknown")
                    })
        
        return lexical_changes
    
    def analyze_grammatical_change(self):
        """
        分析语法的历史变化
        
        Returns:
            dict: 语法变化分析结果
        """
        grammatical_changes = {
            "syntactic": [],       # 句法变化
            "morphosyntactic": [],  # 形态句法变化
            "functional": []        # 功能变化
        }
        
        # 分析语法变化
        if "grammatical_changes" in self.data:
            for change in self.data["grammatical_changes"]:
                change_type = change.get("type", "unknown")
                if change_type in grammatical_changes:
                    grammatical_changes[change_type].append({
                        "description": change.get("description", ""),
                        "old_pattern": change.get("old_pattern", ""),
                        "new_pattern": change.get("new_pattern", ""),
                        "period": change.get("period", "unknown")
                    })
        
        return grammatical_changes
    
    def identify_cognates(self):
        """
        识别不同语言中的同源词
        
        Returns:
            list: 同源词列表
        """
        cognates = []
        
        # 同源词识别规则
        cognate_patterns = [
            ("p", "f", "格里姆定律：原始印欧语p变为日耳曼语f"),
            ("t", "θ", "格里姆定律：原始印欧语t变为日耳曼语θ"),
            ("k", "h", "格里姆定律：原始印欧语k变为日耳曼语h"),
            ("b", "p", "格里姆定律：原始印欧语b变为日耳曼语p"),
            ("d", "t", "格里姆定律：原始印欧语d变为日耳曼语t"),
            ("g", "k", "格里姆定律：原始印欧语g变为日耳曼语k"),
            ("bh", "b", "格里姆定律：原始印欧语bh变为日耳曼语b"),
            ("dh", "d", "格里姆定律：原始印欧语dh变为日耳曼语d"),
            ("gh", "g", "格里姆定律：原始印欧语gh变为日耳曼语g")
        ]
        
        # 分析同源词
        if "cognates" in self.data:
            for cognate_set in self.data["cognates"]:
                words = cognate_set.get("words", [])
                if len(words) >= 2:
                    # 检查语音对应关系
                    for i, word1 in enumerate(words):
                        for word2 in words[i+1:]:
                            for old_sound, new_sound, description in cognate_patterns:
                                if old_sound in word1.get("form", "") and new_sound in word2.get("form", ""):
                                    cognates.append({
                                        "words": [word1, word2],
                                        "sound_correspondence": f"{old_sound} → {new_sound}",
                                        "rule": description,
                                        "proto_form": cognate_set.get("proto_form", "unknown")
                                    })
        
        return cognates
    
    def build_language_tree(self):
        """
        构建语言的亲属关系树
        
        Returns:
            nx.DiGraph: 语言树
        """
        G = nx.DiGraph()
        
        # 添加语言节点和边
        if "language_family" in self.data:
            family = self.data["language_family"]
            G.add_node(family.get("name", "unknown"), type="family")
            
            # 添加子语言
            if "languages" in family:
                for language in family["languages"]:
                    G.add_node(language.get("name", "unknown"), type="language")
                    G.add_edge(family.get("name", "unknown"), language.get("name", "unknown"))
                    
                    # 添加方言
                    if "dialects" in language:
                        for dialect in language["dialects"]:
                            G.add_node(dialect.get("name", "unknown"), type="dialect")
                            G.add_edge(language.get("name", "unknown"), dialect.get("name", "unknown"))
        
        return G
    
    def analyze_language_contact(self):
        """
        分析语言接触现象
        
        Returns:
            dict: 语言接触分析结果
        """
        language_contact = {
            "borrowing": [],        # 借词
            "code_switching": [],   # 语码转换
            "pidginization": [],    # 洋泾浜化
            "creolization": [],     # 克里奥尔化
            "language_shift": [],   # 语言转换
            "language_death": []    # 语言死亡
        }
        
        # 分析语言接触
        if "language_contact" in self.data:
            for contact in self.data["language_contact"]:
                contact_type = contact.get("type", "unknown")
                if contact_type in language_contact:
                    language_contact[contact_type].append({
                        "description": contact.get("description", ""),
                        "languages": contact.get("languages", []),
                        "period": contact.get("period", "unknown"),
                        "outcome": contact.get("outcome", "unknown")
                    })
        
        return language_contact
