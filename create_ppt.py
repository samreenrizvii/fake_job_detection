from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import os

def apply_theme(slide):
    """Applies a professional dark theme background to the slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(24, 33, 45) # Professional Dark Navy Blue

def style_title(title_shape):
    """Styles the title text to be a modern cyan/teal color."""
    if not title_shape.has_text_frame:
        return
    for p in title_shape.text_frame.paragraphs:
        for run in p.runs:
            run.font.size = Pt(40)
            run.font.name = 'Segoe UI'
            run.font.bold = True
            run.font.color.rgb = RGBColor(64, 224, 208) # Turquoise / Cyan

def style_subtitle(subtitle_shape):
    if not subtitle_shape.has_text_frame:
        return
    for p in subtitle_shape.text_frame.paragraphs:
        for run in p.runs:
            run.font.size = Pt(22)
            run.font.name = 'Segoe UI'
            run.font.color.rgb = RGBColor(220, 220, 220)

def create_presentation():
    prs = Presentation()
    
    # --- 1. Title Slide ---
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    apply_theme(slide)
    
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "TrueJob: Fake Job Posting Detection"
    subtitle.text = "A Machine Learning approach using NLP\n\nPresented by: Arman Rizvi\n3rd Year B.Tech, Data Science & AI"
    
    style_title(title)
    style_subtitle(subtitle)

    # Helper function for content slides
    def add_slide(title_text, bullet_points):
        layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(layout)
        apply_theme(slide)
        
        title = slide.shapes.title
        title.text = title_text
        style_title(title)
        
        body_shape = slide.placeholders[1]
        tf = body_shape.text_frame
        tf.clear() # Clear default empty paragraph
        
        for point in bullet_points:
            p = tf.add_paragraph()
            p.text = point
            p.level = 0
            # Apply styling to body text
            for run in p.runs:
                run.font.size = Pt(22)
                run.font.name = 'Segoe UI'
                run.font.color.rgb = RGBColor(240, 240, 240) # Off-white for readability
            
    # --- 2. Problem Statement ---
    add_slide("Problem Statement", [
        "Online job portals are increasingly flooded with fraudulent listings.",
        "Scams target vulnerable job seekers to extract money or personal info.",
        "Traditional spam filters fail because scams use professional, legitimate-sounding language.",
        "There is an urgent need for an automated, NLP-based detection tool."
    ])

    # --- 3. Objectives ---
    add_slide("Project Objectives", [
        "Preprocess and extract features from unstructured job posting text.",
        "Train and compare multiple Machine Learning algorithms.",
        "Address severe class imbalance using mathematical weighting.",
        "Develop an automated pipeline for intelligent model selection.",
        "Build an interactive web dashboard for real-time predictions."
    ])

    # --- 4. The Dataset (EMSCAD) ---
    add_slide("Dataset: EMSCAD", [
        "Employment Scam Aegean Dataset (sourced from Kaggle).",
        "Total Records: ~17,880 job postings.",
        "Features used: Title, Company Profile, Description, Requirements, Benefits.",
        "Target Variable: 'fraudulent' (0 = Real, 1 = Fake).",
        "Challenge: Severe Imbalance. Only ~5% of jobs in the dataset are fraudulent."
    ])

    # --- 5. Data Preprocessing & NLP ---
    add_slide("Data Preprocessing & NLP", [
        "Missing Data: Filled empty text fields instead of dropping rows to preserve data.",
        "Feature Engineering: Concatenated all text features into a single 'full_text' column.",
        "NLP Cleaning: Converted to lowercase, removed punctuation and numbers.",
        "Vectorization: Used TF-IDF (Term Frequency-Inverse Document Frequency).",
        "N-grams: Extracted both unigrams and bigrams (e.g., 'wire transfer') for context."
    ])

    # --- 6. Machine Learning Algorithms ---
    add_slide("Algorithms Evaluated", [
        "1. Logistic Regression: A fast, interpretable baseline.",
        "2. Naive Bayes: The classic NLP text classifier.",
        "3. Random Forest: An ensemble method to capture non-linear patterns.",
        "4. Linear SVC: A Support Vector Machine optimized for sparse TF-IDF matrices.",
        "Crucial Step: Used 'class_weight=balanced' to force algorithms to penalize errors heavily on the minority class."
    ])

    # --- 7. Evaluation Metrics ---
    add_slide("Why Accuracy is Misleading", [
        "Because 95% of the data is Real, a 'dumb' model predicting 'Real' every time achieves 95% Accuracy.",
        "Therefore, we prioritized different metrics:",
        "Recall: Out of all actual scams, how many did we catch?",
        "Precision: Out of all flagged jobs, how many were actually scams?",
        "F1-Score: The harmonic mean of Precision and Recall. This was our primary metric for model selection."
    ])

    # --- 8. Training Results ---
    add_slide("Model Performance & Selection", [
        "Logistic Regression: Accuracy 96.7% | F1-Score 72.8%",
        "Naive Bayes: Accuracy 97.0% | F1-Score 58.4%",
        "Random Forest: Accuracy 98.1% | F1-Score 77.8%",
        "Linear SVC: Accuracy 98.1% | F1-Score 81.5% | Recall 82.6%",
        "Winner: Linear SVC. Automatically selected by the pipeline for achieving the highest F1-Score."
    ])

    # --- 9. Dash Web Application ---
    add_slide("Interactive Dashboard", [
        "Built using Python Dash and Dash Bootstrap Components.",
        "Features a 'Cyborg' dark-mode premium UI.",
        "Real-time Inference: Users paste a job description, and the backend vectorizes and predicts instantly.",
        "Model Insights: Visualizes exactly which words the model flagged as 'Fraudulent' based on SVC coefficients."
    ])

    # --- 10. Conclusion & Future Scope ---
    add_slide("Conclusion & Future Scope", [
        "Conclusion:",
        "- Successfully built an end-to-end ML pipeline.",
        "- Proved that Linear SVC outperforms others on sparse text data.",
        "- Demonstrated the danger of relying purely on Accuracy in imbalanced data.",
        "Future Scope:",
        "- Upgrade from TF-IDF to Transformer models (BERT).",
        "- Deploy as a Google Chrome browser extension for live web scanning."
    ])

    # Save the presentation
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'TrueJob_Presentation.pptx')
    prs.save(save_path)
    print(f"Presentation generated successfully at: {save_path}")

if __name__ == "__main__":
    create_presentation()
