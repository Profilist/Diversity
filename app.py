import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt
from fpdf import FPDF
import io 
import re

st.set_page_config(
    page_title="Inclusivity Among Us",
)

st.title("Inclusivity Among Us")
st.write(
    "Ensure your corporate communication aligns with diversity and inclusivity standards. "
    "Paste your text below to get suggestions on how to make it more inclusive!"
)

if "rating_before" not in st.session_state:
    st.session_state.rating_before = None
if "response_text" not in st.session_state:
    st.session_state.response_text = None

openai_api_key = st.secrets["default"]["openai_api_key"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    client = OpenAI(api_key=openai_api_key)
    
    languages = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Chinese": "zh",
        "Japanese": "ja",
        "Korean": "ko",
        "Portuguese": "pt",
        "Italian": "it"
    }
    
    selected_language = st.selectbox("Select language", options=list(languages.keys()))
    language_code = languages[selected_language]

    st.write("### Paste your corporate communication here:")
    text_input = st.text_area("Enter your text", height=200)

    if st.button("Check for Inclusivity"):
        if text_input:
            st.write("#### Inclusivity Rating:")
            fig, ax = plt.subplots()

            promptRating = (
                f"Analyze the following corporate communication for inclusivity and provide a rating out of 100, "
                f"where 100 indicates the highest level of inclusivity. Focus only on significant inclusivity issues "
                f"and avoid nitpicking trivial or stylistic word choices. The analysis should be done in {selected_language}. "
                f"If the text is largely inclusive (above 90%), avoid lowering the rating unless there are clear exclusionary elements or biases. "
                f"The output should not include anything other than a single integer value, like 90, without decimal points.\n\n"
                f"Text in {selected_language}:\n{text_input}"
            )

            streamRating = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert in evaluating inclusive language in {selected_language}."},
                    {"role": "user", "content": promptRating}
                ],
                temperature=0.5,  
                max_tokens=50,  
                stream=True,
            )

            rating_before = int("".join(chunk.choices[0].delta.content for chunk in streamRating if getattr(chunk.choices[0].delta, "content", None)).strip())
            st.session_state.rating_before = rating_before

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
                f"Analyze the following corporate communication in {selected_language} for non-inclusive language "
                f"and provide specific tips for making it more inclusive and professional. "
                f"Your response should be concise, and for each tip, provide an example from the text and a suggested improvement "
                f"only if a meaningful change is necessary. Avoid suggesting trivial changes such as replacing synonyms or suggesting changes where the text is already inclusive. "
                f"If no meaningful improvement is needed, do not provide a tip for that part of the text. Do not make a suggestion that does not change anything. "
                f"Use the following format for your response:\n"
                "1. (Tip)\n"
                "   Example: \"(example from text)\"\n"
                "   Suggestion: \"(how to improve it)\"\n"
                "2. (Tip)\n"
                "   Example: \"(example from text)\"\n"
                "   Suggestion: \"(how to improve it)\"\n"
                "...\n"
                "At the end, provide the original text and then the final improved text with all the suggested fixes applied, if any are needed.\n\n"
                f"Text to analyze in {selected_language}:\n{text_input}"
            )

            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert in inclusive language and communication. Your task is to provide concise, actionable suggestions for improving inclusivity in the provided text, following a specific format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5, 
                max_tokens=300,  
                stream=True,
            )
            
            response_chunks = [chunk.choices[0].delta.content for chunk in stream if getattr(chunk.choices[0].delta, "content", None)]
            response_text = "".join(response_chunks)
            st.session_state.response_text = response_text
            
            st.write(response_text)
            

            st.write("### Specific Changes:")
            
            def extract_flagged_words(response_text):
                flagged_words = []
                tips = re.findall(r'Example: "(.*?)"', response_text)
                for tip in tips:
                    flagged_words.append(tip)
                return flagged_words

            flagged_words = extract_flagged_words(st.session_state.response_text)
            
            def highlight_text(original_text, flagged_words):
                color = '#8B0000' 

                for word in flagged_words:
                    original_text = re.sub(f"({word})", rf'<span style="background-color:{color};">\1</span>', original_text, flags=re.IGNORECASE)

                return original_text

            highlighted_text = highlight_text(text_input, flagged_words)
            
            st.markdown(highlighted_text, unsafe_allow_html=True)
            
    if st.session_state.rating_before and st.session_state.response_text:
        if st.button('Export Report to PDF'):
            report_text = f"Inclusivity Rating: {st.session_state.rating_before}\n\n" + st.session_state.response_text
            
            buffer = io.BytesIO()

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(200, 10, txt="Inclusivity Report", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font('Arial', '', 12)
            pdf.multi_cell(200, 10, txt=report_text)

            pdf_output = pdf.output(dest='S').encode('latin1')  
            buffer.write(pdf_output)

            st.download_button(
                label="Download PDF",
                data=buffer.getvalue(),
                file_name="Inclusivity_Report.pdf",
                mime="application/pdf"
            )

