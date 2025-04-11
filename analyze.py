import pandas as pd
from sqlalchemy import create_engine
from app.models import Feedback
from app import db

# Connect to the database
def get_feedback_data():
    feedbacks = Feedback.query.all()
    data = [{'college_id': feedback.college_id, 'comment': feedback.comment} for feedback in feedbacks]
    return pd.DataFrame(data)

# Analyze feedback and provide insights
def analyze_feedback():
    # Get feedback data from the database
    feedback_data = get_feedback_data()

    # Simple word count for each feedback
    feedback_data['word_count'] = feedback_data['comment'].apply(lambda x: len(x.split()))
    
    # Basic insights
    total_feedbacks = len(feedback_data)
    average_word_count = feedback_data['word_count'].mean()

    print(f"Total Feedbacks: {total_feedbacks}")
    print(f"Average Word Count per Feedback: {average_word_count:.2f}")
    
    # You can add more analysis here, such as sentiment analysis or specific word mentions.

if __name__ == '__main__':
    analyze_feedback()
