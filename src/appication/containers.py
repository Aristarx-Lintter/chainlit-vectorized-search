from dependency_injector import containers, providers

from src.common.models import Chat


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    chat = providers.Singleton(
        Chat,
        config=config.chat
    )
