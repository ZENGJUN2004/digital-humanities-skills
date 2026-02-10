import re
import string
from collections import Counter, defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from textblob import TextBlob
import dateparser

class HistoricalAnalysis:
    def __init__(self, text):
        """
        Initialize HistoricalAnalysis with the historical text to analyze
        """
        self.text = text
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        # Using NLTK-based entity extraction instead of spaCy
        # to avoid Python 3.14 compatibility issues
    
    def normalize_text(self):
        """
        Normalize historical text by standardizing spelling and formatting
        """
        # Convert to lowercase
        text = self.text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        normalized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        
        # Join back to string
        normalized_text = ' '.join(normalized_tokens)
        
        return normalized_text
    
    def extract_entities(self):
        """
        Extract historical entities (people, places, organizations) from text
        """
        entities = {
            'persons': [],
            'places': [],
            'organizations': []
        }
        
        # Use NLTK-based entity extraction
        sentences = sent_tokenize(self.text)
        for sentence in sentences:
            tokens = word_tokenize(sentence)
            tagged_tokens = pos_tag(tokens)
            for i, (word, tag) in enumerate(tagged_tokens):
                # Simple heuristic: capitalized words that are proper nouns
                if word.istitle() and tag in ['NNP', 'NNPS']:
                    # Check if it's part of a multi-word entity
                    entity = word
                    j = i + 1
                    while j < len(tagged_tokens) and tagged_tokens[j][0].istitle() and tagged_tokens[j][1] in ['NNP', 'NNPS']:
                        entity += ' ' + tagged_tokens[j][0]
                        j += 1
                    # Add to appropriate category (simplified)
                    if any(keyword in entity.lower() for keyword in ['king', 'queen', 'emperor', 'president', 'mr', 'mrs', 'ms']):
                        entities['persons'].append(entity)
                    elif any(keyword in entity.lower() for keyword in ['city', 'town', 'village', 'country', 'state', 'kingdom', 'empire', 'colony', 'state']):
                        entities['places'].append(entity)
                    elif any(keyword in entity.lower() for keyword in ['company', 'organization', 'university', 'college', 'church', 'government', 'legislature', 'house', 'congress']):
                        entities['organizations'].append(entity)
                    else:
                        # Default to person if unsure
                        entities['persons'].append(entity)
        
        # Remove duplicates and sort
        for key in entities:
            entities[key] = sorted(list(set(entities[key])))
        
        return entities
    
    def detect_anachronisms(self):
        """
        Detect potential anachronisms in historical text
        """
        potential_anachronisms = []
        
        # Common technological anachronisms
        tech_terms = [
            'telephone', 'television', 'radio', 'computer', 'internet', 'airplane',
            'car', 'automobile', 'train', 'electricity', 'light bulb', 'camera',
            'photograph', 'movie', 'film', 'telegram', 'telegraph'
        ]
        
        # Common cultural anachronisms
        cultural_terms = [
            'democracy', 'socialism', 'capitalism', 'communism', 'feminism',
            'psychology', 'sociology', 'anthropology', 'evolution', 'genetics',
            'bacteria', 'virus', 'atom', 'nuclear', 'radioactive'
        ]
        
        # Common chronological markers
        time_terms = [
            'BC', 'AD', 'CE', 'BCE', 'century', 'decade', 'year'
        ]
        
        # Check for technological anachronisms
        for term in tech_terms:
            if term in self.text.lower():
                potential_anachronisms.append(f"Technological anachronism: {term}")
        
        # Check for cultural anachronisms
        for term in cultural_terms:
            if term in self.text.lower():
                potential_anachronisms.append(f"Cultural anachronism: {term}")
        
        # Check for chronological inconsistencies
        sentences = sent_tokenize(self.text)
        for sentence in sentences:
            # Look for date references
            date_matches = re.findall(r'\b(\d{4})\b', sentence)
            for date in date_matches:
                year = int(date)
                # Check for dates that are too early or too late for common contexts
                if year < 1000 or year > 2024:
                    potential_anachronisms.append(f"Chronological inconsistency: Year {year}")
        
        return potential_anachronisms
    
    def create_timeline(self):
        """
        Create a timeline of historical events mentioned in the text
        """
        timeline = []
        
        # Extract date references
        sentences = sent_tokenize(self.text)
        for sentence in sentences:
            # Try to parse dates without fuzzy parameter
            try:
                parsed_dates = dateparser.parse(sentence)
                if parsed_dates:
                    timeline.append({
                        'date': parsed_dates.strftime('%Y-%m-%d'),
                        'event': sentence.strip()
                    })
            except:
                pass
            
            # Look for year references
            year_matches = re.findall(r'\b(\d{4})\b', sentence)
            for year in year_matches:
                timeline.append({
                    'date': f"{year}-01-01",
                    'event': sentence.strip()
                })
            
            # Look for century references
            century_matches = re.findall(r'(\d+)(st|nd|rd|th) century', sentence, re.IGNORECASE)
            for century, suffix in century_matches:
                year = (int(century) - 1) * 100
                timeline.append({
                    'date': f"{year}-01-01",
                    'event': sentence.strip()
                })
        
        # Sort timeline by date
        timeline.sort(key=lambda x: x['date'])
        
        return timeline
    
    def analyze_lexical_features(self):
        """
        Analyze lexical features of historical text
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
        
        # Calculate word frequency
        word_freq = Counter(tokens)
        most_common_words = word_freq.most_common(10)
        
        # Calculate historical vocabulary indicators
        historical_terms = [
            'thee', 'thou', 'thy', 'thine', 'ye', 'hath', 'hast', 'doth', 'didst',
            'art', 'wert', 'wilt', 'wouldst', 'couldst', 'shouldst', 'mightst'
        ]
        historical_term_count = sum(1 for token in tokens if token.lower() in historical_terms)
        historical_term_ratio = historical_term_count / word_count if word_count > 0 else 0
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_words_per_sentence': avg_words_per_sentence,
            'lexical_diversity': lexical_diversity,
            'most_common_words': most_common_words,
            'historical_term_count': historical_term_count,
            'historical_term_ratio': historical_term_ratio
        }
    
    def identify_text_type(self):
        """
        Identify the type of historical text (e.g., letter, diary, official document)
        """
        text_lower = self.text.lower()
        
        # Common text type indicators
        text_types = {
            'letter': ['dear', 'yours sincerely', 'yours faithfully', 'regards', 'greetings'],
            'diary': ['dear diary', 'today', 'yesterday', 'tomorrow', 'entry'],
            'official document': ['decree', 'law', 'act', 'ordinance', 'proclamation', 'edict'],
            'newspaper': ['news', 'report', 'article', 'journal', 'gazette'],
            'speech': ['ladies and gentlemen', 'fellow citizens', 'speech', 'address', 'oration'],
            'historical narrative': ['history', 'chronicle', 'account', 'story', 'tale'],
            'correspondence': ['letter', 'write', 'reply', 'response', 'correspondence']
        }
        
        # Score each text type
        scores = {}
        for text_type, indicators in text_types.items():
            score = sum(1 for indicator in indicators if indicator in text_lower)
            scores[text_type] = score
        
        # Identify most likely text type
        if scores:
            most_likely_type = max(scores, key=scores.get)
            if scores[most_likely_type] > 0:
                return most_likely_type
        
        return 'unknown'
    
    def analyze_discourse(self):
        """
        Analyze discourse features of historical text
        """
        # Identify discourse markers
        discourse_markers = {
            'temporal': ['then', 'when', 'before', 'after', 'while', 'during', 'subsequently', 'previously'],
            'causal': ['because', 'since', 'as', 'due to', 'therefore', 'thus', 'consequently', 'hence'],
            'contrastive': ['but', 'however', 'nevertheless', 'nonetheless', 'although', 'though', 'whereas'],
            'additive': ['and', 'also', 'furthermore', 'moreover', 'in addition', 'besides', 'plus'],
            'sequential': ['first', 'second', 'third', 'finally', 'next', 'then', 'lastly', 'initially']
        }
        
        # Count discourse markers
        counts = {}
        text_lower = self.text.lower()
        
        for category, markers in discourse_markers.items():
            count = sum(1 for marker in markers if marker in text_lower)
            counts[category] = count
        
        # Calculate total discourse markers
        total_markers = sum(counts.values())
        
        # Calculate ratios
        ratios = {}
        word_count = len(word_tokenize(self.text))
        if word_count > 0:
            for category, count in counts.items():
                ratios[category] = count / word_count
            ratios['total'] = total_markers / word_count
        
        return {
            'counts': counts,
            'ratios': ratios,
            'total_markers': total_markers
        }
