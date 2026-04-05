"""
NLP Processor — tokenization, keyword extraction, text similarity using NLTK and TF-IDF
"""
import re
import nltk
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


class NLPProcessor:
    """Handles tokenization, keyword extraction, and text similarity"""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000,
        )

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        if not text:
            return []
        text = text.lower()
        tokens = word_tokenize(text)
        # Keep only alphabetic tokens
        tokens = [t for t in tokens if t.isalpha()]
        return tokens

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove common stopwords from token list"""
        return [t for t in tokens if t not in stop_words]

    def lemmatize(self, tokens: List[str]) -> List[str]:
        """Lemmatize tokens to their base form"""
        return [lemmatizer.lemmatize(t) for t in tokens]

    def extract_keywords(self, text: str, top_n: int = 15) -> List[str]:
        """
        Extract most important keywords from text.
        Uses POS tagging to prioritize nouns, verbs, and adjectives.
        """
        if not text:
            return []

        text = text.lower()
        tokens = word_tokenize(text)

        # POS tagging
        tagged = pos_tag(tokens)

        # Filter: keep nouns (NN*), verbs (VB*), adjectives (JJ)
        # Also keep technical terms (contains underscore or is alphanumeric mix)
        important_pos = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ', 'JJR', 'JJS']
        keywords = []

        for word, tag in tagged:
            if word.isalpha() and len(word) > 2:
                # Prioritize based on POS tag
                if tag in important_pos:
                    lemma = lemmatizer.lemmatize(word)
                    if lemma not in stop_words:
                        keywords.append(lemma)

        # Count frequency and return top N
        from collections import Counter
        freq = Counter(keywords)
        return [word for word, _ in freq.most_common(top_n)]

    def get_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts using TF-IDF.
        Returns a value between 0 and 1.
        """
        if not text1 or not text2:
            return 0.0

        try:
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception:
            return 0.0

    def get_keyword_overlap(self, text1: str, text2: str) -> Tuple[List[str], List[str], float]:
        """
        Get keywords that overlap between two texts.
        Returns: (matched_keywords, missed_keywords, overlap_score_0_100)
        """
        keywords1 = set(self.extract_keywords(text1))
        keywords2 = set(self.extract_keywords(text2))

        matched = keywords1.intersection(keywords2)
        missed_in_text2 = keywords1 - keywords2

        if not keywords1:
            return [], [], 0.0

        overlap_score = (len(matched) / len(keywords1)) * 100
        return list(matched), list(missed_in_text2), round(overlap_score, 2)

    def preprocess(self, text: str) -> str:
        """Full preprocessing pipeline: clean, tokenize, remove stopwords, lemmatize"""
        if not text:
            return ""
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        tokens = self.lemmatize(tokens)
        return ' '.join(tokens)
