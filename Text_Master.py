import streamlit as st
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerVectors_core import VectorDatabase
import tempfile
import fitz
import docx
from PIL import Image
from embeddings import generate_embeddings_open_ai, generate_text
from chunker import chunk_by_max_chunk_size
import os
import pyttsx3  # type: ignore

# Set up the Streamlit app configuration
st.set_page_config(page_title="Text Master", page_icon=":memo:")

# Sidebar setup
with st.sidebar:
    st.title("Model Selection")
    model_choice = st.selectbox("Select LLM Model", ["OpenAI GPT-3.5-turbo", "OpenAI GPT-4", "Gemini"])
    st.markdown("<hr>", unsafe_allow_html=True)
    save_content = st.checkbox("Allow saving content in memory", value=False)
    st.markdown(
        "<p style='font-size: 12px; color: #6c757d;'>If you option not to save the content, the uploaded file will be deleted after processing.</p>",
        unsafe_allow_html=True
    )
    # api_key = st.text_input("Enter your API key", type="password")

    # if not api_key:
    #     st.warning("Please enter your API key to proceed.")
    #     st.stop()

# Initialize OpenAI client
# openai_client = OpenAI(api_key=api_key)

# Initialize the selected language model
if model_choice == "OpenAI GPT-3.5-turbo":
    model_name = "gpt-3.5-turbo"
    Phd = LLM.create(LLMProvider.OPENAI, model_name=model_name)
elif model_choice == "OpenAI GPT-4":
    model_name = "gpt-4"
    Phd = LLM.create(LLMProvider.OPENAI, model_name=model_name)
elif model_choice == "Gemini":
    model_name = "gemini-pro"
    Phd = LLM.create(LLMProvider.GEMINI, model_name=model_name)

# Page title and header
st.image("textmaster.png", use_column_width=True)
st.markdown("<h1 style='text-align: left;'>Text Master</h1>", unsafe_allow_html=True)
st.subheader("Your Gateway to Advanced Text Processing")

st.markdown("""
    <style>
    .header-title { font-size: 36px; font-weight: bold; color: #4CAF50; }
    .subheader-title { font-size: 24px; font-weight: bold; color: #2F4F4F; }
    .footer-text { font-size: 14px; color: #808080; text-align: center; }
    .centered-footer { display: flex; justify-content: center; }
    .dark-blue { color: #141C46; }
    .alert { background-color: #f8f9fa; color: #6c757d; padding: 10px; border-radius: 5px; border: 1px solid #ced4da; margin-bottom: 20px; }
    .btn-container { display: flex; flex-direction: column; align-items: center; }
    .btn-container > button { width: 100%; margin: 5px 0; }
    .caption { font-size: 12px; color: #6c757d; text-align: center; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title dark-blue">Upload a text file (PDF, TXT, DOCX) and get a summarized version of its content using the selected LLM model.</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"], help="Upload a PDF, TXT, or DOCX file for summarization")

def read_text_file(file_path, encodings=["utf-8", "latin1", "cp1252"]):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to decode text file with provided encodings")

def read_pdf_file(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def read_docx_file(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def generate_tts(text, filename="output.mp3"):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    try:
        if uploaded_file.type == "text/plain":
            content = read_text_file(tmp_file_path)
        elif uploaded_file.type == "application/pdf":
            content = read_pdf_file(tmp_file_path)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            content = read_docx_file(tmp_file_path)
        else:
            raise ValueError("Unsupported file type")

        st.markdown('<div class="subheader-title">File Content Preview</div>', unsafe_allow_html=True)
        st.text_area("File Content", content, height=300)

        st.markdown('<div class="subheader-title">Customize Your Summary</div>', unsafe_allow_html=True)
        summary_length = st.slider("Summary Length (in sentences)", min_value=1, max_value=10, value=5)
        summarized_text = Phd.generate_response(prompt=f"Summarize the following text to bullet points in {summary_length} sentences, content: {content}")

        st.markdown('<div class="subheader-title">Summarized Text</div>', unsafe_allow_html=True)
        st.write(summarized_text)
        
        st.download_button(label="Download Summary", data=summarized_text, file_name="summary.txt", mime="text/plain", key="download-summary-btn")

        st.markdown('<div class="subheader-title">Advanced Text Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="btn-container">', unsafe_allow_html=True)

        if st.button("Perform Sentiment Analysis", key="sentiment-analysis-btn"):
            sentiment_result = Phd.generate_response(prompt=f"Perform sentiment analysis on the following text: {content}")
            st.write("Sentiment Analysis Result")
            st.write(sentiment_result)

        if st.button("Keywords Extraction", key="extract-keywords-btn"):
            keywords_result = Phd.generate_response(prompt=f"Extract keywords from the following text: {content}")
            st.write("Keywords Extraction Result")
            st.write(keywords_result)

        if st.button("Language Translation", key="language-translation-btn"):
            translated_results = Phd.generate_response(prompt=f"Translate the following text into French: {content}")
            st.write("Translated Text")
            st.write(translated_results)

        if st.button("Summarized Text Translation", key="summarized-text-translation-btn"):
            summarized_translated_results = Phd.generate_response(prompt=f"Translate the following text into French: {summarized_text}")
            st.write("Translated Summarized Text")
            st.write(summarized_translated_results)

        if st.button("Summarized Text to Speech", key="text-to-speech-btn"):
            generate_tts(summarized_text, "output.mp3")
            st.audio("output.mp3", format="audio/mp3")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="subheader-title">Ask Questions from the PDF</div>', unsafe_allow_html=True)
        question = st.text_input("Enter your question:")
        st.markdown('<div class="alert">For this option: Your text is temporarily saved as vectors for text-embedding and then deleted.<br>Your privacy is crucial for us.</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        documents = chunk_by_max_chunk_size(content, 200, preserve_sentence_structure=True)
        text_chunks = [chunk.text for chunk in documents.chunks]

        embedded_documents = [generate_embeddings_open_ai(chunk) for chunk in text_chunks]

        db = VectorDatabase('data')
        for idx, emb in enumerate(embedded_documents):
            db.add_vector(emb, {"doc_id": idx, "vector": text_chunks[idx]}, normalize=True)

        db.save_to_disk("rag")
        db.load_from_disk("rag")

        if st.button("Get Answer", key="get-answer-btn"):
            try:
                query_embedding = generate_embeddings_open_ai(question)
                query_embedding = db.normalize_vector(query_embedding)

                results = db.top_cosine_similarity(query_embedding, top_n=1)
                
                if results:
                    context = results[0][0]['vector']
                    prompt = f"Answer the following question: {question} \n Based on this context only: \n{context}"
                    answer = generate_text(prompt)
                else:
                    answer = "No relevant context found in the PDF."
                
                st.write("Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"An error occurred: {e}")

    except ValueError as e:
        st.error(f"Error processing file: {e}")

    finally:
        if not save_content:
            # Delete the temporary file if the user opts not to save content
            os.remove(tmp_file_path)

else:
    st.info("Please upload a file to summarize.")

# Footer section
with st.container():
    st.markdown("<h5 style='text-align: center;'>Enjoy the Tool :)</h5>", unsafe_allow_html=True)
    st.caption("<p style='text-align: center;'>Developed by Hassan Salman, a PhD Student in LIP6 Laboratory at Sorbonne University</p>", unsafe_allow_html=True)
   