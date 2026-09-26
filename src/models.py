import time
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import cross_val_score

def train_and_evaluate_models(X_train, y_train, X_test, y_test):
    """
    Trains multiple models, evaluates them using our specific metrics,
    and returns a dictionary of their performances.
    """
    
    # We define the models we want to compare.
    # Note: Using class_weight='balanced' for Logistic Regression and SVM is CRITICAL
    # because our dataset only has ~5% fake jobs. This tells the algorithm to pay 20x more
    # attention to a fake job during training to balance the scales.
    models = {
        "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
        "Naive Bayes": MultinomialNB(),
        "Linear SVC": LinearSVC(class_weight='balanced', random_state=42, dual=False),
        "Random Forest": RandomForestClassifier(class_weight='balanced', n_estimators=100, random_state=42)
    }
    
    results = {}
    trained_models = {}
    
    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        start_time = time.time()
        
        # Train the model
        model.fit(X_train, y_train)
        
        training_time = time.time() - start_time
        
        # Make predictions on the test set
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        # We focus on the '1' class (Fraudulent jobs) because that's what we care about catching.
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        results[name] = {
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1-Score": f1,
            "Training Time (s)": round(training_time, 2)
        }
        trained_models[name] = model
        
        print(f"Accuracy: {accuracy:.4f} | F1-Score: {f1:.4f} | Recall: {recall:.4f}")
        
    return results, trained_models

def select_best_model(results, trained_models):
    """
    Intelligent Model Selection:
    Picks the best model based strictly on F1-Score, NOT Accuracy.
    """
    best_model_name = None
    best_f1 = -1
    
    for name, metrics in results.items():
        if metrics["F1-Score"] > best_f1:
            best_f1 = metrics["F1-Score"]
            best_model_name = name
            
    print(f"\n🏆 Automatic Model Selection Winner: {best_model_name} with F1-Score of {best_f1:.4f}")
    
    return best_model_name, trained_models[best_model_name]

def save_model(model, vectorizer, model_path="../models/best_model.pkl", vec_path="../models/tfidf_vectorizer.pkl"):
    """
    Saves the trained model and vectorizer so the Dash app can use them later.
    """
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)
    print(f"\nModel and Vectorizer saved successfully in the 'models/' folder.")

if __name__ == "__main__":
    print("This file contains the model training functions. Run train_pipeline.py to execute the full pipeline.")
