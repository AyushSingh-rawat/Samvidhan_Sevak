import os
import pickle
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from PyPDF2 import PdfReader
from langchain_huggingface import HuggingFaceEmbeddings

def get_pdf_text(pdf_path):
    """Extract text from the Constitution PDF."""
    text = ""
    pdf_reader = PdfReader(pdf_path)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_text_chunks(text):
    """Split the text into manageable chunks."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(text)

def save_embeddings(embedding_file, pdf_path):
    """Generate and save embeddings for the Constitution dataset."""
    # Extract text and split into chunks
    text = get_pdf_text(pdf_path)
    chunks = get_text_chunks(text)

    # # Generate embeddings using HuggingFace model
    # embeddings = HuggingFaceInstructEmbeddings(model_name="all-MiniLM-L6-v2")
    # vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)

    os.environ['HF_TOKEN'] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)

    # Save embeddings to a pickle file
    with open(embedding_file, "wb") as f:
        pickle.dump(vectorstore, f)

    print(f"Embeddings saved to {embedding_file}")


import os
from dotenv import load_dotenv
load_dotenv()  #load all the environment variables


os.environ['HF_TOKEN']=os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Generate embeddings
pdf_path = "constitution_of_india.pdf"
embedding_file = "constitution_embeddings.pkl"
save_embeddings(embedding_file, pdf_path)
