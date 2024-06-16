from SimplerLLM.language.llm import LLM,LLMProvider
from SimplerLLM.tools.generic_loader import load_content

Phd = LLM.create(LLMProvider.OPENAI, model_name="gpt-3.5-turbo")

#upload pdf,text,docx

text = load_content("t.")

summarized_text = Phd.generate_response(prompt=f"Summarize the following text {text.content}")

print(summarized_text)