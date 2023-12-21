from src.common.handlers import load_object


class Chat:
    def __init__(self, config):
        self._config = config
        embedding = self._config.embeddings
        self.embeddings = load_object(embedding.embeddings)(**embedding.kwargs)
        model = self._config.model
        self.model = load_object(model.model)(**model.kwargs)
        self.history = load_object(self._config.history.history)()
        memory_kwargs = {'llm': self.model, 'chat_memory': self.history, **self._config.memory.kwargs}
        self.memory = load_object(self._config.memory.memory)(**memory_kwargs)
