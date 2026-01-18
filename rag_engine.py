import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import RetrievalQA

# Load environment variables
load_dotenv()

class RAGEngine:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model_name=model_name, temperature=0)
        self.vector_store = None

    def process_pdf(self, file_path):
        """Loads a PDF, splits it into chunks, and stores in FAISS."""
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        # Split text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        texts = text_splitter.split_documents(documents)
        
        # Create vector store
        self.vector_store = FAISS.from_documents(texts, self.embeddings)
        return f"Successfully processed {len(texts)} chunks from {os.path.basename(file_path)}."

    def get_qa_chain(self):
        """Creates a RetrievalQA chain using the stored vector store."""
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Please process a document first.")
        
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        return qa_chain

    def query(self, question):
        """Helper method to run a query through the QA chain."""
        qa_chain = self.get_qa_chain()
        response = qa_chain.invoke({"query": question})
        return response["result"], response["source_documents"]
