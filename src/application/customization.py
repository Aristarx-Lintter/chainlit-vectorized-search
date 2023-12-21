from dependency_injector.wiring import inject, Provide

import chainlit as cl

from src.application.actions.selector import make_choice
from src.application.chain import get_chain
from src.application.containers import Container
from src.application.prompt import get_prompt
from src.application.retriever import Vectorizer
from src.common.models import Chat
from src.common.processors import Postprocessing
from src.common.handlers import check_and_write_files


@cl.on_chat_start
@inject
async def on_chat_start(chat: Chat = Provide[Container.chat]):  # noqa: WPS404
    """
    Initialize chat with predefined parameters
    :param chat: preconfigured chat for user operations
    """
    vectorizer = Vectorizer(chat.embeddings)
    await make_choice(Postprocessing(vectorizer.write_file, vectorizer))

    cl.user_session.set('vectorizer', vectorizer)
    cl.user_session.set('chat', chat)
    cl.user_session.set('prompt', get_prompt())


@cl.on_message
async def main(message: cl.Message):
    """
    The operations on message stream
    :param message: message from user
    """
    vectorizer = cl.user_session.get('vectorizer')
    chat = cl.user_session.get('chat')
    vectorizer(check_and_write_files(message))
    chain = get_chain(chat, vectorizer, cl.user_session.get('prompt'))
    res = await chain.acall(message.content, callbacks=[cl.AsyncLangchainCallbackHandler()])
    await cl.Message(content=res['answer']).send()
