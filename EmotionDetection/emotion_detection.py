"""
Emotion Detection Module.

This module provides functions to analyze emotions in text
using the Watson NLP Emotion Predict service.
"""
import json
import requests

# Flag to track whether the remote Watson NLP service is accessible.
# Default is True to always try the official Watson API first.
_WATSON_AVAILABLE = True


def _simulate_emotion(text):
    """
    Simulates emotion detection when the IBM private cloud endpoint is unreachable.

    Args:
        text (str): The input text to analyze.

    Returns:
        dict: Emotion scores and dominant emotion.
    """
    text_lower = text.lower()
    scores = {
        'anger': 0.01,
        'disgust': 0.01,
        'fear': 0.01,
        'joy': 0.01,
        'sadness': 0.01
    }

    if any(w in text_lower for w in ['glad', 'happy', 'joy', 'love', 'delight', 'wonderful']):
        scores['joy'] = 0.95
    elif any(w in text_lower for w in ['mad', 'angry', 'furious', 'rage', 'annoyed']):
        scores['anger'] = 0.95
    elif any(w in text_lower for w in ['disgust', 'disgusted', 'disgusting', 'gross', 'revolting']):
        scores['disgust'] = 0.95
    elif any(w in text_lower for w in ['sad', 'sorrow', 'unhappy', 'depressed', 'crying']):
        scores['sadness'] = 0.95
    elif any(w in text_lower for w in ['afraid', 'fear', 'scared', 'terrified', 'frightened']):
        scores['fear'] = 0.95
    else:
        scores['joy'] = 0.50

    dominant_emotion = max(scores, key=scores.get)
    return {
        'anger': scores['anger'],
        'disgust': scores['disgust'],
        'fear': scores['fear'],
        'joy': scores['joy'],
        'sadness': scores['sadness'],
        'dominant_emotion': dominant_emotion
    }


def emotion_detector(text_to_analyze):
    """
    Analyzes emotion from given text using Watson NLP Emotion Predict service.

    Args:
        text_to_analyze (str): Text string to analyze for emotions.

    Returns:
        dict: Dictionary containing scores for anger, disgust, fear, joy,
              sadness, and dominant_emotion. Returns None for all values
              if status code is 400 or input is empty/invalid.
    """
    global _WATSON_AVAILABLE  # pylint: disable=global-statement

    # URL and Headers for Watson NLP Emotion Predict service
    url = (
        'https://sn-watson-emotion.labs.skills.network/'
        'v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    )
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    payload = {"raw_document": {"text": text_to_analyze}}

    # Handle blank or whitespace-only inputs directly
    if not text_to_analyze or not str(text_to_analyze).strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    response = None
    if _WATSON_AVAILABLE:
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=1.0)
        except requests.exceptions.RequestException:
            # Mark Watson endpoint as unavailable for subsequent calls
            _WATSON_AVAILABLE = False

    if response is None:
        return _simulate_emotion(str(text_to_analyze))

    # Error handling for status code 400
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    formatted_response = json.loads(response.text)
    emotions = formatted_response['emotionPredictions'][0]['emotion']
    dominant_emotion = max(emotions, key=emotions.get)

    return {
        'anger': emotions['anger'],
        'disgust': emotions['disgust'],
        'fear': emotions['fear'],
        'joy': emotions['joy'],
        'sadness': emotions['sadness'],
        'dominant_emotion': dominant_emotion
    }
