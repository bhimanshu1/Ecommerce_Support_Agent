from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()
# llm_api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# creates the rag database using the given policy knowledge(.md files)
def rag_database_initialisation():
    loader = DirectoryLoader(
        "sample_data/docs",
        glob="*.md",
        loader_cls=TextLoader,
    )
    documents = loader.load()
    # Split the documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks: {len(chunks)}")
    # Embedding model converts the chunks into numerical vectors
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    # Create FAISS vector database to store chunks and numerical vectors for sematic search
    vector_db = FAISS.from_documents(
        chunks,
        embedding_model
    )
    return vector_db
    

def semantic_chunk_search(query, vector_db):
    results = vector_db.similarity_search(query, k=3)    
    return results


def answer_policy_question(question, vector_db, retrieval_query=None):
    search_query = retrieval_query if retrieval_query else question
    chunks = semantic_chunk_search(search_query, vector_db)    
    context = "\n\n".join(
        [doc.page_content for doc in chunks]
    )
    prompt = f"""
        You are a customer support assistant.
        Answer ONLY using the context below.
        If the answer is not present in the context, reply:
        "I couldn't find that information in the policy documents."
        Do not make up information.
        Do not use outside knowledge.
        Context:
        {context}
        Question:
        {question}
    """
    response = llm.invoke(prompt)
    return response.content

# results = Semantic_chunk_search("what is the return policies?");

# print("\nRetrieved Chunks:\n")
#     print("=" * 60)
#     print(f"Result {i}")
#     print(doc.metadata)
#     print(doc.page_content)