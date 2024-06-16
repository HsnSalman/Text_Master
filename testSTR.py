# Import necessary libraries
import streamlit as st  # Streamlit for creating the web app
from SimplerLLM.language.llm import LLM, LLMProvider  # LLM and LLMProvider for using language models
import tempfile  # tempfile for handling uploaded files
import fitz  # PyMuPDF for handling PDF files
import docx  # python-docx for handling DOCX files
from PIL import Image  # PIL for handling images
import os  # os for file handling


# Initialize the language model with OpenAI's GPT-3.5-turbo
Phd = LLM.create(LLMProvider.OPENAI, model_name="gpt-3.5-turbo")

# Set up the Streamlit app title and description with an icon
st.set_page_config(page_title="Text Summarizer", page_icon=":memo:")

# Add a header image
header_image = Image.open("Sorbonne.png")  # Replace with your image path
st.image(header_image, use_column_width=True)

st.title("Text Summarizer with GPT-3.5-turbo for our PhD team members")
st.write("""
This application allows you to upload a text file (PDF, TXT, DOCX) and get a summarized version of its content using OpenAI's GPT-3.5-turbo model.
""")

# Add a line separator
st.markdown("<hr>", unsafe_allow_html=True)

# Allow users to upload a file
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"], help="Upload a PDF, TXT, or DOCX file for summarization")

# Function to read text files with different encodings
def read_text_file(file_path, encodings=["utf-8", "latin1", "cp1252"]):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to decode text file with provided encodings")

# Function to read PDF files
def read_pdf_file(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to read DOCX files
def read_docx_file(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Check if a file has been uploaded
if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    try:
        # Determine the file type and read the content accordingly
        if uploaded_file.type == "text/plain":
            content = read_text_file(tmp_file_path)
        elif uploaded_file.type == "application/pdf":
            content = read_pdf_file(tmp_file_path)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            content = read_docx_file(tmp_file_path)
        else:
            raise ValueError("Unsupported file type")

        # Display a preview of the uploaded content
        st.subheader("File Content Preview")
        st.text_area("File Content", content, height=300)

        # Customization options
        st.subheader("Customize Your Summary")
        summary_length = st.slider("Summary Length (in sentences)", min_value=1, max_value=10, value=5)

        # Generate the summary using the language model
        summarized_text = Phd.generate_response(prompt=f"Summarize the following text in {summary_length} sentences: {content}")

        # Display the summarized text in the Streamlit app
        st.subheader("Summarized Text")
        st.write(summarized_text)

        # Add a download button for the summarized text
        st.download_button(
            label="Download Summary",
            data=summarized_text,
            file_name="summary.txt",
            mime="text/plain"
        )

        # Advanced Text Analysis Options
        st.subheader("Advanced Text Analysis")
        if st.button("Perform Sentiment Analysis"):
            sentiment_result = Phd.generate_response(prompt=f"Perform sentiment analysis on the following text: {content}")
            st.write("Sentiment Analysis Result")
            st.write(sentiment_result)
        
        if st.button("Extract Keywords"):
            keywords_result = Phd.generate_response(prompt=f"Extract keywords from the following text: {content}")
            st.write("Keywords Extraction Result")
            st.write(keywords_result)

    except ValueError as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload a file to summarize.")

# Add a footer image
footer_image = Image.open("textsummarizer.png")  # Replace with your image path
st.image(footer_image, use_column_width=True, caption="Thank you for using our service!")
