from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.chains.base import Chain
from langchain_core.prompts import PromptTemplate

from src.application.prompt import get_prompt
from src.application.retriever import Vectorizer
from src.common.models import Chat


def get_chain(chat: Chat, vectorizer: Vectorizer, prompt: PromptTemplate) -> Chain:
    structure = dict(llm=chat.model, memory=chat.memory, output_key='answer')
    if not vectorizer.index:
        chain = LLMChain(prompt=prompt, **structure)
    else:
        retriever_prompt = get_prompt(key='retriever', input_variables=['context', 'question'])
        chain = ConversationalRetrievalChain.from_llm(
            chain_type='stuff',
            retriever=vectorizer.index.as_retriever(),
            combine_docs_chain_kwargs={'prompt': retriever_prompt},
            **structure
        )
    return chain
