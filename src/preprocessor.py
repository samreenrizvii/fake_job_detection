import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

def clean_text(text):
    """
    Basic NLP text cleaning:
    - Lowercases text
    - Removes punctuation
    - Removes numbers (optional, but often good for text classification unless numbers mean something specific)
    - Removes extra whitespace
    """
    if not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers (scammers might use random numbers, but for words it's cleaner without)
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_train_test_splits(df, text_col='full_text', target_col='fraudulent', test_size=0.2, random_state=42):
    """
    Splits the data into training and testing sets.
    Critically, uses 'stratify' to ensure the 5% fake job ratio is maintained in both Train and Test.
    """
    # Apply the cleaning function to the dataset
    print("Applying text cleaning... (This might take a minute)")
    X_clean = df[text_col].apply(clean_text)
    y = df[target_col]
    
    # Stratified split to prevent data imbalance issues
    print("Splitting data into train and test sets (Stratified)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_clean, y, 
        test_size=test_size, 
        random_state=random_state, 
        stratify=y
    )
    
    return X_train, X_test, y_train, y_test

def create_tfidf_vectorizer(max_features=5000, ngram_range=(1, 2)):
    """
    Initializes a TF-IDF vectorizer.
    
    - max_features: Limits the vocabulary to the top 5000 words (saves memory and avoids noise).
    - ngram_range: (1, 2) means it looks at single words ("urgent") AND pairs of words ("wire transfer").
    - stop_words: 'english' removes common words like 'the', 'is', 'and' that don't add meaning.
    """
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        stop_words='english'
    )
    return vectorizer
