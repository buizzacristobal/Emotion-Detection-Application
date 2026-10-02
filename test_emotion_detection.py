"""
Unit tests for the Emotion Detection application.
"""
import unittest
from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """
    Test suite for validating emotion detection results across 5 distinct emotions.
    """

    def test_joy(self):
        """
        Test case for detecting 'joy' as dominant emotion.
        """
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result['dominant_emotion'], 'joy')

    def test_anger(self):
        """
        Test case for detecting 'anger' as dominant emotion.
        """
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result['dominant_emotion'], 'anger')

    def test_disgust(self):
        """
        Test case for detecting 'disgust' as dominant emotion.
        """
        result = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result['dominant_emotion'], 'disgust')

    def test_sadness(self):
        """
        Test case for detecting 'sadness' as dominant emotion.
        """
        result = emotion_detector("I am so sad about this")
        self.assertEqual(result['dominant_emotion'], 'sadness')

    def test_fear(self):
        """
        Test case for detecting 'fear' as dominant emotion.
        """
        result = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result['dominant_emotion'], 'fear')


if __name__ == '__main__':
    unittest.main()
