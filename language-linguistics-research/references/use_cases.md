# 语言与语言学研究技能使用案例

## 1. 文本语言学分析

### 1.1 分析文本特征

**功能说明**：分析文本的基本特征，包括词数、句子数、词汇多样性和可读性。

**使用示例**：

```python
from scripts.text_linguistics_analysis import TextLinguisticsAnalysis

# 读取示例文本
with open('assets/sample_english_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 初始化分析器
analyzer = TextLinguisticsAnalysis()

# 分析文本特征
text_features = analyzer.analyze_text_features(text)
print("文本特征分析结果:")
print(f"词数: {text_features['word_count']}")
print(f"句子数: {text_features['sentence_count']}")
print(f"词汇多样性: {text_features['lexical_diversity']:.2f}")
print(f"平均词长: {text_features['average_word_length']:.2f}")
print(f"平均句长: {text_features['average_sentence_length']:.2f}")
print(f"可读性指数:")
for key, value in text_features['readability'].items():
    print(f"  {key}: {value:.2f}")
```

### 1.2 分析文本风格

**功能说明**：分析文本的风格特征，包括正式性、复杂性和情感倾向。

**使用示例**：

```python
from scripts.text_linguistics_analysis import TextLinguisticsAnalysis

# 读取示例文本
with open('assets/sample_english_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 初始化分析器
analyzer = TextLinguisticsAnalysis()

# 分析文本风格
style_features = analyzer.analyze_style(text)
print("文本风格分析结果:")
print(f"正式性: {style_features['formality']:.2f}")
print(f"复杂性: {style_features['complexity']:.2f}")
print(f"情感倾向: {style_features['sentiment']:.2f}")
```

### 1.3 识别文本类型

**功能说明**：识别文本的语言、体裁和语域。

**使用示例**：

```python
from scripts.text_linguistics_analysis import TextLinguisticsAnalysis

# 读取示例英文文本
with open('assets/sample_english_text.txt', 'r', encoding='utf-8') as f:
    english_text = f.read()

# 读取示例中文文本
with open('assets/sample_chinese_text.txt', 'r', encoding='utf-8') as f:
    chinese_text = f.read()

# 初始化分析器
analyzer = TextLinguisticsAnalysis()

# 识别英文文本类型
english_type = analyzer.identify_text_type(english_text)
print("英文文本类型识别结果:")
print(f"语言: {english_type['language']}")
print(f"体裁: {english_type['genre']}")
print(f"语域: {english_type['register']}")

# 识别中文文本类型
chinese_type = analyzer.identify_text_type(chinese_text)
print("\n中文文本类型识别结果:")
print(f"语言: {chinese_type['language']}")
print(f"体裁: {chinese_type['genre']}")
print(f"语域: {chinese_type['register']}")
```

## 2. 词汇分析

### 2.1 分析词汇形态

**功能说明**：分析单词的形态特征，包括词根、词缀、词性和屈折变化。

**使用示例**：

```python
from scripts.vocabulary_analysis import VocabularyAnalysis

# 初始化分析器
analyzer = VocabularyAnalysis()

# 分析词汇形态
test_words = ['running', 'unhappiness', 'better', 'quickly', 'linguistics']

for word in test_words:
    morphology = analyzer.analyze_morphology(word)
    print(f"\n词汇形态分析 - {word}:")
    print(f"词根: {morphology['root']}")
    print(f"词缀: {morphology['affixes']}")
    print(f"词性: {morphology['part_of_speech']}")
    print(f"屈折变化: {morphology['inflections']}")
```

### 2.2 分析词汇语义

**功能说明**：分析单词的语义特征，包括语义类别、同义词、反义词、上下位词等。

**使用示例**：

```python
from scripts.vocabulary_analysis import VocabularyAnalysis

# 初始化分析器
analyzer = VocabularyAnalysis()

# 分析词汇语义
test_words = ['happy', 'run', 'book', 'computer']

for word in test_words:
    semantics = analyzer.analyze_semantics(word)
    print(f"\n词汇语义分析 - {word}:")
    print(f"语义类别: {semantics['semantic_category']}")
    print(f"同义词: {semantics['synonyms'][:5]}")  # 显示前5个
    print(f"反义词: {semantics['antonyms'][:5]}")  # 显示前5个
    print(f"下位词: {semantics['hyponyms'][:5]}")  # 显示前5个
    print(f"上位词: {semantics['hypernyms'][:5]}")  # 显示前5个
```

## 3. 语法分析

### 3.1 分析短语结构

**功能说明**：分析句子的短语结构，生成成分分析树。

**使用示例**：

```python
from scripts.grammar_analysis import GrammarAnalysis

# 初始化分析器
analyzer = GrammarAnalysis()

# 分析短语结构
test_sentences = [
    "The cat chased the mouse.",
    "She quickly ate the delicious cake."
]

for sentence in test_sentences:
    constituency_tree = analyzer.analyze_constituency(sentence)
    print(f"\n短语结构分析 - {sentence}")
    print(constituency_tree)
```

### 3.2 分析依存关系

**功能说明**：分析句子中单词之间的依存关系。

**使用示例**：

```python
from scripts.grammar_analysis import GrammarAnalysis

# 初始化分析器
analyzer = GrammarAnalysis()

# 分析依存关系
test_sentences = [
    "The cat chased the mouse.",
    "She quickly ate the delicious cake."
]

for sentence in test_sentences:
    dependency_analysis = analyzer.analyze_dependency(sentence)
    print(f"\n依存关系分析 - {sentence}")
    for dep in dependency_analysis:
        print(f"{dep['dependent']} -> {dep['relation']} -> {dep['head']}")
```

## 4. 语义分析

### 4.1 构建语义网络

**功能说明**：基于文本构建语义网络，可视化概念之间的关系。

**使用示例**：

```python
from scripts.semantics_analysis import SemanticsAnalysis

# 初始化分析器
analyzer = SemanticsAnalysis()

# 读取示例文本
with open('assets/sample_english_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 构建语义网络
network = analyzer.build_semantic_network(text)
print("语义网络构建结果:")
print(f"节点数: {network.number_of_nodes()}")
print(f"边数: {network.number_of_edges()}")

# 查看前10个节点
print("\n前10个节点:")
for i, node in enumerate(list(network.nodes())[:10]):
    print(f"{i+1}. {node}")

# 查看前10条边
print("\n前10条边:")
for i, (source, target, data) in enumerate(list(network.edges(data=True))[:10]):
    print(f"{i+1}. {source} -> {target} ({data.get('relation', 'related')})")
```

### 4.2 分析语义角色

**功能说明**：分析句子中名词短语的语义角色，如施事、受事、主题等。

**使用示例**：

```python
from scripts.semantics_analysis import SemanticsAnalysis

# 初始化分析器
analyzer = SemanticsAnalysis()

# 分析语义角色
test_sentences = [
    "John ate the cake with a fork.",
    "Mary gave Peter a book in the library."
]

for sentence in test_sentences:
    semantic_roles = analyzer.analyze_semantic_roles(sentence)
    print(f"\n语义角色分析 - {sentence}")
    for role, entities in semantic_roles.items():
        print(f"{role}: {entities}")
```

## 5. 语用学分析

### 5.1 分析言语行为

**功能说明**：分析对话中的言语行为类型，如断言、指令、承诺等。

**使用示例**：

```python
from scripts.pragmatics_analysis import PragmaticsAnalysis

# 初始化分析器
analyzer = PragmaticsAnalysis()

# 读取示例对话
with open('assets/sample_conversation.txt', 'r', encoding='utf-8') as f:
    conversation = f.read()

# 分析言语行为
speech_acts = analyzer.analyze_speech_acts(conversation)
print("言语行为分析结果:")
for i, act in enumerate(speech_acts):
    print(f"{i+1}. {act['speaker']}: {act['utterance']}")
    print(f"   言语行为类型: {act['speech_act_type']}")
    print(f"   置信度: {act['confidence']:.2f}")
    print()
```

### 5.2 分析对话结构

**功能说明**：分析对话的结构特征，包括轮流发言和相邻对。

**使用示例**：

```python
from scripts.pragmatics_analysis import PragmaticsAnalysis

# 初始化分析器
analyzer = PragmaticsAnalysis()

# 读取示例对话
with open('assets/sample_conversation.txt', 'r', encoding='utf-8') as f:
    conversation = f.read()

# 分析对话结构
conversation_structure = analyzer.analyze_conversation_structure(conversation)
print("对话结构分析结果:")
print(f"总轮数: {len(conversation_structure['turns'])}")
print(f"Alice轮数: {sum(1 for turn in conversation_structure['turns'] if turn['speaker'] == 'Alice')}")
print(f"Bob轮数: {sum(1 for turn in conversation_structure['turns'] if turn['speaker'] == 'Bob')}")
print()
print("相邻对分析:")
for i, pair in enumerate(conversation_structure['adjacency_pairs']):
    print(f"{i+1}. 提问: {pair['first_part']['speaker']}: {pair['first_part']['utterance']}")
    print(f"   回答: {pair['second_part']['speaker']}: {pair['second_part']['utterance']}")
    print()
```

## 6. 历史语言学分析

### 6.1 分析语言变化

**功能说明**：分析语言的历史变化，包括语音变化、形态变化和词汇变化。

**使用示例**：

```python
from scripts.historical_linguistics_analysis import HistoricalLinguisticsAnalysis

# 初始化分析器
analyzer = HistoricalLinguisticsAnalysis()

# 分析语音变化
print("语音变化分析示例:")
print("示例1: 元音大转移")
print("古英语 'mūs' -> 现代英语 'mouse'")
print("示例2: 辅音变化")
print("拉丁语 'pater' -> 法语 'père' -> 英语 'father'")

# 分析词汇变化
print("\n词汇变化分析示例:")
print("语义变化:")
print("'nice' 从古法语的 '无知' 变为现代英语的 '美好'")
print("借词:")
print("英语从法语借入 'restaurant', 'cuisine'")
print("英语从拉丁语借入 'science', 'technology'")

# 分析语言接触
print("\n语言接触分析示例:")
print("英语与其他语言的接触:")
print("- 与法语的接触: 1066年诺曼征服后大量法语词汇进入英语")
print("- 与拉丁语的接触: 文艺复兴时期大量学术词汇进入英语")
print("- 与希腊语的接触: 科学技术词汇的主要来源")
```

### 6.2 构建语言树

**功能说明**：基于语言之间的亲属关系构建语言树。

**使用示例**：

```python
from scripts.historical_linguistics_analysis import HistoricalLinguisticsAnalysis

# 初始化分析器
analyzer = HistoricalLinguisticsAnalysis()

# 构建印欧语系语言树
language_tree = analyzer.build_language_tree()
print("印欧语系语言树构建结果:")
print(f"节点数: {language_tree.number_of_nodes()}")
print(f"边数: {language_tree.number_of_edges()}")

# 查看语言树结构
print("\n语言树结构:")
print("印欧语系")
print("├── 日耳曼语族")
print("│   ├── 英语")
print("│   ├── 德语")
print("│   └── 荷兰语")
print("├── 罗曼语族")
print("│   ├── 法语")
print("│   ├── 西班牙语")
print("│   └── 意大利语")
print("├── 斯拉夫语族")
print("│   ├── 俄语")
print("│   ├── 波兰语")
print("│   └── 捷克语")
print("└── 印度-伊朗语族")
print("    ├── 印地语")
print("    ├── 波斯语")
print("    └── 梵语")
```

## 7. 综合分析示例

### 7.1 完整文本分析流程

**功能说明**：展示完整的文本分析流程，包括文本语言学、词汇、语法、语义和语用学分析。

**使用示例**：

```python
# 完整文本分析流程示例
from scripts.text_linguistics_analysis import TextLinguisticsAnalysis
from scripts.vocabulary_analysis import VocabularyAnalysis
from scripts.grammar_analysis import GrammarAnalysis
from scripts.semantics_analysis import SemanticsAnalysis
from scripts.pragmatics_analysis import PragmaticsAnalysis

# 读取示例文本
with open('assets/sample_english_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print("=== 语言与语言学研究综合分析 ===")
print()

# 1. 文本语言学分析
print("1. 文本语言学分析")
print("-" * 50)
tla = TextLinguisticsAnalysis()
text_features = tla.analyze_text_features(text)
style_features = tla.analyze_style(text)
print(f"词数: {text_features['word_count']}")
print(f"句子数: {text_features['sentence_count']}")
print(f"词汇多样性: {text_features['lexical_diversity']:.2f}")
print(f"正式性: {style_features['formality']:.2f}")
print(f"复杂性: {style_features['complexity']:.2f}")
print()

# 2. 词汇分析
print("2. 词汇分析")
print("-" * 50)
va = VocabularyAnalysis()
# 提取前5个高频词进行分析
high_freq_words = ['language', 'linguistics', 'study', 'analysis', 'computer']
for word in high_freq_words:
    semantics = va.analyze_semantics(word)
    print(f"{word}:")
    print(f"  语义类别: {semantics['semantic_category']}")
    print(f"  同义词: {semantics['synonyms'][:3]}")
print()

# 3. 语法分析
print("3. 语法分析")
print("-" * 50)
ga = GrammarAnalysis()
test_sentence = "Linguistics is the scientific study of language."
dependency_analysis = ga.analyze_dependency(test_sentence)
print(f"句子: {test_sentence}")
print("依存关系:")
for dep in dependency_analysis:
    print(f"  {dep['dependent']} -> {dep['relation']} -> {dep['head']}")
print()

# 4. 语义分析
print("4. 语义分析")
print("-" * 50)
sa = SemanticsAnalysis()
semantic_network = sa.build_semantic_network(text)
print(f"语义网络节点数: {semantic_network.number_of_nodes()}")
print(f"语义网络边数: {semantic_network.number_of_edges()}")
print()

# 5. 语用学分析
print("5. 语用学分析")
print("-" * 50)
print("(使用示例对话进行分析)")
with open('assets/sample_conversation.txt', 'r', encoding='utf-8') as f:
    conversation = f.read()
pa = PragmaticsAnalysis()
speech_acts = pa.analyze_speech_acts(conversation)
print(f"对话中的言语行为数量: {len(speech_acts)}")
print("前3个言语行为:")
for i, act in enumerate(speech_acts[:3]):
    print(f"{i+1}. {act['speaker']}: {act['utterance']}")
    print(f"   类型: {act['speech_act_type']}")
print()

print("=== 分析完成 ===")
```

## 8. 应用场景示例

### 8.1 学术研究应用

**功能说明**：在语言学学术研究中的应用示例。

**使用示例**：

```python
# 学术研究应用示例
print("=== 语言学学术研究应用 ===")
print()
print("1. 文本语料库分析")
print("   - 分析不同时期文本的语言特征变化")
print("   - 比较不同作者的写作风格")
print("   - 研究特定语言现象的分布情况")
print()
print("2. 历史语言学研究")
print("   - 追踪词汇的历史演变")
print("   - 分析语言接触对词汇的影响")
print("   - 构建语言家族树")
print()
print("3. 社会语言学研究")
print("   - 分析不同社会群体的语言变异")
print("   - 研究语言态度和语言政策")
print("   - 调查语言变化的社会因素")
print()
print("4. 计算语言学研究")
print("   - 开发语言模型")
print("   - 研究语义表示方法")
print("   - 构建自然语言处理系统")
```

### 8.2 教育应用

**功能说明**：在语言教育中的应用示例。

**使用示例**：

```python
# 教育应用示例
print("=== 语言教育应用 ===")
print()
print("1. 语言学习辅助")
print("   - 分析学习者的语言产出")
print("   - 提供个性化的语言学习建议")
print("   - 评估语言水平和进步")
print()
print("2. 教学材料分析")
print("   - 分析教材的难度和可读性")
print("   - 评估教材的词汇多样性和覆盖范围")
print("   - 比较不同教材的语言特征")
print()
print("3. 写作教学")
print("   - 分析学生作文的语言特征")
print("   - 提供写作风格改进建议")
print("   - 评估作文的正式性和复杂性")
```

### 8.3 实际应用场景

**功能说明**：在实际工作和生活中的应用示例。

**使用示例**：

```python
# 实际应用场景示例
print("=== 实际应用场景 ===")
print()
print("1. 内容分析")
print("   - 分析社交媒体文本的情感和风格")
print("   - 评估新闻文章的语言特征")
print("   - 分析品牌语言的一致性")
print()
print("2. 翻译和本地化")
print("   - 分析源文本和目标文本的语言特征")
print("   - 评估翻译质量")
print("   - 研究跨语言差异")
print()
print("3. 语言技术开发")
print("   - 构建语言识别系统")
print("   - 开发文本分类系统")
print("   - 研究语义理解技术")
```
