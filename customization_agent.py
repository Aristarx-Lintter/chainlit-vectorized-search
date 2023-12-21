import json

from langchain.agents import AgentType, Tool, initialize_agent
from dependency_injector.wiring import inject, Provide
from langchain.chains import ConversationalRetrievalChain, LLMChain, RetrievalQA
from langchain.memory import ChatMessageHistory, ConversationSummaryBufferMemory

import chainlit as cl
from langchain_core.prompts import PromptTemplate

from src.appication.containers import Container
from src.appication.retriever import Vectorizer
from src.common.models import Chat
from src.common.utils import check_and_write_files, write_file


@cl.on_chat_start
@inject
async def on_chat_start(chat: Chat = Provide[Container.chat]):
    vectorizer = Vectorizer(chat.embeddings)
    res = await cl.AskActionMessage(
        content="Вырерите вариант чата.",
        actions=[
            cl.Action(name="big", value="big", label="Вопросы к большому документу (до 100Мб)"),
            cl.Action(name="just", value="just", label="Простой диалог и вопросы к не большим документам (до 20Мб)")
        ]
    ).send()
    if res and res.get("value") == "big":
        files = await cl.AskFileMessage(
            content="Загрузите файл", accept=["text/csv", "application/pdf"], max_size_mb=100,
        ).send()

        for file_ in files:
            write_file(file_.path, file_.content)

        vectorizer([file_.path for file_ in files])

    cl.user_session.set("vectorizer", vectorizer)

    memory = ConversationSummaryBufferMemory(
        llm=chat.model,
        memory_key="chat_history",
        output_key="answer",
        chat_memory=ChatMessageHistory(),
        return_messages=True,
    )

    with open("templates/chat_templates.json", "r") as f:
        data = json.loads(f.read())['just_chain']
        prompt = PromptTemplate(template=data, input_variables=["input", "history"])

    cl.user_session.set("chat", chat)
    cl.user_session.set("prompt", prompt)
    cl.user_session.set("memory", memory)


@cl.on_message
async def main(message: cl.Message):

    files = check_and_write_files(message)
    vectorizer = cl.user_session.get("vectorizer")
    vectorizer(files)

    # Create a chain that uses the Chroma vector store
    chat = cl.user_session.get("chat")
    plain_chain = LLMChain(llm=chat.model, prompt=cl.user_session.get("prompt"), memory=cl.user_session.get("memory"), output_key="answer")
    tools = [Tool(name="История сообщений", func=plain_chain, description="Используется для вопросов получения информации об истории разговора.")]

    if vectorizer.index:
        files_chain = RetrievalQA.from_chain_type(
            chat.model,
            chain_type="stuff",
            retriever=vectorizer.index.as_retriever(),
        )
        tool = Tool(
                name="Векторизованное представление полученных файлов",
                func=files_chain.run,
                description="Используется для вопросов к документам.",
            )
        tools.append(tool)
    agent = initialize_agent(
        tools, chat.model, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    agent_chain = cl.make_async(agent.run)
    answer = await agent_chain(message.content, callbacks=[cl.AsyncLangchainCallbackHandler()])
    await cl.Message(content=answer).send()























# llm = OpenAI(temperature=0)
# llm_math = LLMMathChain.from_llm(llm=llm)
#
# @cl.on_message
# async def main(message: cl.Message):
#     res = await llm_math.acall(message.content, callbacks=[cl.AsyncLangchainCallbackHandler()])
#
#     await cl.Message(content="Hello").send()
#


# import chainlit as cl
#
#
# @cl.on_chat_start
# async def start():
#     # Send the first message without the elements
#     content = "Here is image1, a nice image! As well as text1 and text2! and pdf1"
#
#     await cl.Message(
#         content=content,
#     ).send()
#
#     elements = [
#         cl.Image(path="./background.jpg", name="image1", display="side"),
#         cl.Pdf(name="pdf1", display="side", path="./MathHW.pdf")
#         # cl.Text(content="Here is a side text document", name="text1", display="side"),
#         # cl.Text(content="Here is a page text document", name="text2", display="page"),
#     ]
#
#     # Send the second message with the elements
#     await cl.Message(
#         content=content,
#         elements=elements,
#     ).send()
