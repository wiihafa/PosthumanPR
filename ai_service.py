import os
import json
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

def analyze_response(response_text, peer_text):
    """
    Analyze a peer review response using OpenAI's GPT-4 model.
    Returns feedback and a score.
    """
    try:
        prompt = f"""Analyze this peer review response and provide constructive feedback.

Original Text: {peer_text}

Peer Review Response: {response_text}

Provide feedback in JSON format with:
1. A detailed analysis of the review's strengths and weaknesses
2. Specific suggestions for improvement
3. A score from 0 to 100
Format: {{"feedback": "string", "score": number}}"""

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return {
            "feedback": result["feedback"],
            "score": result["score"]
        }
    except Exception as e:
        raise Exception(f"Failed to analyze response: {e}")