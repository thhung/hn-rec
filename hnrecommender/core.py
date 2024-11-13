import json
import os

import nltk
import requests
import torch
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("stopwords")

# Base URL for Hacker News API
base_url = "https://hacker-news.firebaseio.com/v0"

ASSET_FOLDER = "../query_reformulation/assets"
cross_encoder = ORTModelForSequenceClassification.from_pretrained(
    f"{ASSET_FOLDER}/ce-ms-marco-MiniLM-L-6-v2"
)
ce_tokenizer = AutoTokenizer.from_pretrained(
    f"{ASSET_FOLDER}/ce-ms-marco-MiniLM-L-6-v2"
)
# Cache directory
CACHE_DIR = "cache_stories/"

# Ensure the cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def warmup():
    """warm up cross encoder for performance"""
    texts = [
        ["How many people live in Berlin?", "How many people live in Berlin?"],
        [
            "Berlin has a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers.",
            "New York City is famous for the Metropolitan Museum of Art.",
        ],
    ] * 40

    warmup_features = ce_tokenizer(texts[:10], padding=True, return_tensors="pt")
    with torch.no_grad():
        scores = cross_encoder(**warmup_features).logits


warmup()


def clean_paragraph(paragraph):
    """
    split a paragraphh into sentences and clean up each sentences and return the cleaned one.
    Remove stop words and non alphanet numeric characters.

    Parameters:
        limit: number of stories to return

    Returns:
        list of HN story object: refers to HN API documentation.
    """
    # Tokenize paragraph into sentences
    sentences = sent_tokenize(paragraph)

    # Get English stopwords
    stop_words = set(stopwords.words("english"))

    cleaned_sentences = []

    # Iterate through each sentence
    for sentence in sentences:
        # Tokenize sentence into words
        words = word_tokenize(sentence)

        # Remove stopwords and non-alphabetic words
        cleaned_words = [
            word for word in words if word.isalnum() and word.lower() not in stop_words
        ]

        # Reconstruct sentence from cleaned words and add to list
        cleaned_sentence = " ".join(cleaned_words)
        cleaned_sentences.append(cleaned_sentence)

    return cleaned_sentences

# Function to fetch story data with caching based on story ID
def fetch_top_hacker_news_items(limit=500):
    """
    Retrieve top N stories from HN with cache to improve processing time.

    Parameters:
        limit: number of stories to return

    Returns:
        list of HN story object: refers to HN API documentation.
    """
    # Fetch the top story IDs
    top_stories_url = f"{base_url}/topstories.json"
    response = requests.get(top_stories_url)

    if response.status_code == 200:
        top_story_ids = response.json()[:limit]  # Get only the top `limit` story IDs
        stories = []

        # Fetch details for each story ID
        for story_id in top_story_ids:
            # Check if the story is already cached
            cache_file = os.path.join(CACHE_DIR, f"{story_id}.json")
            if os.path.exists(cache_file):
                print(f"Loading story with ID {story_id} from cache.")
                with open(cache_file, "r") as f:
                    story_data = json.load(f)
            else:
                print(f"Fetching story with ID {story_id} from the web.")
                story_url = f"{base_url}/item/{story_id}.json"
                story_response = requests.get(story_url)

                if story_response.status_code == 200:
                    story_data = story_response.json()
                    # Save the fetched data to cache
                    with open(cache_file, "w") as f:
                        json.dump(story_data, f)
                else:
                    print(f"Failed to fetch story with ID: {story_id}")
                    continue

            stories.append(story_data)

        return stories
    else:
        print("Failed to fetch top stories.")
        return []


def recommend_hacker_news(user_bio, limit=100):
    """
    From users' bio suggest HN story for them to match their interest

    Parameters:
        user_bio (str) : paragraph describe what they like
        limit: number of stories to returns.
    Returns:
        list of HN story object: refers to HN API documentation. 
    """
    top_500_stories = fetch_top_hacker_news_items(limit)
    user_profile = clean_paragraph(user_bio)
    list_scores = []
    for sentence in user_profile:
        text_pairs = [[sentence, story["title"]] for story in top_500_stories]
        features = ce_tokenizer(text_pairs, padding=True, return_tensors="pt")
        ranks = cross_encoder(**features).logits
        list_scores.append(ranks)
    scores = torch.mean(torch.cat(list_scores, dim=1), dim=1)
    _, indices = torch.topk(scores, scores.shape[0], dim=0, largest=True)
    return [top_500_stories[i] for i in indices]
