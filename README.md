# TrueJob: Fake Job Posting Detection 🛡️

Catching job scams before they catch you. TrueJob is an end-to-end Machine Learning web application designed to automatically detect fraudulent job postings using Natural Language Processing (NLP).

## 📊 Data Source
This project uses the **Employment Scam Aegean Dataset (EMSCAD)**, which is publicly available on Kaggle as the [Real or Fake: Fake JobPosting Prediction Dataset](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction). It contains ~18,000 real and fraudulent job descriptions.

## ✨ Features
*   **NLP Text Processing:** Uses TF-IDF vectorization with N-grams to analyze the semantic meaning of job descriptions, company profiles, and requirements.
*   **Intelligent Model Selection:** Automatically trains multiple classification models (Logistic Regression, Naive Bayes, Random Forest, Linear SVC) and selects the best performer based on the F1-Score to handle severe class imbalance.
*   **Interactive Dashboard:** A sleek, dark-mode Python Dash web application for real-time inference. Paste any job posting and instantly see if it's legitimate or a scam.

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.8+ installed.

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/TrueJob.git
cd TrueJob
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the Data
1. Download the `fake_job_postings.csv` file from the [Kaggle Dataset Link](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction).
2. Place the CSV file inside the `data/` folder in the root of this project.

### 4. Train the Model
Run the machine learning pipeline to clean the data, train the models, and save the best performing model:
```bash
python train_pipeline.py
```
*Note: This will generate `best_model.pkl` and `tfidf_vectorizer.pkl` inside the `models/` directory.*

### 5. Launch the Dashboard
Start the interactive web application:
```bash
python dashboard/app.py
```
Open your browser and navigate to `http://127.0.0.1:8050/`.

## 📂 Project Structure
```text
TrueJob/
│
├── data/                  # Contains the raw CSV dataset
├── src/                   
│   ├── data_loader.py     # Data loading and initial cleaning
│   ├── preprocessor.py    # NLP text cleaning and TF-IDF setup
│   └── models.py          # Model training, evaluation, and selection
├── models/                # Saved serialized ML models (.pkl)
├── dashboard/             
│   └── app.py             # Dash web application code
├── requirements.txt       # Python dependencies
├── train_pipeline.py      # Master script to run the ML pipeline
└── README.md              # Project documentation
```

## 📈 Evaluation Metrics
Because fraudulent jobs only make up ~5% of the dataset, accuracy is a misleading metric. This project prioritizes **Recall** (catching actual scams) and the **F1-Score** (balancing false alarms). The selected `Linear SVC` model achieved an impressive F1-Score of **81.5%** with a Recall of **82.6%**.

## 👨‍💻 Author
**[Samreen Rizvi]** 
