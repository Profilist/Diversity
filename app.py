import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt

st.set_page_config(
        page_title="Inclusivity Among Us",
)

st.title("Inclusivity Among Us")
st.write(
    "Ensure your corporate communication aligns with diversity and inclusivity standards. "
    "Paste your text below to get suggestions on how to make it more inclusive!"
)

openai_api_key = st.secrets["default"]["openai_api_key"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    client = OpenAI(api_key=openai_api_key)

    st.write("### Paste your corporate communication here:")
    text_input = st.text_area("Enter your text", height=200)

    if st.button("Check for Inclusivity"):
        if text_input:
            st.write("#### Inclusivity Rating:")
            fig, ax = plt.subplots()

            promptRating = (
                "Analyze the following corporate communication for inclusivity and provide a rating out of 100, "
                "where 100 indicates the highest level of inclusivity. Focus only on significant inclusivity issues and avoid nitpicking trivial or stylistic word choices. "
                "If the text is largely inclusive (above 90%), avoid lowering the rating unless there are clear exclusionary elements or biases. "
                "The output should not include anything other than a single integer value, like 90, without decimal points.\n\n"
                f"{text_input}"
            )

            streamRating = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in evaluating inclusive language in corporate communications. Your task is to provide a clear and accurate inclusivity rating based on significant language choices."},
                    {"role": "user", "content": promptRating}
                ],
                temperature=0.5,  
                max_tokens=50,  
                stream=True,
            )

            rating_before = int("".join(chunk.choices[0].delta.content for chunk in streamRating if getattr(chunk.choices[0].delta, "content", None)).strip())

            sizes = [rating_before, 100 - rating_before]
            labels = ['Inclusive', 'Non-Inclusive']
            colors = ['#4CAF50', '#FF6347']  
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, 
                   textprops={'color': 'white'})
            ax.axis('equal') 
            fig.patch.set_facecolor('#0e1118')
            st.pyplot(fig)

            st.write("#### Tips:")
            prompt = (
                "Analyze the following corporate communication for non-inclusive language "
                "and provide specific tips for making it more inclusive and professional. "
                "Your response should be concise, and for each tip, provide an example from the text and a suggested improvement "
                "only if a meaningful change is necessary. Avoid suggesting trivial changes such as replacing synonyms or suggesting changes where the text is already inclusive. "
                "If no meaningful improvement is needed, do not provide a tip for that part of the text. Do not make a suggestion that does not change anything. "
                "Use the following format for your response:\n"
                "1. (tip)\n"
                "   Example: \"(example from text)\"\n"
                "   Suggestion: \"(how to improve it)\"\n"
                "2. (tip)\n"
                "   Example: \"(example from text)\"\n"
                "   Suggestion: \"(how to improve it)\"\n"
                "...\n"
                "At the end, provide the original text and then the final improved text with all the suggested fixes applied, if any are needed.\n\n"
                f"Text to analyze:\n{text_input}"
            )

            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in inclusive language and communication. Your task is to provide concise, actionable suggestions for improving inclusivity in the provided text, following a specific format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5, 
                max_tokens=300,  
                stream=True,
            )

            # response_chunks = [chunk.choices[0].delta.content for chunk in stream if getattr(chunk.choices[0].delta, "content", None)]
            # response_text = "".join(response_chunks)

            st.write(stream)

        else:
            st.error("Please paste some text to check for inclusivity.")
