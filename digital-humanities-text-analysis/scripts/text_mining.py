import re
import string
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import numpy as np

class TextMining:
    def __init__(self, text):
        """
        Initialize TextMining with the text to analyze
        """
        self.text = text
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
    
    def clean_text(self):
        """
        Clean and preprocess the text
        """
        # Convert to lowercase
        text = self.text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        cleaned_tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        
        # Join back to string
        cleaned_text = ' '.join(cleaned_tokens)
        
        return cleaned_text
    
    def extract_keywords(self, n=10):
        """
        Extract top n keywords using TF-IDF
        """
        # Clean text
        cleaned_text = self.clean_text()
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([cleaned_text])
        
        # Get feature names and scores
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        
        # Sort by score
        keyword_scores = [(feature_names[i], scores[i]) for i in range(len(feature_names))]
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top n keywords
        return keyword_scores[:n]
    
    def topic_modeling(self, n_topics=5, n_words=5, method='lda'):
        """
        Perform topic modeling using LDA or NMF
        """
        # Clean text
        cleaned_text = self.clean_text()
        
        # Tokenize into sentences
        sentences = sent_tokenize(self.text)
        cleaned_sentences = [self.clean_text() for sentence in sentences]
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(cleaned_sentences)
        
        # Perform topic modeling
        if method == 'lda':
            model = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        else:  # nmf
            model = NMF(n_components=n_topics, random_state=42)
        
        topic_matrix = model.fit_transform(tfidf_matrix)
        
        # Get feature names
        feature_names = vectorizer.get_feature_names_out()
        
        # Extract top words for each topic
        topics = []
        for i, topic in enumerate(model.components_):
            top_words = [feature_names[j] for j in topic.argsort()[:-n_words-1:-1]]
            topics.append({
                'topic_id': i+1,
                'top_words': top_words
            })
        
        return topics
    
    def sentiment_analysis(self):
        """
        Perform sentiment analysis
        """
        # Create TextBlob object
        blob = TextBlob(self.text)
        
        # Get sentiment score
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment category
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'sentiment': sentiment
        }
    
    def compare_texts(self, other_text):
        """
        Compare this text with another text using cosine similarity
        """
        # Clean both texts
        cleaned_self = self.clean_text()
        cleaned_other = TextMining(other_text).clean_text()
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([cleaned_self, cleaned_other])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return similarity
    
    def text_statistics(self):
        """
        Calculate various text statistics
        """
        # Tokenize
        tokens = word_tokenize(self.text)
        sentences = sent_tokenize(self.text)
        
        # Calculate basic statistics
        word_count = len(tokens)
        sentence_count = len(sentences)
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        
        # Calculate lexical diversity
        unique_words = set(tokens)
        lexical_diversity = len(unique_words) / word_count if word_count > 0 else 0
        
        # Calculate punctuation count
        punctuation_count = sum(1 for char in self.text if char in string.punctuation)
        
        # Calculate word frequency
        word_freq = Counter(tokens)
        most_common_words = word_freq.most_common(10)
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_words_per_sentence': avg_words_per_sentence,
            'lexical_diversity': lexical_diversity,
            'punctuation_count': punctuation_count,
            'most_common_words': most_common_words
        }
    
    def extract_entities(self):
        """
        Extract named entities from the text
        """
        # Create TextBlob object
        blob = TextBlob(self.text)
        
        # Extract entities
        entities = {}
        for sentence in blob.sentences:
            for word, tag in sentence.tags:
                if tag in ['NNP', 'NNPS']:  # Proper nouns
                    if word not in entities:
                        entities[word] = 0
                    entities[word] += 1
        
        # Sort by count
        sorted_entities = sorted(entities.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_entities
    
    def readability_scores(self):
        """
        Calculate basic readability scores
        """
        # Tokenize
        tokens = word_tokenize(self.text)
        sentences = sent_tokenize(self.text)
        
        # Calculate statistics
        word_count = len(tokens)
        sentence_count = len(sentences)
        
        # Calculate average sentence length
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Calculate percentage of complex words (words with 3+ syllables)
        complex_words = 0
        for word in tokens:
            syllables = self.count_syllables(word)
            if syllables >= 3:
                complex_words += 1
        
        percent_complex_words = complex_words / word_count if word_count > 0 else 0
        
        # Calculate Flesch-Kincaid Grade Level
        # Formula: 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
        total_syllables = sum(self.count_syllables(word) for word in tokens)
        avg_syllables_per_word = total_syllables / word_count if word_count > 0 else 0
        
        flesch_kincaid = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
        
        return {
            'avg_sentence_length': avg_sentence_length,
            'percent_complex_words': percent_complex_words,
            'flesch_kincaid_grade_level': flesch_kincaid
        }
    
    def count_syllables(self, word):
        """
        Count syllables in a word (simplified)
        """
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        
        if word[0] in vowels:
            count += 1
        
        for index in range(1, len(word)):
            if word[index] in vowels and word[index-1] not in vowels:
                count += 1
        
        if word.endswith("e"):
            count -= 1
        
        if count == 0:
            count = 1
        
        return count
