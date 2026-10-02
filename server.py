"""
Emotion Detection Server.

This Flask application serves the Emotion Detection web interface and provides
an API endpoint to analyze text emotions using the Watson NLP service.
"""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/")
def render_index_page():
    """
    Renders the index.html template for the main web application page.
    """
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_endpoint():
    """
    Analyzes the emotion of the provided text query parameter.

    Query Parameters:
        textToAnalyze (str): The text input to be analyzed.

    Returns:
        str: A formatted string containing scores for anger, disgust, fear, joy,
             sadness, and dominant_emotion, or an error message if invalid.
    """
    text_to_analyze = request.args.get("textToAnalyze", "")
    response = emotion_detector(text_to_analyze)

    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        f"For the given statement, the system response is 'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, 'fear': {response['fear']}, "
        f"'joy': {response['joy']} and 'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
