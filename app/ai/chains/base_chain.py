from abc import ABC, abstractmethod
from typing import Any


class BaseChain(ABC):
    """
    Classe base astratta per tutte le chain LangChain.
    
    TODO: Implementazione completa in Fase 6 con:
    - Logging automatico
    - Tracing LangSmith integrato
    - Gestione errori centralizzata
    - Interfaccia comune per tutte le chain
    """

    name: str = "base_chain"

    @abstractmethod
    async def run(self, input: dict[str, Any]) -> dict[str, Any]:
        """Esegue la chain con logging e tracing automatici."""
        ...
