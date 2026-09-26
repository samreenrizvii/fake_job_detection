import os
import sys

# Ensure src/ is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_loader import load_and_clean_data
from src.preprocessor import get_train_test_splits, create_tfidf_vectorizer
from src.models import train_and_evaluate_models, select_best_model, save_model

def run_pipeline():
    print("🚀 Starting TrueJob Machine Learning Pipeline 🚀\n")
    
    # 1. Load Data
    data_path = "data/fake_job_postings.csv"
    try:
        df = load_and_clean_data(data_path)
    except FileNotFoundError as e:
        print(e)
        return

    # 2. Split Data (Stratified!)
    X_train_text, X_test_text, y_train, y_test = get_train_test_splits(df)
    
    # 3. Create Vectorizer and Transform Text
    print("\nVectorizing text using TF-IDF (This takes a few seconds)...")
    vectorizer = create_tfidf_vectorizer(max_features=5000, ngram_range=(1, 2))
    
    # Fit ONLY on training data to prevent Data Leakage!
    # Then transform both train and test.
    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)
    
    print(f"Text vocabulary size: {len(vectorizer.vocabulary_)} words/phrases.")
    
    # 4. Train and Evaluate Models
    print("\nTraining models. Brace yourself...")
    results, trained_models = train_and_evaluate_models(X_train, y_train, X_test, y_test)
    
    # 5. Select Best Model
    best_model_name, best_model = select_best_model(results, trained_models)
    
    # 6. Save for the Dashboard
    print("\nSaving the best model and vectorizer...")
    os.makedirs("models", exist_ok=True)
    save_model(best_model, vectorizer, 
               model_path="models/best_model.pkl", 
               vec_path="models/tfidf_vectorizer.pkl")
    
    print("\n✅ Pipeline complete! The model is ready for the Dash app.")

if __name__ == "__main__":
    run_pipeline()
