"""Base Agent class for all agents"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage

from src.config import settings


class BaseAgent(ABC):
    """Abstract base class for all agents"""

    def __init__(
        self,
        name: str,
        description: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ):
        self.name = name
        self.description = description

        # Initialize LLM
        self.llm = ChatOllama(
            base_url=settings.ollama.host,
            model=model or settings.ollama.model,
            temperature=temperature or settings.ollama.temperature,
            num_ctx=settings.ollama.num_ctx
        )

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Define the system prompt for this agent"""
        pass

    def get_prompt_template(self, human_template: str) -> ChatPromptTemplate:
        """Create a prompt template with system and human messages"""
        return ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", human_template)
        ])

    @abstractmethod
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's task"""
        pass

    async def invoke_llm(self, prompt: str) -> str:
        """Invoke the LLM with a prompt"""
        response = await self.llm.ainvoke(prompt)
        return response.content

    async def invoke_with_template(
        self,
        template: ChatPromptTemplate,
        **kwargs
    ) -> str:
        """Invoke the LLM with a template and variables"""
        chain = template | self.llm
        response = await chain.ainvoke(kwargs)
        return response.content

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
