import os
import openai
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader,VectorStoreIndex

load_dotenv()
openai.api_key = os.getenv("api_key")

def CreateIndex(label,persisDirName):
    try:
        path="data/"+label
        docs = SimpleDirectoryReader(path).load_data()
        index=VectorStoreIndex.from_documents(docs)
        PersistentDir=persisDirName
        index.storage_context.persist(persist_dir=PersistentDir)
    except Exception as e:
        print(f"Error creating index for {label}: {e}")

CreateIndex("TAIBALL","Embeddings/TAIBALL")
CreateIndex("TAIBEECS","Embeddings/TAIBEECS")
CreateIndex("TAIBIT","Embeddings/TAIBIT")