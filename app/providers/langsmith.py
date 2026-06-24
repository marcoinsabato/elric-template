import os

from config.settings import get_settings

settings = get_settings()


def init_langsmith():
    if settings.LANGCHAIN_TRACING_V2:
        os.environ["LANGCHAIN_TRACING_V2"] = str(settings.LANGCHAIN_TRACING_V2).lower()
        os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
