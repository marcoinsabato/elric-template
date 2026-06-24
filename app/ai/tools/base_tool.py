from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """
    Classe base astratta per tutti i tool LangChain.
    
    TODO: Implementazione completa in Fase 6 con:
    - Logging automatico
    - Tracing LangSmith integrato
    - Gestione errori centralizzata
    - Interfaccia comune per tutti i tool
    """

    name: str = "base_tool"
    description: str = ""

    @abstractmethod
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        """Esegue il tool con logging e tracing automatici."""
        ...
