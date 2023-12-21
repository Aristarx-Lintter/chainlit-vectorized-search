import chainlit as cl

from src.common.processors import Postprocessing


async def make_choice(postprocessing: Postprocessing):
    message = cl.AskActionMessage(
        content='Вырерите вариант чата.',
        actions=[
            cl.Action(name='big', value='big', label='Вопросы к большому документу (до 100Мб)'),
            cl.Action(name='just', value='just', label='Простой диалог и вопросы к не большим документам (до 20Мб)')
        ]
    )

    res = await message.send()
    if res and res.get('value') == 'big':
        files = await cl.AskFileMessage(
            content='Загрузите файл', accept=['text/csv', 'application/pdf'], max_size_mb=100, max_files=10
        ).send()

        msg = cl.Message(
            content='Обработка файлов ...', disable_human_feedback=True
        )
        await msg.send()

        postprocessing(files)
        msg.content = f'Обработка файлов завершена, можете задавать вопросы.'
        await msg.update()
