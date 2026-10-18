"""Model: contém a lógica de IA do chatbot (scikit-learn)."""
import json
import random
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


@dataclass
class Message:
    """Representa uma mensagem do diálogo."""
    sender: str
    text: str
    timestamp: datetime


class TextPreprocessor:
    """Normaliza textos: minúsculas e remoção de acentos."""

    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower().strip()
        text = unicodedata.normalize("NFKD", text)
        return "".join(c for c in text if not unicodedata.combining(c))


class IntentClassifier:
    """Classificador de intenções: TF-IDF + Regressão Logística."""

    def __init__(self, threshold: float = 0.40):
        self.threshold = threshold
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))),
            ("clf", LogisticRegression(max_iter=1000, C=10)),
        ])

    def train(self, texts, labels):
        self.pipeline.fit([TextPreprocessor.normalize(t) for t in texts], labels)

    def predict(self, text: str):
        probs = self.pipeline.predict_proba([TextPreprocessor.normalize(text)])[0]
        idx = probs.argmax()
        tag = str(self.pipeline.classes_[idx])
        conf = float(probs[idx])
        return (tag if conf >= self.threshold else None), conf


class ChatbotModel:
    """Fachada do Model: carrega dados, treina e gera respostas; guarda o histórico."""

    FALLBACK = ["Desculpe, não entendi. Pode reformular?",
                "Hmm, ainda não sei responder isso."]

    def __init__(self, intents_path: Path, bot_name: str = "PyBot"):
        self.bot_name = bot_name
        self.history: list[Message] = []
        self._responses: dict[str, list[str]] = {}
        self.classifier = IntentClassifier()
        self._load_and_train(intents_path)

    def _load_and_train(self, path: Path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        texts, labels = [], []
        for intent in data["intents"]:
            self._responses[intent["tag"]] = intent["responses"]
            for p in intent["patterns"]:
                texts.append(p)
                labels.append(intent["tag"])
        self.classifier.train(texts, labels)

    def add_message(self, sender: str, text: str) -> Message:
        msg = Message(sender, text, datetime.now())
        self.history.append(msg)
        return msg

    def get_response(self, user_text: str) -> tuple[str, str | None, float]:
        tag, conf = self.classifier.predict(user_text)
        reply = random.choice(self._responses[tag] if tag else self.FALLBACK)
        return reply, tag, conf

    def clear_history(self):
        self.history.clear()
