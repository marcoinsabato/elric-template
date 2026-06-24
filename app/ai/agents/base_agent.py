from abc import ABC, abstractmethod

from langgraph.graph import StateGraph


class BaseAgent(ABC):
    """
    Classe base astratta per tutti gli agenti LangGraph.
    
    TODO: Implementazione completa in Fase 6 con:
    - Logging automatico
    - Tracing LangSmith integrato
    - Gestione errori centralizzata
    - Interfaccia comune per tutti gli agenti
    """

    name: str = "base_agent"

    @abstractmethod
    def build_graph(self) -> StateGraph:
        """Costruisce e restituisce il grafo LangGraph."""
        ...

    async def run(self, input: dict) -> dict:
        """Esegue l'agent con logging e tracing automatici."""
        graph = self.build_graph().compile()
        return await graph.ainvoke(input)
