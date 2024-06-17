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
from openai import OpenAI

# Set up the Streamlit app configuration
st.set_page_config(page_title="Text Summarizer", page_icon=":memo:")

# Sidebar setup
st.sidebar.title("Model Selection and Options")
model_choice = st.sidebar.selectbox("Select LLM Model", ["OpenAI GPT-3.5-turbo", "OpenAI GPT-4", "Gemini"])
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Add API key input field
api_key = st.sidebar.text_input("Enter your API key", type="password")

# Check if the API key is provided
if not api_key:
    st.sidebar.warning("Please enter your API key to proceed.")
    st.stop()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize the selected language model
if model_choice == "OpenAI GPT-3.5-turbo":
    model_name = "gpt-3.5-turbo"
    Phd = LLM.create(LLMProvider.OPENAI, model_name=model_name)
elif model_choice == "OpenAI GPT-4":
    model_name = "gpt-4"
    Phd = LLM.create(LLMProvider.OPENAI, model_name=model_name)
# elif model_choice == "Gemini":
#     # Replace 'gemini-model' with the actual model name for Gemeni
#     model_name = "gemini-pro"
#     Phd = LLM.create(LLMProvider.GEMINI, model_name=model_name)

# Set up the Streamlit app title and description with an icon
header_image = Image.open("Sorbonne.png")  # Replace with your image path
st.image(header_image, use_column_width=True)
st.title("Text Summarizer with LLM Models for Our PhD Team Members")
st.write("Upload a text file (PDF, TXT, DOCX) and get a summarized version of its content using the selected LLM model.")

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

        if st.button("Language Translation"):
            Translated_Results = Phd.generate_response(prompt=f"Translate the following text into French: {content}")
            st.write("Translated Text")
            st.write(Translated_Results)

        if st.button("Summarized Text Translation"):
            Summarized_Translated_Results = Phd.generate_response(prompt=f"Translate the following text into French: {summarized_text}")
            st.write("Translated Summarized Text")
            st.write(Summarized_Translated_Results)

        # Add a section to ask questions from the PDF
        st.subheader("Ask Questions from the PDF")
        question = st.text_input("Enter your question:")


        documents = chunk_by_max_chunk_size(content,200, preserve_sentence_structure=True)


        chunks = documents.chunks

        #print(documents.num_chunks)

        text_chunks = [chunk.text for chunk in chunks]

        embedded_documents = []

        for chunk in text_chunks:
            embedding = generate_embeddings_open_ai(chunk)
            embedded_documents.append(embedding)



        db = VectorDatabase('data')
        # Adding each vector to the database with some metadata (e.g., the document it came from)
        for idx, emb in enumerate(embedded_documents):
            db.add_vector(emb, {"doc_id": idx, "vector": text_chunks[idx]}, normalize=True)


        db.save_to_disk("rag")


        db.load_from_disk("rag")


        if st.button("Get Answer"):
            try:
                query_embedding = generate_embeddings_open_ai(question)
                query_embedding = db.normalize_vector(query_embedding)  # Normalizing the query vector

                # Debugging: Print the query embedding to ensure it's generated correctly
                st.write(f"Query Embedding: {query_embedding}")

                results = db.top_cosine_similarity(query_embedding, top_n=1)
                
                if results:
                    context = results[0][0]['vector']
                    prompt = f"Answer the following question: {question} \n Based on this context only: \n{context}"
                    
                    # Debugging: Print the context to ensure it's retrieved correctly
                    st.write(f"Context: {context}")

                    answer = generate_text(prompt)
                else:
                    answer = "No relevant context found in the PDF."
                
                st.write("Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"An error occurred: {e}")

    except ValueError as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload a file to summarize.")

# Add a footer image
footer_image = Image.open("textsummarizer.png")  
st.image(footer_image, use_column_width=True, caption="Thank you for using our service!")
