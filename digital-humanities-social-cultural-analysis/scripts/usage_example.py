#!/usr/bin/env python3
"""
Usage example for the SocialMediaAnalysis class in the digital-humanities-social-cultural-analysis library.
"""

from social_media_analysis import SocialMediaAnalysis
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Sample data generation function
def generate_sample_data():
    """
    Generate sample social media data for testing.
    
    Returns:
        pd.DataFrame: Sample social media data.
    """
    # Generate dates
    dates = [datetime.now() - timedelta(days=i) for i in range(30)]
    
    # Generate sample users
    users = [f"user{i}" for i in range(1, 21)]
    
    # Generate sample content
    topics = [
        "digital humanities", "social media", "cultural analysis",
        "network analysis", "sentiment analysis", "trend detection",
        "audience analysis", "content categorization", "social networks",
        "cultural heritage"
    ]
    
    # Generate sample sentiments
    sentiment_phrases = {
        "positive": ["love", "great", "amazing", "fantastic", "wonderful", "excellent", "brilliant", "awesome"],
        "negative": ["hate", "terrible", "awful", "horrible", "bad", "disappointed", "poor", "sad"],
        "neutral": ["discussing", "talking about", "exploring", "examining", "analyzing", "studying", "looking at", "investigating"]
    }
    
    # Generate sample data
    data = []
    for _ in range(500):
        user = random.choice(users)
        date = random.choice(dates)
        topic = random.choice(topics)
        sentiment = random.choice(list(sentiment_phrases.keys()))
        phrase = random.choice(sentiment_phrases[sentiment])
        
        # Generate text
        text = f"I'm {phrase} {topic} in the context of digital humanities."
        
        # Generate mentions
        num_mentions = random.randint(0, 3)
        mentions = random.sample([u for u in users if u != user], num_mentions)
        mentions_str = ", ".join(mentions)
        
        # Generate engagement metrics
        likes = random.randint(0, 100)
        shares = random.randint(0, 50)
        comments = random.randint(0, 30)
        
        data.append({
            "user": user,
            "timestamp": date,
            "text": text,
            "mentions": mentions_str,
            "likes": likes,
            "shares": shares,
            "comments": comments
        })
    
    return pd.DataFrame(data)

def main():
    """
    Main function to demonstrate the SocialMediaAnalysis class.
    """
    print("=== Digital Humanities Social Cultural Analysis ===")
    print("Creating sample social media data...")
    
    # Generate sample data
    sample_data = generate_sample_data()
    print(f"Generated {len(sample_data)} sample posts")
    
    # Create SocialMediaAnalysis instance
    sma = SocialMediaAnalysis(sample_data)
    
    # Clean data
    print("\n1. Cleaning data...")
    cleaned_data = sma.clean_data()
    print(f"Cleaned data shape: {cleaned_data.shape}")
    
    # Perform sentiment analysis
    print("\n2. Performing sentiment analysis...")
    sentiment_data = sma.sentiment_analysis()
    sentiment_counts = sentiment_data['sentiment_category'].value_counts()
    print("Sentiment distribution:")
    print(sentiment_counts)
    
    # Extract network
    print("\n3. Extracting social network...")
    network = sma.network_extraction()
    
    # Detect trends
    print("\n4. Detecting trends...")
    daily_trends = sma.trend_detection('day')
    print("Daily trends (first 5 days):")
    print(daily_trends.head())
    
    # Analyze audience
    print("\n5. Analyzing audience...")
    audience_stats = sma.audience_analysis()
    print("Top users:")
    for user, count in list(audience_stats['top_users'].items())[:5]:
        print(f"  {user}: {count} posts")
    
    print("\nTop words:")
    for word, count in list(audience_stats['top_words'].items())[:10]:
        print(f"  {word}: {count}")
    
    # Categorize content
    print("\n6. Categorizing content...")
    categorized_data = sma.content_categorization(n_clusters=5)
    category_counts = categorized_data['category'].value_counts()
    print("Content categories:")
    print(category_counts)
    
    # Visualizations (commented out for non-interactive environments)
    print("\n7. Generating visualizations...")
    print("Note: Visualizations are commented out in this example for non-interactive environments.")
    print("Uncomment the visualization calls in the script to see the visualizations.")
    
    # Uncomment the following lines to see visualizations
    # sma.visualize_sentiment()
    # sma.visualize_trends('day')
    # sma.visualize_network()
    
    print("\n=== Analysis Complete ===")

if __name__ == "__main__":
    main()
