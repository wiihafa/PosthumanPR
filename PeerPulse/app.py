import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Configuration
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "dev_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///peer_review.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)

# Import routes after app initialization to avoid circular imports
from models import Review, Prompt
from ai_service import analyze_response

# Sample prompts
SAMPLE_PROMPTS = [
    "What are the main strengths of your peer's argument?",
    "How could your peer improve their evidence and reasoning?",
    "Evaluate the clarity and organization of your peer's writing.",
    "Assess the effectiveness of your peer's introduction and conclusion."
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "POST":
        peer_text = request.form.get("peer_text")
        prompt_id = request.form.get("prompt_id")
        response = request.form.get("response")

        if not all([peer_text, prompt_id, response]):
            flash("Please fill out all fields", "error")
            return redirect(url_for("review"))

        # Analyze the response using OpenAI
        try:
            analysis = analyze_response(response, peer_text)

            # Save the review
            review = Review(
                peer_text=peer_text,
                prompt_id=prompt_id,
                response=response,
                feedback=analysis.get("feedback"),
                score=analysis.get("score", 0)
            )
            db.session.add(review)
            db.session.commit()

            session["last_review_id"] = review.id
            return redirect(url_for("feedback"))

        except Exception as e:
            app.logger.error(f"Error analyzing response: {e}")
            flash("An error occurred while analyzing your response. Please try again.", "error")
            return redirect(url_for("review"))

    # Create enumerated prompts list for the template
    enumerated_prompts = list(enumerate(SAMPLE_PROMPTS, 1))  # Start counting from 1
    return render_template("review.html", prompts=enumerated_prompts)

@app.route("/feedback")
def feedback():
    review_id = session.get("last_review_id")
    if not review_id:
        return redirect(url_for("review"))
    
    review = Review.query.get_or_404(review_id)
    return render_template("feedback.html", review=review)

with app.app_context():
    db.create_all()
    
    # Initialize prompts if none exist
    if not Prompt.query.first():
        for prompt_text in SAMPLE_PROMPTS:
            prompt = Prompt(text=prompt_text)
            db.session.add(prompt)
        db.session.commit()