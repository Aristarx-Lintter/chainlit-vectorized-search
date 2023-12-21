from src.common.utils import load_object


class Chat:
    def __init__(self, config):
        self._config = config
        self.embeddings = load_object(self._config.embeddings.embeddings)(**self._config.embeddings.kwargs)
        self.model = load_object(self._config.model.model)(**self._config.model.kwargs)
        self.history = load_object(self._config.history.history)()
        memory_kwargs = {"llm": self.model, "chat_memory": self.history, **self._config.memory.kwargs}
        self.memory = load_object(self._config.memory.memory)(**memory_kwargs)