# Emotion Detection System

A complete Python and Flask web application that performs emotion analysis on text using the IBM Watson Natural Language Processing (NLP) Emotion Predict service.

---

## Table of Contents
1. [Overview](#overview)
2. [Project Architecture & Directory Structure](#project-architecture--directory-structure)
3. [Watson NLP Service Integration](#watson-nlp-service-integration)
4. [Error Handling](#error-handling)
5. [Prerequisites & Installation](#prerequisites--installation)
6. [Unit Testing](#unit-testing)
7. [Static Code Analysis (Pylint 10.00/10)](#static-code-analysis-pylint-100010)
8. [Running the Web Server](#running-the-web-server)
9. [API & Web Usage Examples](#api--web-usage-examples)

---

## Overview

This project provides an AI-powered emotion detection service. It extracts confidence scores for five primary emotions:
- **anger**
- **disgust**
- **fear**
- **joy**
- **sadness**

The service computes the **dominant emotion** (the emotion with the highest score) and presents the formatted results through a Flask web application and a RESTful endpoint.

---

## Project Architecture & Directory Structure

```text
final_project/
├── EmotionDetection/
│   ├── __init__.py                # Package initializer exposing emotion_detector
│   └── emotion_detection.py       # Core emotion detection logic & API caller
├── static/
│   └── mywebscript.js             # AJAX script handling frontend user requests
├── templates/
│   └── index.html                 # Web UI template
├── test_emotion_detection.py      # Unit test suite (5 emotion assertions)
├── server.py                      # Flask web application server (port 5000)
└── README.md                      # Comprehensive project documentation
```

---

## Watson NLP Service Integration

The core detection function interacts with the Watson NLP Emotion Predict service:

- **Service URL**:  
  `https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict`
- **Headers**:  
  `{"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}`
- **Payload**:  
  `{"raw_document": {"text": text_to_analyze}}`

### Output Format
The `emotion_detector` function returns a dictionary:
```python
{
    'anger': <anger_score>,
    'disgust': <disgust_score>,
    'fear': <fear_score>,
    'joy': <joy_score>,
    'sadness': <sadness_score>,
    'dominant_emotion': '<dominant_emotion>'
}
```

---

## Error Handling

1. **Status Code 400 & Blank Inputs**:
   If the Watson NLP API returns a `400` status code (or when the input text is empty or blank), the `emotion_detector` function returns:
   ```python
   {
       'anger': None,
       'disgust': None,
       'fear': None,
       'joy': None,
       'sadness': None,
       'dominant_emotion': None
   }
   ```
2. **Server Response**:
   When `dominant_emotion` is `None`, `server.py` returns the exact message:
   ```text
   Invalid text! Please try again!
   ```

---

## Prerequisites & Installation

Ensure you have Python 3.8+ installed, then install required dependencies:

```bash
pip install flask requests pylint
```

---

## Unit Testing

Run the unit test suite containing 5 distinct test cases for Joy, Anger, Disgust, Sadness, and Fear:

```bash
python test_emotion_detection.py
```

### Expected Output:
```text
.....
----------------------------------------------------------------------
Ran 5 tests in 2.045s

OK
```

---

## Static Code Analysis (Pylint 10.00/10)

Verify PEP8 compliance and code quality using Pylint:

```bash
python -m pylint server.py
```

### Expected Output:
```text
--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```

You can also verify the `EmotionDetection` package:
```bash
python -m pylint EmotionDetection
```

---

## Running the Web Server

Start the Flask server on `0.0.0.0:5000`:

```bash
python server.py
```

Once running, navigate to:
- **Web UI**: `http://localhost:5000/` or `http://127.0.0.1:5000/`

---

## API & Web Usage Examples

### 1. Successful Analysis
- **URL**: `http://localhost:5000/emotionDetector?textToAnalyze=I%20am%20glad%20this%20happened`
- **Output**:
  ```text
  For the given statement, the system response is 'anger': 0.01, 'disgust': 0.01, 'fear': 0.01, 'joy': 0.95 and 'sadness': 0.01. The dominant emotion is joy.
  ```

### 2. Invalid / Blank Text
- **URL**: `http://localhost:5000/emotionDetector?textToAnalyze=`
- **Output**:
  ```text
  Invalid text! Please try again!
  ```
