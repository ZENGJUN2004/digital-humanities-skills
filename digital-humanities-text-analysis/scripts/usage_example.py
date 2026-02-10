#!/usr/bin/env python3
"""
Usage example for Digital Humanities Text Analysis skill
Demonstrates how to analyze a literary text using the TextMining class
"""

from text_mining import TextMining
import os

# Load the sample literary text
asset_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
sample_text_path = os.path.join(asset_dir, 'sample_literary_text.txt')

with open(sample_text_path, 'r', encoding='utf-8') as f:
    sample_text = f.read()

print("=== Digital Humanities Text Analysis Example ===")
print("Analyzing Hamlet's Soliloquy: 'To be, or not to be'")
print("=" * 60)

# Initialize TextMining
miner = TextMining(sample_text)

print("\n1. Text Statistics")
print("-" * 40)
stats = miner.text_statistics()
print(f"Word count: {stats['word_count']}")
print(f"Sentence count: {stats['sentence_count']}")
print(f"Average words per sentence: {stats['avg_words_per_sentence']:.2f}")
print(f"Lexical diversity: {stats['lexical_diversity']:.3f}")
print(f"Most common words:")
for word, count in stats['most_common_words'][:5]:
    print(f"  - {word}: {count}")

print("\n2. Keyword Extraction")
print("-" * 40)
keywords = miner.extract_keywords(n=10)
print("Top keywords:")
for keyword, score in keywords:
    print(f"  - {keyword}: {score:.3f}")

print("\n3. Sentiment Analysis")
print("-" * 40)
sentiment = miner.sentiment_analysis()
print(f"Polarity: {sentiment['polarity']:.3f}")
print(f"Subjectivity: {sentiment['subjectivity']:.3f}")
print(f"Sentiment: {sentiment['sentiment']}")

print("\n4. Topic Modeling")
print("-" * 40)
topics = miner.topic_modeling(n_topics=3, n_words=5, method='lda')
print("Detected topics:")
for topic in topics:
    print(f"  Topic {topic['topic_id']}: {', '.join(topic['top_words'])}")

print("\n5. Readability Scores")
print("-" * 40)
readability = miner.readability_scores()
print(f"Average sentence length: {readability['avg_sentence_length']:.2f}")
print(f"Percent complex words: {readability['percent_complex_words']:.3f}")
print(f"Flesch-Kincaid grade level: {readability['flesch_kincaid_grade_level']:.2f}")

print("\n6. Entity Extraction")
print("-" * 40)
entities = miner.extract_entities()
print("Extracted entities:")
for entity, count in entities[:10]:
    print(f"  - {entity}: {count}")

print("\n=== Analysis Complete ===")
print("This example demonstrates how the Digital Humanities Text Analysis skill")
print("can be used to analyze literary texts, extract insights, and support")
print("humanities research through computational methods.")
