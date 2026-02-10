#!/usr/bin/env python3
# 文本语言学分析模块

import re
import string
from collections import Counter
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TextLinguisticsAnalysis:
    """文本语言学分析类"""
    
    def __init__(self, text, language="english"):
        """
        初始化文本语言学分析实例
        
        Args:
            text (str): 要分析的文本
            language (str): 文本语言，默认为"english"
        """
        self.text = text
        self.language = language.lower()
        self.lemmatizer = WordNetLemmatizer()
        
        # 简化版本：移除spaCy依赖
        self.nlp = None
    
    def analyze_text_features(self):
        """
        分析文本的基本特征
        
        Returns:
            dict: 包含文本特征的字典
        """
        # 分词和分句
        words = word_tokenize(self.text)
        sentences = sent_tokenize(self.text)
        
        # 去除标点和停用词
        stop_words = set(stopwords.words(self.language))
        filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
        
        # 计算基本统计信息
        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        lexical_diversity = len(set(filtered_words)) / len(filtered_words) if filtered_words else 0
        
        # 计算可读性指标
        readability = self._calculate_readability()
        
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": avg_sentence_length,
            "lexical_diversity": lexical_diversity,
            "readability": readability
        }
    
    def analyze_style(self):
        """
        分析文本的风格特征
        
        Returns:
            dict: 包含风格特征的字典
        """
        # 简化版本：移除TextBlob依赖，使用基本的情感分析
        # 正面词和负面词列表（简化版）
        positive_words = set(["good", "great", "excellent", "wonderful", "perfect", "happy", "joy", "love", "like", "enjoy"])
        negative_words = set(["bad", "terrible", "awful", "horrible", "sad", "hate", "dislike", "pain", "suffering", "angry"])
        
        # 分析情感
        words = word_tokenize(self.text)
        positive_count = sum(1 for word in words if word.lower() in positive_words)
        negative_count = sum(1 for word in words if word.lower() in negative_words)
        
        total = positive_count + negative_count
        if total > 0:
            polarity = (positive_count - negative_count) / total
        else:
            polarity = 0.0
        
        sentiment = {
            "polarity": polarity,
            "subjectivity": 0.5  # 简化：默认为中性
        }
        
        # 分析正式度
        formality = self._calculate_formality()
        
        # 分析复杂度
        complexity = self._calculate_complexity()
        
        return {
            "formality": formality,
            "complexity": complexity,
            "sentiment": sentiment
        }
    
    def identify_text_type(self):
        """
        识别文本类型
        
        Returns:
            dict: 包含文本类型信息的字典
        """
        # 识别语言
        language = self._identify_language()
        
        # 识别体裁
        genre = self._identify_genre()
        
        # 识别语域
        register = self._identify_register()
        
        return {
            "language": language,
            "genre": genre,
            "register": register
        }
    
    def _calculate_readability(self):
        """
        计算文本的可读性指标
        
        Returns:
            dict: 包含可读性指标的字典
        """
        # 仅支持英语的可读性指标
        if self.language != "english":
            return {"error": "仅支持英语文本的可读性分析"}
        
        # Flesch-Kincaid可读性指数
        words = word_tokenize(self.text)
        sentences = sent_tokenize(self.text)
        
        # 计算音节数（简化版）
        syllable_count = sum(self._count_syllables(word) for word in words if word.isalnum())
        
        # Flesch-Kincaid Grade Level
        if len(words) > 0 and len(sentences) > 0:
            fk_grade = 0.39 * (len(words) / len(sentences)) + 11.8 * (syllable_count / len(words)) - 15.59
        else:
            fk_grade = 0
        
        # Gunning Fog指数
        complex_words = [word for word in words if self._count_syllables(word) >= 3]
        if len(words) > 0 and len(sentences) > 0:
            fog_index = 0.4 * ((len(words) / len(sentences)) + 100 * (len(complex_words) / len(words)))
        else:
            fog_index = 0
        
        return {
            "flesch_kincaid": fk_grade,
            "gunning_fog": fog_index
        }
    
    def _count_syllables(self, word):
        """
        计算单词的音节数（简化版）
        
        Args:
            word (str): 单词
            
        Returns:
            int: 音节数
        """
        word = word.lower()
        vowels = "aeiouy"
        count = 0
        prev_char_was_vowel = False
        
        for char in word:
            if char in vowels:
                if not prev_char_was_vowel:
                    count += 1
                prev_char_was_vowel = True
            else:
                prev_char_was_vowel = False
        
        # 调整：以e结尾的单词通常减少一个音节
        if word.endswith("e") and count > 1:
            count -= 1
        
        return max(1, count)
    
    def _calculate_formality(self):
        """
        计算文本的正式度
        
        Returns:
            float: 正式度分数（0-1）
        """
        # 简化的正式度计算
        formal_words = set(["therefore", "however", "nevertheless", "consequently", "furthermore", "moreover", "hence", "thus", "accordingly", "additionally"])
        informal_words = set(["yeah", "yeah", "gotta", "wanna", "gonna", "lemme", "kinda", "sorta", "ain't", "don't"])
        
        words = word_tokenize(self.text)
        formal_count = sum(1 for word in words if word.lower() in formal_words)
        informal_count = sum(1 for word in words if word.lower() in informal_words)
        
        total = formal_count + informal_count
        if total == 0:
            return 0.5  # 中性
        
        formality = formal_count / total
        return formality
    
    def _calculate_complexity(self):
        """
        计算文本的复杂度
        
        Returns:
            float: 复杂度分数（0-1）
        """
        words = word_tokenize(self.text)
        sentences = sent_tokenize(self.text)
        
        if not words:
            return 0
        
        # 平均句长
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # 长词比例（超过6个字母）
        long_words = [word for word in words if len(word) > 6]
        long_word_ratio = len(long_words) / len(words)
        
        # 复杂度分数（归一化）
        complexity = (min(avg_sentence_length / 20, 1) + long_word_ratio) / 2
        return complexity
    
    def _identify_language(self):
        """
        识别文本的语言
        
        Returns:
            str: 语言名称
        """
        # 简化版本：基于字符特征的语言识别
        text = self.text
        
        # 中文特征：包含中文字符
        if re.search(r'[\u4e00-\u9fff]', text):
            return "chinese"
        
        # 英文特征：主要包含英文字母和常见英文标点
        elif re.search(r'^[a-zA-Z0-9\s.,!?;:"]*$', text.replace('\n', ' ')):
            return "english"
        
        # 其他语言暂不支持
        else:
            return "unknown"
    
    def _identify_genre(self):
        """
        识别文本的体裁
        
        Returns:
            str: 体裁名称
        """
        # 简化的体裁识别
        text_lower = self.text.lower()
        
        # 学术论文特征
        if any(term in text_lower for term in ["abstract", "introduction", "methodology", "results", "discussion", "conclusion", "references"]):
            return "academic"
        
        # 新闻特征
        if any(term in text_lower for term in ["breaking news", "report", "journalist", "source says", "according to"]):
            return "news"
        
        # 小说特征
        if any(term in text_lower for term in ["chapter", "story", "character", "plot", "scene"]):
            return "fiction"
        
        # 散文特征
        if any(term in text_lower for term in ["essay", "reflection", "personal experience", "thoughts"]):
            return "essay"
        
        return "unknown"
    
    def _identify_register(self):
        """
        识别文本的语域
        
        Returns:
            str: 语域名称
        """
        # 简化的语域识别
        text_lower = self.text.lower()
        
        # 正式语域特征
        if any(term in text_lower for term in ["therefore", "however", "nevertheless", "consequently", "furthermore"]):
            return "formal"
        
        # 非正式语域特征
        if any(term in text_lower for term in ["yeah", "gotta", "wanna", "gonna", "lemme"]):
            return "informal"
        
        # 口语特征
        if any(term in text_lower for term in ["you know", "like", "sort of", "kind of", "I mean"]):
            return "colloquial"
        
        return "neutral"
