# services/backend/app/nlp.py
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np

# load once (takes a moment)
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
# small sentiment pipeline (CPU)
sentiment_pipe = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

def embed_texts(texts):
    """
    texts: list[str]
    returns: numpy array (n, dim)
    """
    return embed_model.encode(texts, show_progress_bar=False, convert_to_numpy=True)

def analyze_sentiment(text):
    # returns standardized label: "positive"/"negative"/"neutral" and confidence
    res = sentiment_pipe(text[:512])[0]
    lbl = res['label'].lower()
    score = float(res['score'])
    # transform to 'neutral' under threshold (optional)
    if score < 0.6:
        return "neutral", score
    return lbl, score