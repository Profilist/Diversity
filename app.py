import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt

st.title("Inclusive Language Checker")
st.write(
    "Ensure your corporate communication aligns with diversity and inclusivity standards."
    "Paste your text below to get suggestions on how to make it more inclusive!"
)

openai_api_key = st.secrets["default"]["openai_api_key"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "inclusivity_rating_before" not in st.session_state:
        st.session_state.inclusivity_rating_before = None

    st.write("### Paste your corporate communication here:")
    text_input = st.text_area("Enter your text", height=200)

    if st.button("Check for Inclusivity"):
        if text_input:
            st.write("#### Your Communication:")
            st.write(text_input)

            st.write("#### Inclusivity Rating:")
            fig, ax = plt.subplots()

            promptRating = (
                "Analyze the following corporate communication for non-inclusive language "
                "and give it a rating out of 100 (being the most inclusive), with the output being only a value like 60, "
                "you don't have to round it to the nearest tenth, just no decimals. "
                "For reference,  \n\n"
                f"{text_input}"
            )

            streamRating = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert on inclusive language."},
                    {"role": "user", "content": promptRating}
                ],
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

            prompt = (
                "Analyze the following corporate communication for non-inclusive language "
                "and provide suggestions for making it more inclusive. Format it using this example "
                "1. (tip 1).\n"
                "2. (tip 2).\n"
                "...\n"
                "(final text with improvements) \n\n"
                f"{text_input}"
            )

            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert on inclusive language."},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
            )

            with st.chat_message("assistant"):
                response_text = st.write_stream(stream)

        else:
            st.error("Please paste some text to check for inclusivity.")
