#!/usr/bin/env python3
# 语用学分析模块

import re
from collections import defaultdict
import spacy

class PragmaticsAnalysis:
    """语用学分析类"""
    
    def __init__(self, text, context=None, language="english"):
        """
        初始化语用学分析实例
        
        Args:
            text (str): 要分析的文本
            context (dict, optional): 上下文信息
            language (str, optional): 文本语言，默认为"english"
        """
        self.text = text
        self.context = context or {}
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
    
    def analyze_speech_acts(self):
        """
        分析文本中的言语行为
        
        Returns:
            list: 言语行为列表
        """
        speech_acts = []
        
        # 言语行为类型和特征
        speech_act_patterns = {
            "assertive": {
                "description": "断言类：陈述事实，表达信念",
                "patterns": ["assert", "claim", "state", "affirm", "deny", "report", "describe", "explain"]
            },
            "directive": {
                "description": "指令类：试图让听话人做某事",
                "patterns": ["request", "ask", "order", "command", "beg", "plead", "invite", "suggest", "advise"]
            },
            "commissive": {
                "description": "承诺类：承诺说话人将来做某事",
                "patterns": ["promise", "commit", "pledge", "vow", "guarantee", "swear", "undertake"]
            },
            "expressive": {
                "description": "表达类：表达说话人的情感或态度",
                "patterns": ["thank", "apologize", "congratulate", "condole", "welcome", "greet", "farewell"]
            },
            "declarative": {
                "description": "宣告类：通过说话使某事成为现实",
                "patterns": ["declare", "name", "appoint", "nominate", "christen", "pronounce"]
            }
        }
        
        # 分析文本中的言语行为
        text_lower = self.text.lower()
        for act_type, act_info in speech_act_patterns.items():
            for pattern in act_info["patterns"]:
                if pattern in text_lower:
                    speech_acts.append({
                        "type": act_type,
                        "description": act_info["description"],
                        "evidence": pattern
                    })
                    break
        
        # 使用spaCy进一步分析
        if self.nlp:
            try:
                doc = self.nlp(self.text)
                for token in doc:
                    # 检查是否为祈使句（指令类言语行为）
                    if token.dep_ == "ROOT" and token.pos_ == "VERB" and token.tag_ == "VB":
                        speech_acts.append({
                            "type": "directive",
                            "description": "指令类：试图让听话人做某事",
                            "evidence": token.text
                        })
                    # 检查是否为疑问句（可能是指令类言语行为）
                    elif token.text == "?" or token.tag_ in ["WDT", "WP", "WP$", "WRB"]:
                        speech_acts.append({
                            "type": "directive",
                            "description": "指令类：试图让听话人提供信息",
                            "evidence": token.text
                        })
            except Exception as e:
                print(f"言语行为分析失败: {e}")
        
        return speech_acts
    
    def analyze_implicature(self):
        """
        分析文本中的隐含意义
        
        Returns:
            list: 隐含意义列表
        """
        implicatures = []
        
        # 隐含意义模式
        implicature_patterns = {
            "quantity": {
                "description": "量的准则：提供足够但不过多的信息",
                "examples": ["Some students passed the exam.", "I have three books."]
            },
            "quality": {
                "description": "质的准则：提供真实的信息",
                "examples": ["I think it's going to rain.", "It might be a good idea."]
            },
            "relation": {
                "description": "关系准则：提供相关的信息",
                "examples": ["A: What's the time? B: The postman has just left."]
            },
            "manner": {
                "description": "方式准则：清晰、简洁地表达",
                "examples": ["He is not unattractive.", "I visited the city that never sleeps."]
            }
        }
        
        # 分析文本中的隐含意义
        text_lower = self.text.lower()
        
        # 检查量的准则违反
        if "some" in text_lower or "a few" in text_lower:
            implicatures.append({
                "type": "quantity",
                "description": "量的准则：提供足够但不过多的信息",
                "interpretation": "并非所有"
            })
        
        # 检查质的准则违反
        if "think" in text_lower or "believe" in text_lower or "might" in text_lower or "maybe" in text_lower:
            implicatures.append({
                "type": "quality",
                "description": "质的准则：提供真实的信息",
                "interpretation": "说话人对信息的真实性不确定"
            })
        
        # 检查方式准则违反（间接表达）
        if "not un" in text_lower or "it's a bit cold" in text_lower:
            implicatures.append({
                "type": "manner",
                "description": "方式准则：清晰、简洁地表达",
                "interpretation": "间接表达，可能有隐含意义"
            })
        
        return implicatures
    
    def analyze_politeness(self):
        """
        分析文本的礼貌程度
        
        Returns:
            dict: 礼貌程度分析结果
        """
        politeness = {
            "level": "neutral",  # 礼貌程度：very_polite, polite, neutral, impolite, very_impolite
            "strategies": [],  # 礼貌策略
            "features": []  # 礼貌特征
        }
        
        # 礼貌策略和特征
        polite_features = {
            "greetings": ["hello", "hi", "good morning", "good afternoon", "good evening"],
            "thanking": ["thank you", "thanks", "much obliged", "appreciate"],
            "apologizing": ["sorry", "excuse me", "pardon me", "apologize"],
            "requests": ["please", "could you", "would you", "might I ask", "if you don't mind"],
            "hedging": ["maybe", "perhaps", "sort of", "kind of", "I think", "I believe"],
            "formality": ["sir", "madam", "Mr.", "Mrs.", "Ms.", "Dr.", "Professor"]
        }
        
        impolite_features = {
            "directness": ["you must", "you have to", "do it now", "hurry up"],
            "rudeness": ["stupid", "idiot", "lazy", "useless", "shut up", "get lost"]
        }
        
        text_lower = self.text.lower()
        
        # 分析礼貌特征
        polite_score = 0
        impolite_score = 0
        
        for feature_type, features in polite_features.items():
            for feature in features:
                if feature in text_lower:
                    polite_score += 1
                    politeness["features"].append(f"{feature_type}: {feature}")
        
        for feature_type, features in impolite_features.items():
            for feature in features:
                if feature in text_lower:
                    impolite_score += 1
                    politeness["features"].append(f"{feature_type}: {feature}")
        
        # 确定礼貌程度
        if impolite_score > 2:
            politeness["level"] = "very_impolite"
        elif impolite_score > 0:
            politeness["level"] = "impolite"
        elif polite_score > 3:
            politeness["level"] = "very_polite"
        elif polite_score > 1:
            politeness["level"] = "polite"
        else:
            politeness["level"] = "neutral"
        
        # 识别礼貌策略
        if any(feature in text_lower for feature in polite_features["requests"]):
            politeness["strategies"].append("间接请求")
        if any(feature in text_lower for feature in polite_features["hedging"]):
            politeness["strategies"].append("模糊表达")
        if any(feature in text_lower for feature in polite_features["formality"]):
            politeness["strategies"].append("正式称呼")
        
        return politeness
    
    def analyze_contextual_meanings(self):
        """
        分析文本在具体语境中的意义
        
        Returns:
            dict: 语境意义分析结果
        """
        contextual_meanings = {
            "literal_meanings": [],  # 字面意义
            "contextual_meanings": [],  # 语境意义
            "context_dependent_elements": []  # 依赖语境的元素
        }
        
        # 识别依赖语境的元素
        context_dependent_patterns = {
            "indexicals": {
                "description": "指示词：依赖语境才能确定指称",
                "patterns": ["I", "you", "he", "she", "it", "we", "they", "this", "that", "these", "those", "here", "there", "now", "then", "today", "yesterday", "tomorrow"]
            },
            "deixis": {
                "description": "指示现象：依赖语境才能理解",
                "patterns": ["come", "go", "bring", "take", "left", "right", "up", "down"]
            },
            "presuppositions": {
                "description": "预设：说话人认为听话人已知的信息",
                "patterns": ["stop", "continue", "return", "again", "too", "either", "still"]
            },
            "implicatures": {
                "description": "隐含意义：需要语境推理才能理解",
                "patterns": ["but", "however", "nevertheless", "yet", "although", "despite"]
            }
        }
        
        # 分析依赖语境的元素
        text_lower = self.text.lower()
        for element_type, element_info in context_dependent_patterns.items():
            for pattern in element_info["patterns"]:
                if pattern in text_lower:
                    contextual_meanings["context_dependent_elements"].append({
                        "type": element_type,
                        "description": element_info["description"],
                        "example": pattern
                    })
        
        # 分析字面意义和语境意义
        if self.nlp:
            try:
                doc = self.nlp(self.text)
                for token in doc:
                    if token.is_alpha:
                        contextual_meanings["literal_meanings"].append({
                            "word": token.text,
                            "lemma": token.lemma_,
                            "pos": token.pos_
                        })
            except Exception as e:
                print(f"语境意义分析失败: {e}")
        
        return contextual_meanings
    
    def analyze_conversation_structure(self):
        """
        分析对话结构
        
        Returns:
            dict: 对话结构分析结果
        """
        conversation_structure = {
            "turns": [],  # 话轮
            "adjacency_pairs": [],  # 相邻对
            "preference_organization": [],  # 偏好组织
            "repair": []  # 修复机制
        }
        
        # 分析对话轮次
        turns = re.split(r'[A-Za-z]+:', self.text)
        turns = [turn.strip() for turn in turns if turn.strip()]
        
        for i, turn in enumerate(turns):
            conversation_structure["turns"].append({
                "turn_number": i+1,
                "content": turn
            })
        
        # 分析相邻对
        adjacency_pair_patterns = {
            "greeting-greeting": ["hello", "hi", "good morning"],
            "question-answer": ["what", "when", "where", "who", "why", "how"],
            "request-acceptance": ["can you", "could you", "would you"],
            "offer-acceptance": ["would you like", "do you want"],
            "apology-acceptance": ["sorry", "excuse me"],
            "thank-acknowledgment": ["thank you", "thanks"]
        }
        
        text_lower = self.text.lower()
        for pair_type, patterns in adjacency_pair_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    conversation_structure["adjacency_pairs"].append({
                        "type": pair_type,
                        "evidence": pattern
                    })
        
        return conversation_structure
