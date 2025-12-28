import pandas as pd
from transformers import pipeline
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def analyze_feedback(csv_path=None):
    if csv_path is None:
        csv_path = os.path.join(config.DATA_DIR, "feedback_sample.csv")
    
    if not os.path.exists(csv_path):
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    
    # Use a smaller/faster model for analytics to keep it "student friendly"
    # or the one specified: cardiffnlp/twitter-roberta-base-sentiment-latest
    # We'll use a try-except to handle model download issues or just use a simple one
    try:
        sentiment_pipeline = pipeline("sentiment-analysis", 
                                    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                                    truncation=True, max_length=512)
        
        sentiments = []
        for complaint in df['complaint'].astype(str):
            # Simple truncation to avoid errors
            result = sentiment_pipeline(complaint[:512])
            sentiments.append(result[0]['label'])
        
        df['sentiment'] = sentiments
        
        # Return grouped data for plotting
        # count by category and sentiment
        return df
    except Exception as e:
        print(f"Analytics error: {e}")
        return df

if __name__ == "__main__":
    df = analyze_feedback()
    print(df.head())
