import pandas as pd
import numpy as np
import os

def load_and_clean_data(filepath):
    """
    Loads the job postings dataset and performs basic cleaning.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}. Please download it from Kaggle.")

    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Drop columns that are completely irrelevant for NLP or contain too many missing/unusable values
    # job_id is just an index. 
    columns_to_drop = ['job_id']
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # Many text columns might be NaN (empty). 
    # For a text classification model, it's best to fill empty strings with a space or placeholder 
    # rather than dropping the row, because the other columns might contain strong signals.
    text_columns = ['title', 'location', 'department', 'salary_range', 
                    'company_profile', 'description', 'requirements', 'benefits']
    
    for col in text_columns:
        df[col] = df[col].fillna('')

    # Create a single unified text feature
    # The intuition: Words indicating a scam could be in the title, the profile, or the description.
    # Combining them gives the TF-IDF vectorizer the full context.
    print("Combining text features into a single 'full_text' column...")
    df['full_text'] = (df['title'] + " " + 
                       df['company_profile'] + " " + 
                       df['description'] + " " + 
                       df['requirements'] + " " + 
                       df['benefits'])
    
    # We don't want excess whitespace
    df['full_text'] = df['full_text'].str.replace(r'\s+', ' ', regex=True).str.strip()

    # The target variable is 'fraudulent'
    return df

if __name__ == "__main__":
    # Test the loader if run directly
    data_path = "../data/fake_job_postings.csv"
    try:
        df_clean = load_and_clean_data(data_path)
        print("Data loaded successfully!")
        print(f"Total records: {len(df_clean)}")
        print(f"Class distribution:\n{df_clean['fraudulent'].value_counts(normalize=True) * 100}")
    except Exception as e:
        print(f"Error: {e}")
