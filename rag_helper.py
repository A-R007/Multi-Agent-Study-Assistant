import os
from typing import List, Optional
from phi.knowledge.pdf import PDFUrlKnowledgeBase, PDFKnowledgeBase
from phi.vectordb.chroma import ChromaDb
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import chromadb

class RAGHelper:
    """
    Helper class for RAG (Retrieval Augmented Generation) functionality.
    Manages document loading, embedding, and retrieval.
    """
    
    def __init__(self, collection_name: str = "study_materials", persist_directory: str = "./chroma_db"):
        """
        Initialize the RAG helper.
        
        Args:
            collection_name (str): Name of the ChromaDB collection
            persist_directory (str): Directory to persist the vector database
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vectorstore = None
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """
        Initialize or load the vector store.
        """
        try:
            # Create persist directory if it doesn't exist
            os.makedirs(self.persist_directory, exist_ok=True)
            
            # Initialize ChromaDB
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            self.vectorstore = None
    
    def load_pdf(self, file_path: str) -> bool:
        """
        Load a PDF file and add it to the knowledge base.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Add to vector store
            if self.vectorstore:
                self.vectorstore.add_documents(chunks)
                return True
            return False
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
    
    def load_text(self, file_path: str) -> bool:
        """
        Load a text file and add it to the knowledge base.
        
        Args:
            file_path (str): Path to the text file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            loader = TextLoader(file_path)
            documents = loader.load()
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Add to vector store
            if self.vectorstore:
                self.vectorstore.add_documents(chunks)
                return True
            return False
        except Exception as e:
            print(f"Error loading text file: {e}")
            return False
    
    def load_text_content(self, text: str, metadata: dict = None) -> bool:
        """
        Load text content directly and add it to the knowledge base.
        
        Args:
            text (str): The text content to add
            metadata (dict): Optional metadata for the document
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            from langchain.schema import Document
            
            # Create document
            doc = Document(page_content=text, metadata=metadata or {})
            
            # Split into chunks
            chunks = self.text_splitter.split_documents([doc])
            
            # Add to vector store
            if self.vectorstore:
                self.vectorstore.add_documents(chunks)
                return True
            return False
        except Exception as e:
            print(f"Error loading text content: {e}")
            return False
    
    def query(self, question: str, k: int = 4) -> List[str]:
        """
        Query the knowledge base and retrieve relevant documents.
        
        Args:
            question (str): The question to search for
            k (int): Number of documents to retrieve
            
        Returns:
            List[str]: List of relevant document contents
        """
        try:
            if not self.vectorstore:
                return []
            
            # Perform similarity search
            docs = self.vectorstore.similarity_search(question, k=k)
            
            # Extract content
            return [doc.page_content for doc in docs]
        except Exception as e:
            print(f"Error querying knowledge base: {e}")
            return []
    
    def query_with_scores(self, question: str, k: int = 4) -> List[tuple]:
        """
        Query the knowledge base and retrieve relevant documents with similarity scores.
        
        Args:
            question (str): The question to search for
            k (int): Number of documents to retrieve
            
        Returns:
            List[tuple]: List of (document, score) tuples
        """
        try:
            if not self.vectorstore:
                return []
            
            # Perform similarity search with scores
            results = self.vectorstore.similarity_search_with_score(question, k=k)
            
            return [(doc.page_content, score) for doc, score in results]
        except Exception as e:
            print(f"Error querying knowledge base: {e}")
            return []
    
    def clear_database(self) -> bool:
        """
        Clear all documents from the database.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.vectorstore:
                # Delete the collection and reinitialize
                client = chromadb.PersistentClient(path=self.persist_directory)
                client.delete_collection(name=self.collection_name)
                self._initialize_vectorstore()
                return True
            return False
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False
    
    def get_document_count(self) -> int:
        """
        Get the number of documents in the knowledge base.
        
        Returns:
            int: Number of documents
        """
        try:
            if self.vectorstore:
                collection = self.vectorstore._collection
                return collection.count()
            return 0
        except Exception as e:
            print(f"Error getting document count: {e}")
            return 0
    
    def create_phi_knowledge_base(self) -> Optional[object]:
        """
        Create a Phi-compatible knowledge base for use with Phi agents.
        
        Returns:
            Optional[object]: A Phi knowledge base object or None
        """
        try:
            # Create a Phi ChromaDB knowledge base
            knowledge_base = ChromaDb(
                collection=self.collection_name,
                path=self.persist_directory,
                embedder=self.embeddings
            )
            return knowledge_base
        except Exception as e:
            print(f"Error creating Phi knowledge base: {e}")
            return None
