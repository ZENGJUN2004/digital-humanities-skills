import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import networkx as nx
from datetime import datetime
import re

class SocialMediaAnalysis:
    """
    A comprehensive class for analyzing social media data in digital humanities contexts.
    """
    
    def __init__(self, data=None):
        """
        Initialize the SocialMediaAnalysis class with optional data.
        
        Args:
            data (pd.DataFrame, optional): Social media data to analyze.
        """
        self.data = data
    
    def load_data(self, file_path):
        """
        Load social media data from a CSV file.
        
        Args:
            file_path (str): Path to the CSV file containing social media data.
        
        Returns:
            pd.DataFrame: Loaded social media data.
        """
        try:
            self.data = pd.read_csv(file_path)
            print(f"Loaded data from {file_path}")
            return self.data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def clean_data(self):
        """
        Clean social media data by removing duplicates, handling missing values, and standardizing formats.
        
        Returns:
            pd.DataFrame: Cleaned social media data.
        """
        if self.data is None:
            print("No data to clean. Please load data first.")
            return None
        
        try:
            # Remove duplicates
            self.data = self.data.drop_duplicates()
            
            # Handle missing values
            self.data = self.data.dropna(subset=['text'])
            
            # Standardize timestamps if present
            if 'timestamp' in self.data.columns:
                self.data['timestamp'] = pd.to_datetime(self.data['timestamp'], errors='coerce')
            
            # Clean text
            self.data['cleaned_text'] = self.data['text'].apply(self._clean_text)
            
            print("Data cleaned successfully")
            return self.data
        except Exception as e:
            print(f"Error cleaning data: {e}")
            return None
    
    def _clean_text(self, text):
        """
        Clean text by removing noise, URLs, and special characters.
        
        Args:
            text (str): Text to clean.
        
        Returns:
            str: Cleaned text.
        """
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def sentiment_analysis(self):
        """
        Perform sentiment analysis on social media text.
        
        Returns:
            pd.DataFrame: Data with sentiment scores.
        """
        if self.data is None:
            print("No data for sentiment analysis. Please load data first.")
            return None
        
        try:
            # Ensure text is cleaned
            if 'cleaned_text' not in self.data.columns:
                self.data['cleaned_text'] = self.data['text'].apply(self._clean_text)
            
            # Calculate sentiment
            self.data['sentiment'] = self.data['cleaned_text'].apply(lambda x: TextBlob(x).sentiment.polarity)
            self.data['sentiment_category'] = self.data['sentiment'].apply(lambda x: 'positive' if x > 0 else 'negative' if x < 0 else 'neutral')
            
            print("Sentiment analysis completed")
            return self.data
        except Exception as e:
            print(f"Error performing sentiment analysis: {e}")
            return None
    
    def network_extraction(self):
        """
        Extract social networks from social media data.
        
        Returns:
            nx.Graph: Extracted social network graph.
        """
        if self.data is None:
            print("No data for network extraction. Please load data first.")
            return None
        
        try:
            # Create a graph
            G = nx.Graph()
            
            # Add edges based on mentions or connections
            # This is a simplified example - actual implementation would depend on data format
            if 'user' in self.data.columns and 'mentions' in self.data.columns:
                for _, row in self.data.iterrows():
                    user = row['user']
                    mentions = row['mentions'].split(',') if isinstance(row['mentions'], str) else []
                    for mention in mentions:
                        mention = mention.strip()
                        if mention and user != mention:
                            G.add_edge(user, mention)
            
            print(f"Network extracted with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
            return G
        except Exception as e:
            print(f"Error extracting network: {e}")
            return None
    
    def trend_detection(self, time_period='day'):
        """
        Detect trends in social media data over time.
        
        Args:
            time_period (str): Time period for trend detection ('day', 'week', 'month').
        
        Returns:
            pd.DataFrame: Trend data.
        """
        if self.data is None:
            print("No data for trend detection. Please load data first.")
            return None
        
        try:
            # Ensure timestamp column exists
            if 'timestamp' not in self.data.columns:
                print("No timestamp column found. Cannot perform trend detection.")
                return None
            
            # Set timestamp as index
            data = self.data.set_index('timestamp').copy()
            
            # Resample based on time period
            if time_period == 'day':
                trends = data.resample('D').size().to_frame('count')
            elif time_period == 'week':
                trends = data.resample('W').size().to_frame('count')
            elif time_period == 'month':
                trends = data.resample('M').size().to_frame('count')
            else:
                print(f"Invalid time period: {time_period}")
                return None
            
            # Calculate rolling average
            trends['rolling_avg'] = trends['count'].rolling(window=3, min_periods=1).mean()
            
            print(f"Trend detection completed for {time_period} time period")
            return trends
        except Exception as e:
            print(f"Error detecting trends: {e}")
            return None
    
    def audience_analysis(self):
        """
        Analyze audience demographics and engagement patterns.
        
        Returns:
            dict: Audience analysis results.
        """
        if self.data is None:
            print("No data for audience analysis. Please load data first.")
            return None
        
        try:
            analysis = {}
            
            # Basic engagement metrics
            if 'likes' in self.data.columns:
                analysis['average_likes'] = self.data['likes'].mean()
            if 'shares' in self.data.columns:
                analysis['average_shares'] = self.data['shares'].mean()
            if 'comments' in self.data.columns:
                analysis['average_comments'] = self.data['comments'].mean()
            
            # User analysis
            if 'user' in self.data.columns:
                user_counts = self.data['user'].value_counts()
                analysis['top_users'] = user_counts.head(10).to_dict()
                analysis['unique_users'] = self.data['user'].nunique()
            
            # Content analysis
            if 'text' in self.data.columns:
                # Most frequent words
                all_text = ' '.join(self.data['cleaned_text'] if 'cleaned_text' in self.data.columns else self.data['text'])
                word_counts = pd.Series(all_text.split()).value_counts()
                analysis['top_words'] = word_counts.head(20).to_dict()
            
            print("Audience analysis completed")
            return analysis
        except Exception as e:
            print(f"Error performing audience analysis: {e}")
            return None
    
    def content_categorization(self, n_clusters=5):
        """
        Categorize social media content using clustering.
        
        Args:
            n_clusters (int): Number of clusters for categorization.
        
        Returns:
            pd.DataFrame: Data with content categories.
        """
        if self.data is None:
            print("No data for content categorization. Please load data first.")
            return None
        
        try:
            # Ensure text is cleaned
            if 'cleaned_text' not in self.data.columns:
                self.data['cleaned_text'] = self.data['text'].apply(self._clean_text)
            
            # Vectorize text
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            X = vectorizer.fit_transform(self.data['cleaned_text'])
            
            # Cluster text
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            self.data['category'] = kmeans.fit_predict(X)
            
            # Get top terms for each cluster
            terms = vectorizer.get_feature_names_out()
            clusters = kmeans.cluster_centers_.argsort()[:, ::-1]
            
            print("Content categorization completed")
            return self.data
        except Exception as e:
            print(f"Error categorizing content: {e}")
            return None
    
    def visualize_sentiment(self):
        """
        Visualize sentiment distribution.
        """
        if self.data is None or 'sentiment' not in self.data.columns:
            print("No sentiment data to visualize. Please run sentiment analysis first.")
            return
        
        try:
            plt.figure(figsize=(10, 6))
            sns.histplot(self.data['sentiment'], bins=30, kde=True)
            plt.title('Sentiment Distribution')
            plt.xlabel('Sentiment Score')
            plt.ylabel('Frequency')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error visualizing sentiment: {e}")
    
    def visualize_trends(self, time_period='day'):
        """
        Visualize trends over time.
        
        Args:
            time_period (str): Time period for visualization ('day', 'week', 'month').
        """
        trends = self.trend_detection(time_period)
        if trends is None:
            return
        
        try:
            plt.figure(figsize=(12, 6))
            plt.plot(trends.index, trends['count'], marker='o', label='Raw Count')
            plt.plot(trends.index, trends['rolling_avg'], marker='', linewidth=2, label='3-Period Rolling Average')
            plt.title(f'Post Frequency Trend ({time_period.capitalize()}ly)')
            plt.xlabel('Date')
            plt.ylabel('Post Count')
            plt.legend()
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error visualizing trends: {e}")
    
    def visualize_network(self):
        """
        Visualize social network.
        """
        G = self.network_extraction()
        if G is None:
            return
        
        try:
            plt.figure(figsize=(12, 10))
            # Use spring layout for better visualization
            pos = nx.spring_layout(G, k=0.15, iterations=20)
            nx.draw(G, pos, node_size=50, node_color='lightblue', edge_color='gray', with_labels=False)
            plt.title('Social Network Visualization')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error visualizing network: {e}")
