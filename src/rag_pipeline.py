"""
RAG pipeline module for constructing and executing the retrieval-augmented generation chain.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from typing import List
import config


class RAGPipeline:
    """Manages the RAG (Retrieval-Augmented Generation) pipeline."""
    
    def __init__(self, llm, retriever, prompt_template: str = config.PROMPT_TEMPLATE):
        """
        Initialize RAG pipeline.
        
        Args:
            llm: Language model instance
            retriever: Vector store retriever instance
            prompt_template: Template for the prompt
        """
        self.llm = llm
        self.retriever = retriever
        self.prompt = ChatPromptTemplate.from_template(prompt_template)
        self.chain = self._create_chain()
    
    @staticmethod
    def format_docs(docs: List) -> str:
        """
        Format retrieved documents into a single string.
        
        Args:
            docs: List of retrieved documents
            
        Returns:
            Formatted string of document contents
        """
        return "\n\n".join(doc.page_content for doc in docs)
    
    def _create_chain(self):
        """
        Create the RAG chain.
        
        Returns:
            Configured RAG chain
        """
        chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        return chain
    
    def query(self, question: str) -> str:
        """
        Execute a query through the RAG pipeline.
        
        Args:
            question: User question
            
        Returns:
            Generated answer
        """
        print(f"❓ Query: {question}")
        answer = self.chain.invoke(question)
        print(f"✅ Answer generated")
        return answer
    
    def query_with_sources(self, question: str) -> dict:
        """
        Execute a query and return answer with source documents.
        
        Args:
            question: User question
            
        Returns:
            Dictionary with 'answer' and 'sources'
        """
        # Retrieve source documents
        source_docs = self.retriever.get_relevant_documents(question)
        
        # Generate answer
        answer = self.query(question)
        
        return {
            "answer": answer,
            "sources": source_docs
        }