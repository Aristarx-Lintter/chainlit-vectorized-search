import json
from typing import List

from langchain_core.prompts import PromptTemplate


def get_prompt(
    path: str = 'templates/chat_templates.json',
    key: str = 'just_chain',
    input_variables: List[str] = ['input', 'history']  # noqa: B006, WPS404
) -> PromptTemplate:
    with open(path, 'r') as f:
        data = json.loads(f.read())[key]
    return PromptTemplate(template=data, input_variables=input_variables)
