import numpy as np
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import os
import openai

from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

FAISS_PATH = "faiss_db_opt"  # Define the FAISS directory


class BaseSupportAgent(ABC):
    """Abstract base class for all support agents."""

    def __init__(self):
        """Initialize the BaseSupportAgent with the vector db type, Faiss index path, and embeddings model."""
        self.embedding_function = OpenAIEmbeddings(openai_api_key=openai.api_key)
        self.active_db = self._load_db()

    def _load_db(self) -> FAISS:
        """Loads the FAISS index or creates a new one if not found."""
        if os.path.exists(FAISS_PATH):
            try:
                db = FAISS.load_local(
                    FAISS_PATH,
                    self.embedding_function,
                    allow_dangerous_deserialization=True,  # Only use if you trust the source of the index
                )
                return db
            except Exception as e:
                print(f"Error loading existing FAISS index: {e}")
                print("Creating new FAISS index...")
                # Create an empty FAISS index with sample data
                db = FAISS.from_texts(["placeholder"], self.embedding_function)
                db.save_local(FAISS_PATH)
                return db
        else:
            # Create an empty FAISS index with sample data
            if not os.path.exists(FAISS_PATH):
                os.makedirs(FAISS_PATH)
            db = FAISS.from_texts(["placeholder"], self.embedding_function)
            db.save_local(FAISS_PATH)
            return db
            
    @abstractmethod
    def _get_vector_embedding(self, query: str) -> np.ndarray:
        """Abstract method to generate vector embedding for a query."""
        pass

    @abstractmethod
    def _search_db(self, query: str, top_k: int) -> list:
        """Abstract method to perform vector database search."""
        pass

    @abstractmethod
    def _process_results(self, search_results: list) -> list:
        """Abstract method to format the results for consumption."""
        pass
    
    def prepare_evidence(self, query_text: str) -> str:
        results = self.active_db.similarity_search_with_score(query_text, k=20)
        
        # Convert distances to similarity scores (0 to 1 scale)
        scores = [1 / (1 + score) for _, score in results]
        
        # Increase threshold for stricter filtering
        similarity_threshold = 0.7  # Increased from 0.5 for stricter matching
        
        filtered_results = [
            (doc, score) 
            for (doc, score) in zip((doc for doc, _ in results), scores)
            if score >= similarity_threshold
        ]

        if len(filtered_results) == 0:
            return "NO_RELEVANT_INFO"
        
        # Calculate average similarity score
        avg_similarity = sum(score for _, score in filtered_results) / len(filtered_results)
        
        # If average similarity is too low, return no info
        if avg_similarity < 0.65:  # Added additional threshold for average similarity
            return "NO_RELEVANT_INFO"
        
        sorted_results = sorted(filtered_results, key=lambda x: x[1], reverse=True)
        
        selected_chunks = []
        total_tokens = 0
        max_tokens = 1000
        
        for doc, score in sorted_results:
            chunk_tokens = len(doc.page_content.split())
            if total_tokens + chunk_tokens > max_tokens:
                break
            selected_chunks.append(doc.page_content)
            total_tokens += chunk_tokens
            print("selected_chunks",selected_chunks)

        return "\n\n---\n\n".join(selected_chunks)

    def query(self, subquery: str, top_k: int = 3) -> list:
        """Main method to query the vector database."""
        try:
           search_results = self._search_db(subquery, top_k)
           processed_results = self._process_results(search_results)
           return processed_results
        except Exception as e:
            print(f"Error querying database: {e}")
            return []
            
class KnowledgeRetriever(BaseSupportAgent):
    """Retrieves domain-specific knowledge from the Solvi Database."""
    def __init__(self):
        """Initialize the KnowledgeRetriever agent."""
        super().__init__()

    def _get_vector_embedding(self, query: str) -> np.ndarray:
        """Generates a vector embedding using an LLM for domain knowledge."""
        return self.embedding_function.embed_query(query)

    def _search_db(self, query: str, top_k: int) -> list:
        """
        Queries the FAISS index for relevant domain knowledge.
        """
        evidence = self.prepare_evidence(query)
        return [{"text": evidence}]
        
    def _process_results(self, search_results: list) -> list:
       """Formats results from Solvi DB into a readable format."""
       return [result["text"] + "\n\n---\n\n Source: Solvi Database" for result in search_results]

class EquationsFormulasRetriever(BaseSupportAgent):
    """Retrieves equations and formulas from the Equations & Formulas DB."""
    def __init__(self):
       """Initialize the EquationsFormulasRetriever agent."""
       super().__init__()

    def _get_vector_embedding(self, query: str) -> np.ndarray:
        """Generates a vector embedding using an LLM for equations and formulas."""
        return self.embedding_function.embed_query(query)

    def _search_db(self, query: str, top_k: int) -> list:
       """
       Queries the FAISS index for relevant equations and formulas.
       """
       evidence = self.prepare_evidence(query)
       return [{"text": evidence}]

    def _process_results(self, search_results: list) -> list:
        """Formats results from Equations & Formulas DB into a readable format."""
        return [result["text"]+ "\n\n---\n\n Source: Equations & Formulas DB" for result in search_results]

class PhysChemPropertiesRetriever(BaseSupportAgent):
    """Retrieves physical and chemical properties from the Phys/Chem Properties DB."""
    def __init__(self):
       """Initialize the PhysChemPropertiesRetriever agent."""
       super().__init__()

    def _get_vector_embedding(self, query: str) -> np.ndarray:
        """Generates a vector embedding using an LLM for properties."""
        return self.embedding_function.embed_query(query)

    def _search_db(self, query: str, top_k: int) -> list:
       """
       Queries the FAISS index for relevant physical and chemical properties.
       """
       evidence = self.prepare_evidence(query)
       return [{"text": evidence}]

    def _process_results(self, search_results: list) -> list:
        """Formats results from Phys/Chem Properties DB into a readable format."""
        return [result["text"] + "\n\n---\n\n Source: Phys/Chem Properties DB" for result in search_results]

class IndustryStandardsRetriever(BaseSupportAgent):
    """Retrieves industry standards from the Industry Standards DB."""
    def __init__(self):
       """Initialize the IndustryStandardsRetriever agent."""
       super().__init__()

    def _get_vector_embedding(self, query: str) -> np.ndarray:
        """Generates a vector embedding using an LLM for industry standards."""
        return self.embedding_function.embed_query(query)

    def _search_db(self, query: str, top_k: int) -> list:
       """
       Queries the FAISS index for relevant industry standards.
       """
       evidence = self.prepare_evidence(query)
       return [{"text": evidence}]

    def _process_results(self, search_results: list) -> list:
        """Formats results from Industry Standards DB into a readable format."""
        return [result["text"] + "\n\n---\n\n Source: Industry Standards DB" for result in search_results]