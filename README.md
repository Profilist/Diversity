# 🔍 Inclusivity Among Us

A **Streamlit** app designed to help communities embrace diversity and inclusivity. This tool analyzes text and provides actionable suggestions to ensure that the language used is inclusive, addressing important topics like race, gender expression, disability, and educational attainment. The app highlights non-inclusive phrases, rates the inclusivity of the content, and offers detailed feedback on how to make the communication more aligned with diversity standards.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://inclusivity-among-us.streamlit.app/)

## Features

- **Inclusivity Rating**: Analyze any type of community-related content (policies, announcements, or communication) and receive a rating out of 100 to gauge how inclusive it is.
- **Detailed Feedback**: Provides concrete suggestions on how to improve the inclusivity of language, touching on areas such as race, gender expression, disability, and educational attainment.
- **Highlight Problematic Text**: Automatically highlights non-inclusive language in dark red, making it easy to visualize where improvements can be made.
- **Multilingual Support**: Analyze text in multiple languages such as English, French, German, Chinese, and more.
- **Export to PDF**: Download the inclusivity report, including ratings and feedback, as a PDF.
- **Community-Focused**: Built to reflect and encourage the change we want to see in our communities by promoting diverse and inclusive language.

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