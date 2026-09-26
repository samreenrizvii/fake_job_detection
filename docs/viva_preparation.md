# TrueJob: Viva Preparation Guide

This guide contains 60 questions categorized by difficulty, with answers written exactly how a 3rd-year B.Tech DS & AI student should explain them. 

---

## Part 1: Basic Questions (20)

**1. What is the title of your project and what does it do?**
"My project is called TrueJob. It's a machine learning web application that analyzes job postings and predicts whether they are legitimate or fraudulent job scams."

**2. Why did you choose this specific problem?**
"Job scams are a huge problem, especially for students and freshers applying online. I wanted to build something practical that actually protects people, rather than just doing a standard email spam classifier."

**3. What dataset did you use?**
"I used the Employment Scam Aegean Dataset (EMSCAD), which contains about 18,000 real and fake job postings. It has both text descriptions and categorical data like location and salary range."

**4. What is the target variable in your dataset?**
"The target variable is a binary column called 'fraudulent'. A 0 means the job is real, and a 1 means it's a fake or scam posting."

**5. Which programming language and libraries did you use?**
"I used Python. For data processing and machine learning, I used Pandas, NumPy, and Scikit-Learn. For the frontend dashboard, I used Dash and Dash Bootstrap Components."

**6. What is Exploratory Data Analysis (EDA)?**
"EDA is the process of looking at the data before feeding it to a model. In my project, it meant checking how many jobs were actually fake, looking for missing values, and seeing which words appeared most frequently in scams."

**7. Did you find any missing values in your data? How did you handle them?**
"Yes, a lot of text fields like 'company profile' or 'benefits' were empty. Instead of dropping those rows (which would lose valuable data), I simply filled them with an empty string, so the NLP model just treats it as blank text."

**8. What algorithms did you use?**
"I trained four models: Logistic Regression, Naive Bayes, Random Forest, and Linear Support Vector Classification (Linear SVC)."

**9. What is TF-IDF?**
"Machine learning models can't read text; they need numbers. TF-IDF stands for Term Frequency-Inverse Document Frequency. It converts words into numbers based on how often a word appears in a specific job posting versus how often it appears across *all* postings."

**10. Why use TF-IDF instead of just counting words?**
"If we just count words, common words like 'the' or 'and' get the highest scores. TF-IDF penalizes those common words and highlights words that are unique and actually carry meaning, like 'wire transfer' or 'urgent'."

**11. What is a train/test split?**
"It's when we divide our dataset into two parts. I used 80% of the data to teach (train) the model, and hid the remaining 20% to test the model later to see how well it learned."

**12. What does 'Stratified' split mean?**
"Since only 5% of my dataset is fake jobs, a random split might accidentally put all the fake jobs in the training set and none in the test set. Stratifying ensures that exactly 5% of both the train and test sets are fake jobs."

**13. What is Accuracy?**
"Accuracy is simply the percentage of total predictions the model got right. (Correct Predictions / Total Predictions)."

**14. Why is Accuracy a bad metric for this project?**
"Because 95% of the data is real jobs. A 'dumb' model that just guesses 'Real' every single time would get 95% accuracy, but it would catch exactly zero scams. So accuracy looks great, but the model is actually useless."

**15. What is Precision?**
"Precision means: out of all the jobs my model flagged as 'Fake', how many were *actually* fake? It measures how many false alarms we have."

**16. What is Recall?**
"Recall means: out of all the *real* fake jobs in the dataset, how many did my model successfully catch? This is crucial for my project because we don't want scams to slip through."

**17. What is the F1-Score?**
"It's the harmonic mean of Precision and Recall. It gives us a single number that balances the trade-off between catching scams (Recall) and not falsely accusing real jobs (Precision)."

**18. Which model performed the best?**
"Linear SVC performed the best. It achieved an F1-Score of about 81.5% and a Recall of 82.6%, meaning it caught the vast majority of scams with very few false alarms."

**19. What is a Confusion Matrix?**
"It's a table that shows the exact number of True Positives, True Negatives, False Positives, and False Negatives our model produced. It helps visualize exactly where the model is getting confused."

**20. What is Dash?**
"Dash is a Python framework built on top of Flask and React. It allowed me to build the interactive web dashboard purely in Python without needing to write complex JavaScript."

---

## Part 2: Intermediate Questions (20)

**21. Explain how Logistic Regression works for text classification.**
"Even though it's called regression, it's used for classification. It takes our TF-IDF word scores, applies weights to them, and pushes the sum through a Sigmoid function to output a probability between 0 and 1 (0 being real, 1 being fake)."

**22. How does Naive Bayes work? Why is it 'Naive'?**
"It calculates the probability of a job being fake based on the probabilities of the individual words in the text. It's 'naive' because it assumes every word is completely independent of the others, which isn't entirely true in human language, but it still works surprisingly well."

**23. Why did Naive Bayes perform poorly on Recall in your tests?**
"Naive Bayes often struggles with heavily imbalanced datasets unless carefully tuned. It became biased toward the majority class (Real jobs), so it was too hesitant to label something as Fake, leading to a low Recall score of 42%."

**24. What is a Random Forest?**
"It's an ensemble learning method. Instead of training one decision tree, it trains 100 different decision trees on random subsets of the data and features. When predicting, all 100 trees vote, and the majority wins. It prevents overfitting."

**25. How did you handle the severe class imbalance in your dataset?**
"This was a major challenge. I used the `class_weight='balanced'` parameter in Scikit-Learn for my Logistic Regression, Random Forest, and SVC models. This artificially increases the penalty if the model gets a 'Fake' job wrong, forcing the algorithm to pay 20x more attention to the minority class."

**26. What is Data Leakage?**
"Data leakage is when information from outside the training dataset is used to create the model. It's like giving a student the exam answers before the test."

**27. How did you prevent Data Leakage in your NLP pipeline?**
"I strictly used `fit_transform` on the training data, but only `transform` on the testing data. If I had fitted the TF-IDF vectorizer on the *entire* dataset before splitting, the vectorizer would have learned the vocabulary of the test set, which is a form of leakage."

**28. What are N-grams in your TF-IDF vectorizer?**
"N-grams are combinations of adjacent words. I used an `ngram_range=(1, 2)`. This means the model didn't just look at single words (unigrams), but also pairs of words (bigrams) like 'wire transfer' or 'bank account', which often contain strong signals for scams."

**29. What are Stop Words?**
"Stop words are common language words like 'is', 'the', 'and', 'a'. I removed them during preprocessing because they appear in both real and fake jobs equally, so they just add mathematical noise without helping the model classify."

**30. Why did you choose Linear SVC over a standard SVM with an RBF kernel?**
"Text data converted by TF-IDF has thousands of dimensions (features) but is very sparse (mostly zeros). In high-dimensional spaces, classes are usually linearly separable. Linear SVC is significantly faster and often more accurate for text than an RBF kernel."

**31. Explain the architecture of your project code.**
"I made it modular instead of using one notebook. I have a `src` folder containing `data_loader.py` for cleaning, `preprocessor.py` for NLP, and `models.py` for training. Then `train_pipeline.py` orchestrates them, and `app.py` runs the web interface."

**32. How does the 'Intelligent Model Selection' work in your code?**
"Instead of me hardcoding the best model, my script trains all four, calculates their metrics, stores them in a dictionary, and programmatically selects the model with the highest F1-Score. It then saves that specific model to disk."

**33. How do you save and load models in Python?**
"I used the `joblib` library. `joblib.dump()` serializes the trained model object into a `.pkl` file. Later, my Dash app uses `joblib.load()` to bring it back into memory to make predictions."

**34. Why did you combine the text features (title, description, etc.) into one column?**
"Scammers are unpredictable. Sometimes the scam is obvious in the 'company profile', sometimes in the 'requirements'. By concatenating them into one `full_text` column, the TF-IDF vectorizer gets the maximum context of the entire job posting."

**35. What is Overfitting?**
"Overfitting is when a model memorizes the training data perfectly (like scoring 100% on the training set) but fails completely on new, unseen data (the test set) because it didn't learn the underlying patterns, just the specific examples."

**36. Did your model overfit? How do you know?**
"No, because my test set metrics (F1-score of ~81%) remained high. If it had overfit, I would have seen 99% accuracy on the train set but maybe 40% on the test set."

**37. How did you test your Dash dashboard?**
"I ran the server locally on port 8050. I manually pasted text from known fake jobs in the dataset, and also text from legitimate LinkedIn jobs, to ensure the UI responded correctly and didn't crash on edge cases."

**38. What are Dash Callbacks?**
"Callbacks are Python functions that make the Dash app interactive. They listen for an 'Input' (like clicking the 'Analyze' button), process the data, and return an 'Output' (like updating the screen with the prediction result)."

**39. How would you handle a user pasting completely empty text into the dashboard?**
"In my Dash callback, I added input validation. If the string is empty or very short, it prevents the model from running and returns a warning alert telling the user to enter a valid description."

**40. What is a false positive in the context of this project?**
"A false positive is when the model flags a completely legitimate job posting as a 'Scam'. It's annoying for the employer, but generally less dangerous than a false negative (letting a scam slip through)."

---

## Part 3: Advanced Questions (20)

**41. If you had 1 million records instead of 18k, how would your algorithm choice change?**
"I would likely move away from standard Scikit-Learn models and use deep learning, specifically transformer models like BERT. I'd also have to use distributed computing frameworks like PySpark for data processing, as pandas would run out of RAM."

**42. How does the 'balanced' class weight actually work mathematically?**
"It alters the loss function during training. Normally, misclassifying a real job and a fake job adds the same penalty to the loss. 'Balanced' sets the weight inversely proportional to class frequencies: `n_samples / (n_classes * np.bincount(y))`. So misclassifying the minority class results in a much higher gradient penalty."

**43. Why did Random Forest underperform compared to Linear SVC on this text data?**
"Random Forest splits data based on feature thresholds. TF-IDF vectors are extremely sparse (thousands of features, but a single row only has non-zero values for 50 of them). Trees struggle to make good splits on sparse data compared to Linear SVC, which just draws a hyperplane through the high-dimensional space."

**44. What is Cross-Validation and did you use it?**
"Cross-validation involves splitting the training data into 'K' folds, training on K-1 folds, and validating on the remaining fold, repeating this K times. While I used a standard train/test split for the final pipeline for simplicity and speed, CV is the academically rigorous way to ensure the model's performance is stable across different subsets."

**45. Could you use Word2Vec or GloVe instead of TF-IDF? What's the difference?**
"Yes. TF-IDF just looks at word frequency; it doesn't understand context or synonyms (e.g., 'money' and 'cash' are treated as totally unrelated). Word2Vec creates dense vector embeddings where words with similar meanings are close together in space. It captures semantic meaning better, but requires more computational power and a different model architecture (like an LSTM)."

**46. How would you deploy this Dash application to the internet?**
"I would containerize the app using Docker to ensure environment consistency. Then, I could deploy the container to a cloud provider like AWS (using Elastic Beanstalk), Google Cloud Run, or a PaaS like Heroku. I'd use `gunicorn` as the WSGI HTTP server instead of the built-in Flask development server."

**47. What is Model Explainability, and how could you implement it for your Linear SVC?**
"Explainability tells the user *why* a decision was made. Since I used a Linear SVC with a TF-IDF vectorizer, I could extract the `.coef_` array from the model. By mapping those coefficients back to the vectorizer's vocabulary, I can show exactly which words had the highest positive weights pushing the decision toward 'Fraudulent'."

**48. What are the limitations of your current model?**
"First, it relies on the specific vocabulary of the training dataset. If scammers start using entirely new phrases, the model won't recognize them. Second, short job descriptions might not have enough text features to confidently classify. Third, it doesn't analyze the company's actual website or email domain."

**49. How would you handle concept drift in a real-world scenario?**
"Concept drift is when the patterns of fake jobs change over time as scammers adapt. I would implement an MLOps pipeline that continuously monitors the model's performance in production. Users could flag 'incorrect' predictions on the dashboard, and those flagged jobs would be reviewed and added to a new dataset to periodically retrain the model."

**50. What is the difference between stemming and lemmatization, and which is better?**
"Stemming roughly chops off the ends of words (e.g., 'running' becomes 'run', but 'caring' might become 'car'). Lemmatization uses a dictionary to reduce words to their actual root form (e.g., 'better' becomes 'good'). Lemmatization is better and more accurate, though slightly slower."

**51. How does the dimensionality of TF-IDF affect training time and memory?**
"If a dataset has 50,000 unique words, the TF-IDF matrix has 50,000 columns. This 'Curse of Dimensionality' uses massive RAM and exponentially increases training time. I handled this by setting `max_features=5000` in the vectorizer, keeping only the top 5000 most relevant terms."

**52. If a scammer knows how your model works, how could they bypass it?**
"This is an adversarial attack. If they know the model flags words like 'urgent wire', they will simply replace them with synonyms like 'immediate bank route' or bury the scam requirements in an image instead of text. This is why text-only models are vulnerable."

**53. How would you improve this project if you had 3 more months?**
"I would build a web scraper to pull live jobs from LinkedIn/Indeed to test real-time data. I would upgrade the NLP model from TF-IDF to a pre-trained BERT transformer. Finally, I would package the Dash app as a Chrome Extension so it warns users while they are browsing job sites."

**54. Explain the ROC-AUC score.**
"Receiver Operating Characteristic - Area Under Curve. It plots the True Positive Rate against the False Positive Rate at various probability thresholds. An AUC of 0.5 is random guessing, 1.0 is perfect. It measures how well the model separates the two classes."

**55. Why did you use `prevent_initial_call=True` in your Dash callback?**
"When a Dash app loads, callbacks usually fire once automatically with empty inputs. Since I don't want the model trying to predict an empty string the second the user opens the homepage, this parameter prevents that initial useless execution."

**56. Did you consider SMOTE for handling the imbalanced data?**
"SMOTE (Synthetic Minority Over-sampling Technique) creates fake synthetic examples of the minority class. While it works well for numerical data, applying SMOTE directly to sparse TF-IDF text matrices is mathematically problematic and often creates nonsensical 'frankenstein' text vectors. Using `class_weight='balanced'` is much safer and standard for text."

**57. What is the `dual=False` parameter in your LinearSVC?**
"In SVMs, you can solve either the primal or dual optimization problem. Scikit-learn recommends setting `dual=False` when the number of samples (18k) is greater than the number of features (5k). It makes the algorithm converge much faster."

**58. Could you combine multiple models? What is that called?**
"Yes, it's called an Ensemble, specifically a Voting Classifier or Stacking. I could have Logistic Regression, SVM, and Random Forest all make a prediction, and take the majority vote. It usually increases stability but makes the system slower and harder to explain."

**59. How would you measure the latency of your prediction pipeline?**
"I could use Python's `time` module to record the timestamp right before the text enters the vectorizer, and right after the model outputs the prediction. In production, I would log this latency to ensure the user isn't waiting more than 200-300 milliseconds for a result."

**60. Summarize what you learned from this project in one sentence.**
"I learned how to manage highly imbalanced text data, build modular ML pipelines to prevent data leakage, prioritize metrics like F1-score over accuracy, and wrap an ML model into a user-friendly web application."
