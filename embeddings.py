from openai import OpenAI
import os

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_embeddings_open_ai(user_input):
    response = openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=user_input
            )
    return response.data[0].embedding

def generate_text(user_input):
    response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "answer only based on the provided context, if you don't find an answer there, return 'I don't know.'"},
                    {"role": "user", "content": user_input},
                ]
            )
    return response.choices[0].message.content
