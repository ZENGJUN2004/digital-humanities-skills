#!/usr/bin/env python3
"""
Usage example for Digital Humanities Historical Research skill
Demonstrates how to analyze a historical document using the HistoricalAnalysis and NetworkAnalysis classes
"""

from historical_analysis import HistoricalAnalysis
from network_analysis import NetworkAnalysis
import os

# Load the sample historical document
asset_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
sample_text_path = os.path.join(asset_dir, 'sample_historical_document.txt')

with open(sample_text_path, 'r', encoding='utf-8') as f:
    sample_text = f.read()

print("=== Digital Humanities Historical Research Example ===")
print("Analyzing the United States Declaration of Independence (Excerpt)")
print("=" * 60)

# Initialize HistoricalAnalysis
analyzer = HistoricalAnalysis(sample_text)

print("\n1. Text Analysis")
print("-" * 40)

# Text type identification
text_type = analyzer.identify_text_type()
print(f"Text type: {text_type}")

# Lexical features
lexical_features = analyzer.analyze_lexical_features()
print(f"Word count: {lexical_features['word_count']}")
print(f"Lexical diversity: {lexical_features['lexical_diversity']:.3f}")
print(f"Historical term ratio: {lexical_features['historical_term_ratio']:.3f}")
print(f"Most common words:")
for word, count in lexical_features['most_common_words'][:5]:
    print(f"  - {word}: {count}")

print("\n2. Entity Extraction")
print("-" * 40)
entities = analyzer.extract_entities()
print(f"Persons: {entities['persons']}")
print(f"Places: {entities['places']}")
print(f"Organizations: {entities['organizations']}")

print("\n3. Anachronism Detection")
print("-" * 40)
anachronisms = analyzer.detect_anachronisms()
if anachronisms:
    print("Potential anachronisms:")
    for anachronism in anachronisms:
        print(f"  - {anachronism}")
else:
    print("No potential anachronisms detected.")

print("\n4. Timeline Creation")
print("-" * 40)
timeline = analyzer.create_timeline()
if timeline:
    print("Historical timeline:")
    for event in timeline:
        print(f"  {event['date']}: {event['event'][:100]}...")
else:
    print("No date references found in the text.")

print("\n5. Discourse Analysis")
print("-" * 40)
discourse = analyzer.analyze_discourse()
print("Discourse markers:")
for category, count in discourse['counts'].items():
    print(f"  {category}: {count}")

print("\n6. Network Analysis")
print("-" * 40)

# Initialize NetworkAnalysis
network_analyzer = NetworkAnalysis([sample_text])

# Build network
network = network_analyzer.build_network()
print(f"Network nodes: {len(network.nodes())}")
print(f"Network edges: {len(network.edges())}")
print(f"Network density: {network_analyzer.analyze_network()['density']:.3f}")

# Identify key figures
key_figures = network_analyzer.identify_key_figures(top_n=5)
print("Key figures in the network:")
for figure, score in key_figures:
    print(f"  - {figure}: {score:.3f}")

# Analyze relationship strength
relationships = network_analyzer.analyze_relationship_strength()
if relationships:
    print("\nStrongest relationships:")
    for source, target, weight in relationships[:3]:
        print(f"  {source} - {target}: {weight}")

print("\n=== Analysis Complete ===")
print("This example demonstrates how the Digital Humanities Historical Research skill")
print("can be used to analyze historical documents, extract entities, detect")
print("anachronisms, create timelines, analyze discourse, and map relationships.")
