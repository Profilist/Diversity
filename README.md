# 🔍 Inclusivity Among Us

A **Streamlit** app that analyzes corporate communication for inclusivity and provides actionable suggestions to improve language. The app highlights non-inclusive phrases, rates the inclusivity of the text, and gives detailed feedback on how to make the communication more inclusive, ensuring alignment with diversity standards.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://inclusivity-among-us.streamlit.app/)

## Features

- **Inclusivity Rating**: Analyze corporate communication and receive a rating out of 100 to gauge inclusivity.
- **Detailed Feedback**: Provides suggestions on how to improve the language for inclusivity.
- **Highlight Problematic Text**: Automatically highlights non-inclusive text in dark red, making it easier for users to visualize areas that need improvement.
- **Multilingual Support**: Analyze text in multiple languages such as English, French, German, Chinese, and more.
- **Export to PDF**: Download the inclusivity report, including ratings and feedback, as a PDF.

## How to run it on your own machine

### 1. Install the requirements

To get started, first install the necessary Python libraries:

```bash
$ pip install -r requirements.txt
```

### 2. Add your OpenAI API Key

You need an OpenAI API key to run this app. Create a file called `.streamlit/secrets.toml` in your root directory and add your OpenAI API key like this:

```toml
[default]
openai_api_key = "your-openai-api-key"
```

### 3. Run the app
```bash
$ streamlit run app.py
```