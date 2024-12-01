from flask import Flask, request, jsonify
import speech_recognition as sr
from transformers import pipeline

app = Flask(__name__)


sentiment_model = pipeline("sentiment-analysis")


affirmations = {
    "positive": ["You're doing amazing! Keep shining!", "Positivity radiates from you."],
    "neutral": ["Every day is a new opportunity.", "You have the power to make today great."],
    "negative": ["It's okay to feel this way; brighter days are ahead.", "You are stronger than you realize."]
}

@app.route('/process_voice', methods=['POST'])
def process_voice():
    try:
       
        audio_file = request.files['file']

       
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            user_text = recognizer.recognize_google(audio_data)

       
        analysis = sentiment_model(user_text)[0]
        sentiment = analysis['label'].lower()
        confidence = round(analysis['score'] * 100, 2)

     
        selected_affirmation = affirmations.get(sentiment, ["Stay strong, you're doing great!"])[0]

        response = {
            "transcribed_text": user_text,
            "sentiment": sentiment,
            "confidence": confidence,
            "affirmation": selected_affirmation
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
