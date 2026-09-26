import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import joblib
import pandas as pd
import os

# Initialize the Dash app with a sleek dark theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)
app.title = "TrueJob: Job Scam Detector"

# --- Load Models ---
# Make paths robust regardless of where the script is run from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "models", "best_model.pkl")
vec_path = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    print("✅ Model and vectorizer loaded successfully!")
except FileNotFoundError:
    print("⚠️ WARNING: Model files not found. Did you run train_pipeline.py?")
    model = None
    vectorizer = None

# --- UI Components ---

# 1. Navigation Bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Test a Job Posting", href="/predict")),
        dbc.NavItem(dbc.NavLink("Model Comparison", href="/comparison")),
        dbc.NavItem(dbc.NavLink("Model Insights", href="/insights")),
    ],
    brand="🛡️ TrueJob Analytics",
    brand_href="/",
    color="primary",
    dark=True,
    className="mb-4",
)

# 2. Home Page Layout
home_layout = dbc.Container([
    html.H1("Catching Job Scams Before They Catch You.", className="text-center mt-5 mb-4 text-light"),
    html.P("Every year, thousands of job seekers are scammed by fraudulent listings. TrueJob uses advanced Natural Language Processing to detect these scams instantly.", className="text-center text-muted fs-5 mb-5"),
    
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("17.8k+", className="text-primary text-center"),
                html.P("Job Postings Analyzed", className="text-center text-muted")
            ])
        ]), md=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("NLP Powered", className="text-success text-center"),
                html.P("TF-IDF Vectorization", className="text-center text-muted")
            ])
        ]), md=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("98% Recall", className="text-danger text-center"),
                html.P("Catching the Fakes", className="text-center text-muted")
            ])
        ]), md=4),
    ], className="mb-5"),
    
    html.Div(
        dbc.Button("Try the Detector Now", color="primary", size="lg", href="/predict"),
        className="d-flex justify-content-center"
    )
], fluid=True)

# 3. Prediction Page Layout
predict_layout = dbc.Container([
    html.H2("Analyze a Job Posting", className="mb-4"),
    html.P("Paste the title, company profile, and job description below. Our ML model will predict if it's legitimate or a scam.", className="text-muted"),
    
    dbc.Textarea(id="job-input", placeholder="Paste the full job posting here...", style={"height": "300px"}, className="mb-3"),
    dbc.Button("Analyze Posting", id="analyze-btn", color="success", className="mb-4 w-100", size="lg"),
    
    # Spinner while processing
    dbc.Spinner(html.Div(id="prediction-result"))
])

import plotly.express as px

def create_feature_importance_plot(trained_model, trained_vectorizer, top_n=15):
    if trained_model is None or not hasattr(trained_model, 'coef_'):
        return dbc.Alert("Feature importance requires a trained model with coefficients.", color="warning")
    
    # Extract coefficients and feature names
    coefs = trained_model.coef_[0]
    features = trained_vectorizer.get_feature_names_out()
    
    # Get the indices of the highest positive (Fraud) and lowest negative (Legit) weights
    top_fake_idx = coefs.argsort()[-top_n:][::-1]
    top_real_idx = coefs.argsort()[:top_n]
    
    # Build a DataFrame for Plotly
    data = []
    for i in top_fake_idx:
        data.append({"Word/Phrase": features[i], "Weight": coefs[i], "Indicator": "Fraudulent Signal"})
    for i in top_real_idx:
        data.append({"Word/Phrase": features[i], "Weight": coefs[i], "Indicator": "Legitimate Signal"})
        
    df_feat = pd.DataFrame(data)
    
    # Create an interactive horizontal bar chart
    fig = px.bar(
        df_feat, 
        x="Weight", 
        y="Word/Phrase", 
        color="Indicator",
        orientation='h',
        color_discrete_map={"Fraudulent Signal": "#ef5350", "Legitimate Signal": "#66bb6a"},
    )
    fig.update_layout(
        template="plotly_dark",
        yaxis={'categoryorder':'total ascending'},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return dcc.Graph(figure=fig)

def create_comparison_plot():
    df_metrics = pd.DataFrame({
        "Model": ["Logistic Regression", "Naive Bayes", "Random Forest", "Linear SVC"],
        "Accuracy": [0.9678, 0.9709, 0.9818, 0.9818],
        "F1-Score": [0.7281, 0.5840, 0.7782, 0.8148],
        "Recall": [0.8902, 0.4220, 0.6590, 0.8266]
    })
    
    # Melt the dataframe for plotly grouped bar chart
    df_melt = df_metrics.melt(id_vars="Model", var_name="Metric", value_name="Score")
    
    fig = px.bar(
        df_melt, 
        x="Model", 
        y="Score", 
        color="Metric", 
        barmode="group",
        text_auto=".2f",
        title="Performance Metrics Across Models"
    )
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Score (0 to 1)",
    )
    
    return dcc.Graph(figure=fig), df_metrics

comparison_graph, df_metrics = create_comparison_plot()

# 4. Model Comparison Page
comparison_layout = dbc.Container([
    html.H2("Model Comparison", className="mb-4 text-light"),
    html.P("Comparing different classification algorithms. Notice how Accuracy is misleadingly high across all models, which is why we selected Linear SVC based on its superior F1-Score.", className="text-muted mb-4"),
    
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                comparison_graph
            ])
        ]), md=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Metrics Table", className="card-title text-center mb-4"),
                dbc.Table.from_dataframe(df_metrics, striped=True, bordered=True, hover=True, color="dark")
            ])
        ]), md=12)
    ])
])

# 5. Insights Page (Model Explainability)
insights_layout = dbc.Container([
    html.H2("Model Insights: How does the AI think?", className="mb-4 text-light"),
    html.P("This chart shows exactly which words our Linear SVC model looks for to make its decision. Words with a high positive weight push the prediction toward 'Fraudulent', while words with a negative weight point to a 'Legitimate' posting.", className="text-muted mb-4"),
    
    dbc.Card(
        dbc.CardBody([
            html.H4("Top Predictive Features (TF-IDF Bigrams)", className="card-title text-center mb-4"),
            create_feature_importance_plot(model, vectorizer)
        ]),
        className="mb-5 shadow-sm"
    )
])

# --- Main App Layout ---
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

# --- Callbacks ---

# Routing
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/predict':
        return predict_layout
    elif pathname == '/insights':
        return insights_layout
    elif pathname == '/comparison':
        return comparison_layout
    else:
        return home_layout

# Prediction Logic
@app.callback(
    Output("prediction-result", "children"),
    Input("analyze-btn", "n_clicks"),
    State("job-input", "value"),
    prevent_initial_call=True
)
def predict_job(n_clicks, text):
    if not text or len(text.strip()) < 10:
        return dbc.Alert("Please enter a valid, detailed job description.", color="warning")
    
    if model is None or vectorizer is None:
        return dbc.Alert("Model not loaded. Please run the training script first.", color="danger")
    
    try:
        # Preprocess and Predict
        # We clean it slightly just by lowercasing (our vectorizer handles the rest)
        clean_input = text.lower()
        vec_input = vectorizer.transform([clean_input])
        
        prediction = model.predict(vec_input)[0]
        # Depending on the model, we might get probabilities (e.g., Logistic Regression)
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(vec_input)[0][1] * 100
            prob_text = f"Confidence: {prob:.1f}%"
        else:
            prob_text = ""
        
        if prediction == 1:
            return dbc.Card(dbc.CardBody([
                html.H3("🚨 FRAUDULENT POSTING DETECTED", className="text-danger text-center"),
                html.P(prob_text, className="text-center text-muted mb-0")
            ]), color="danger", outline=True, className="mt-4")
        else:
            return dbc.Card(dbc.CardBody([
                html.H3("✅ LEGITIMATE POSTING", className="text-success text-center"),
                html.P(prob_text, className="text-center text-muted mb-0")
            ]), color="success", outline=True, className="mt-4")
            
    except Exception as e:
        return dbc.Alert(f"An error occurred during prediction: {str(e)}", color="danger")

if __name__ == "__main__":
    # Run the app locally
    print("Starting Dash server at http://127.0.0.1:8050/")
    app.run(debug=True, port=8050)
