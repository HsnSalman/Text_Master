# Text Master

Welcome to Text Master, your go-to advanced text summarizer, crafted with different language models. Our tool enables swift and efficient summarization of extensive text files, including PDFs, TXT, and DOCX formats. By leveraging multiple models such as OpenAI GPT-3.5-turbo, GPT-4, and Gemini, Text Master delivers accurate and concise summaries, complemented by advanced text analysis features. Tailored for researchers, students, and professionals, Text Master is designed to help you manage and utilize your text data more effectively.

![Text Master logo](logo.png)

## Table of Contents
- [Home](#home)
- [Documentation](#documentation)
- [Source Code](#source-code)
- [Report a Problem](#report-a-problem)
- [About](#about)

## Home
Welcome to Text Master, your gateway to advanced text processing.

![Introduction](text_master.png)

## Documentation
### Installation and Setup
To set up the Text Master application, follow these steps:
1. Clone the repository from GitHub:
    ```bash
    git clone https://github.com/HsnSalman/Text_Master
    ```
2. Navigate to the project directory:
    ```bash
    cd Text_Master
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a `.env` file in the root directory of your project and add your API keys there:
    ```env
    OPENAI_API_KEY="your_openai_api_key_here"
    ```
5. Run the Streamlit application:
    ```bash
    streamlit run Text_Master.py
    ```

### Usage
Once the application is running, follow these steps to use Text Master:
1. Select the LLM Model from the sidebar options.
2. Upload a text file (PDF, TXT, DOCX) for summarization.
3. Preview the uploaded content in the provided text area.
4. Customize the summary length using the slider.
5. Click the "Generate Summary" button to get the summarized text.
6. Download the summarized text using the provided download button.

### Advanced Features
Text Master also offers advanced text analysis options, including:
- Sentiment Analysis: Analyze the sentiment of the text content.
- Keywords Extraction: Extract important keywords from the text.
- Language Translation: Translate the text into French language.
- Text to Speech: Convert the Summarized Text into Speech.
- Ask Questions: Get answers to specific questions based on the uploaded text content.

![Documentation Video](documentation.mp4)

## Source Code
Access the source code on our [GitHub repository](https://github.com/HsnSalman/Text_Summarizer). Contribute to the project or customize it to suit your needs.

## Report a Problem
If you encounter any issues or have suggestions for improvements, please report them on our [issue tracker](https://github.com/HsnSalman/Text_Summarizer/issues).

## About
Text Master is developed by Hassan Salman in the Move team at LIP6, Sorbonne Université. If you want to collaborate or have a case study, feel free to send an email to: [hassan.salman@etu.sorbonne-universite.fr](mailto:hassan.salman@etu.sorbonne-universite.fr).

![LIP6](lip6.png)

&copy; 2024 Laboratoire d'Informatique de Paris 6, CNRS, Sorbonne Universités. All rights reserved.
