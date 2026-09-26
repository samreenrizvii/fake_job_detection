# TrueJob: Fake Job Posting Detection

**A Machine Learning Project for Identifying Fraudulent Job Listings using NLP**

---

## 1. Abstract
The rapid growth of online job portals has unfortunately led to a corresponding increase in fraudulent job postings. These scams target vulnerable job seekers to extract personal information or money. This project, TrueJob, presents a machine learning-based approach to automatically detect fraudulent job listings. Using the Employment Scam Aegean Dataset (EMSCAD), we applied Natural Language Processing (NLP) techniques, specifically TF-IDF vectorization, to process the textual data. We evaluated four classification models: Logistic Regression, Naive Bayes, Random Forest, and Linear SVC. To address the severe class imbalance (only ~5% fraudulent jobs), we utilized balanced class weighting and prioritized the F1-Score and Recall metrics over standard accuracy. The Linear SVC model achieved the best performance with an F1-Score of 81.5%. Finally, a user-friendly interactive web dashboard was built using Python Dash, allowing users to analyze job postings in real-time.

## 2. Introduction
In today's digital era, the majority of job hunting happens online via platforms like LinkedIn, Indeed, and specialized portals. While this offers unprecedented convenience, it has also created a fertile ground for scammers. Fraudulent job postings are designed to look legitimate but are intended to steal identity details or solicit upfront payments for "training" or "equipment." The goal of this project is to build an automated, intelligent system that acts as a first line of defense for job seekers. 

## 3. Problem Statement
Job scams are difficult for the average applicant to spot because they often mimic the professional language of legitimate companies. Currently, there is a lack of accessible, real-time tools that job seekers can use to verify a listing before applying. The problem is fundamentally a text classification task, complicated by a severe class imbalance.

## 4. Objectives
*   To preprocess and extract meaningful features from unstructured job posting text using NLP techniques.
*   To train and compare multiple machine learning algorithms on highly imbalanced data.
*   To develop an automated pipeline that selects the best-performing model based on the F1-Score.
*   To create an interactive, web-based dashboard where users can input job descriptions and receive instant fraud predictions.

## 5. Literature / Background
Traditional spam detection relies heavily on keyword matching and Naive Bayes classifiers (commonly used in email). However, job postings contain complex, domain-specific language. Recent studies in text classification have shown that Support Vector Machines (SVM) perform exceptionally well in high-dimensional, sparse feature spaces created by TF-IDF (Term Frequency-Inverse Document Frequency) vectorization. 

## 6. Methodology
The project follows a standard Data Science lifecycle:
1.  **Data Acquisition:** Downloading the EMSCAD dataset.
2.  **Exploratory Data Analysis (EDA):** Understanding class distribution and identifying missing data.
3.  **Data Preprocessing:** Cleaning text and engineering a unified text feature.
4.  **Vectorization:** Converting text to numerical matrices using TF-IDF.
5.  **Model Training:** Training four distinct classification algorithms.
6.  **Evaluation & Selection:** Comparing models based on precision, recall, and F1-score.
7.  **Deployment:** Integrating the winning model into a Dash web application.

## 7. System Architecture
The system is divided into a modular pipeline:
*   `data_loader.py`: Handles file I/O, drops unnecessary IDs, and fills missing text values.
*   `preprocessor.py`: Cleans text (lowercasing, punctuation removal) and sets up the stratified train/test splits to maintain the 5% minority class ratio.
*   `models.py`: Defines the algorithms, applies `class_weight='balanced'`, trains the models, and saves the highest-scoring model as a `.pkl` file.
*   `train_pipeline.py`: The orchestrator script.
*   `app.py`: The Dash frontend that loads the serialized model and serves the UI.

## 8. Dataset Description
The Employment Scam Aegean Dataset (EMSCAD) contains approximately 17,880 records. It includes fields such as `title`, `location`, `company_profile`, `description`, `requirements`, and `benefits`. The target variable is `fraudulent` (binary). The dataset is highly imbalanced, with roughly 17,014 legitimate jobs and only 866 fraudulent jobs.

## 9. Data Preprocessing
Missing values in text columns were replaced with empty strings to avoid losing data rows. To maximize contextual understanding, the `title`, `company_profile`, `description`, `requirements`, and `benefits` columns were concatenated into a single `full_text` feature. 

## 10. Exploratory Data Analysis (EDA)
Initial EDA highlighted the massive class imbalance. If not addressed, this imbalance would cause models to predict "Legitimate" 100% of the time, achieving 95% accuracy while failing the core objective. 

## 11. Algorithms Used
1.  **Logistic Regression:** Used as a strong, interpretable baseline.
2.  **Naive Bayes (MultinomialNB):** The classic NLP classifier.
3.  **Random Forest:** An ensemble method tested for its robustness against non-linear patterns.
4.  **Linear SVC (Support Vector Classification):** Chosen for its proven effectiveness in high-dimensional sparse spaces (TF-IDF matrices).

## 12. Model Evaluation Strategy
Because of the 95/5 class imbalance, **Accuracy was rejected as the primary metric.** Instead, we focused on:
*   **Recall:** The percentage of actual scams successfully caught.
*   **Precision:** The percentage of flagged jobs that were actually scams.
*   **F1-Score:** The harmonic mean of Precision and Recall, serving as our primary metric for intelligent model selection.

## 13. Results
The models were evaluated on a stratified 20% test set.
*   **Logistic Regression:** Accuracy: 96.7% | F1-Score: 72.8% | Recall: 89.0%
*   **Naive Bayes:** Accuracy: 97.0% | F1-Score: 58.4% | Recall: 42.2%
*   **Random Forest:** Accuracy: 98.1% | F1-Score: 77.8% | Recall: 65.9%
*   **Linear SVC:** Accuracy: 98.1% | F1-Score: 81.4% | Recall: 82.6%

Linear SVC was automatically selected as the winner due to its superior F1-Score, balancing a high recall rate with excellent precision.

## 14. Dashboard
A web application was built using Python Dash and Dash Bootstrap Components. It features a "Cyborg" dark-mode theme to provide a premium user experience. The application includes a Home page highlighting project metrics, and a Prediction page for user interaction.

## 15. Prediction System
The Prediction page allows users to paste any job description into a text area. Upon clicking "Analyze," the text is passed through the saved TF-IDF vectorizer and the Linear SVC model. The UI instantly updates with a prominent, color-coded alert: a red warning for "Fraudulent" or a green check for "Legitimate."

## 16. Limitations
*   **Adversarial Evasion:** Scammers can bypass text-based models by replacing known trigger words with obscure synonyms or by embedding text in images.
*   **Context Dependency:** The model relies heavily on the vocabulary of the training set. It cannot verify external factors like the legitimacy of the company's email domain or website URL.

## 17. Future Scope
*   **Model Explainability:** Extracting SVC coefficients to highlight specific suspicious words directly in the UI.
*   **Advanced NLP:** Upgrading from TF-IDF to transformer-based models like BERT for deeper semantic understanding.
*   **Browser Extension:** Deploying the prediction pipeline as a Chrome extension to evaluate jobs automatically while the user browses LinkedIn or Indeed.

## 18. Conclusion
This project successfully demonstrates the application of Machine Learning and Natural Language Processing to solve a real-world security issue. By prioritizing appropriate evaluation metrics (F1-score) over misleading ones (accuracy), and handling imbalanced data through algorithmic weighting, we developed a highly capable fraud detection system. The accompanying web dashboard bridges the gap between raw ML code and practical user utility, proving the project's viability as an end-to-end data science solution.

## 19. References
1.  Amidi, A., & Amidi, S. (2019). Employment Scam Aegean Dataset (EMSCAD). *Kaggle*.
2.  Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*.
3.  Plotly Technologies Inc. (2023). Dash: Analytical Web Apps for Python.
