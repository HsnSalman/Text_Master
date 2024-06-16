from SimplerLLM.language.llm import LLM,LLMProvider
from SimplerLLM.tools.generic_loader import load_content
from SimplerLLM.language.llm_addons import generate_pydantic_json_model

from pydantic import BaseModel
from typing import List

class TitlesModel(BaseModel):
    titles: List[str]



Phd = LLM.create(LLMProvider.OPENAI, model_name="gpt-3.5-turbo")

topic = "coffee"
my_input = f"""generate 3 titles for my article about {topic}.

The output should be a valid JSON.
Example:
{{
  "titles": [
    "title 1",
    "title 2",
    "title 3"
  ]
}}

"""

my_input_super = f"generate 3 titles for my article about {topic}."




response = generate_pydantic_json_model(model_class=TitlesModel,prompt=my_input_super,llm_instance=Phd)


#response = Phd.generate_response(prompt=my_input)

print(response.titles[0])