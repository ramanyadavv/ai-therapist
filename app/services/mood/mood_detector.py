from typing import Dict

class MoodDetector:
    def __init__(self):
        self.mood_keywords = {
            "anxious": ["anxious", "worried", "nervous", "panic", "fear", "scared", "stress"],
            "sad": ["sad", "depressed", "hopeless", "crying", "empty", "grief", "loss"],
            "angry": ["angry", "frustrated", "furious", "irritated", "rage", "hate"],
            "happy": ["happy", "joy", "grateful", "excited", "wonderful", "great"],
            "overwhelmed": ["overwhelmed", "too much", "can't cope", "drowning", "exhausted"],
            "lonely": ["lonely", "alone", "isolated", "no one", "miss", "abandoned"],
        }

    def detect_mood_from_keywords(self, text: str) -> str:
        text_lower = text.lower()
        scores = {}
        for mood, keywords in self.mood_keywords.items():
            scores[mood] = sum(1 for kw in keywords if kw in text_lower)
        if max(scores.values()) == 0:
            return "neutral"
        return max(scores, key=scores.get)

    def analyze_sentiment_score(self, text: str) -> float:
        positive_words = ["good", "great", "happy", "thankful", "better", "love"]
        negative_words = ["bad", "sad", "angry", "worse", "hate", "hopeless"]
        text_lower = text.lower()
        pos = sum(1 for w in positive_words if w in text_lower)
        neg = sum(1 for w in negative_words if w in text_lower)
        total = pos + neg
        if total == 0:
            return 0.0
        return round((pos - neg) / total, 3)

    def is_crisis(self, text: str) -> bool:
        crisis_keywords = [
            "suicide", "kill myself", "end my life", "want to die",
            "self harm", "cut myself", "hurt myself", "no reason to live"
        ]
        text_lower = text.lower()
        return any(kw in text_lower for kw in crisis_keywords)

    def analyze(self, text: str) -> Dict:
        return {
            "primary_mood": self.detect_mood_from_keywords(text),
            "sentiment_score": self.analyze_sentiment_score(text),
            "is_crisis": self.is_crisis(text),
            "intensity": min(1.0, len(text.split()) / 50)
        }

mood_detector = MoodDetector()
