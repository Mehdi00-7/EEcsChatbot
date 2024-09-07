import os
import openai
from dotenv import load_dotenv
from pathlib import Path
from llama_index.core import  StorageContext, load_index_from_storage
from llama_index.core.memory import ChatMemoryBuffer
load_dotenv()
openai.api_key = os.getenv("api_key")

#  Loads the index from my local directory 
storage_context = StorageContext.from_defaults(persist_dir=Path("Embeddings/TAIBEECS")) #Path to embeddings in local repositery these are stored in the embeddings folder and are named accordingly
index = load_index_from_storage(storage_context)
# Creates a memory buffer for the chatbot
memory = ChatMemoryBuffer.from_defaults()

# Creates the chat engine with custom configuration like a prompt etc
chat_engine = index.as_chat_engine(
    chat_mode="react",
    memory=memory,
    system_prompt=(
        """You are a chatbot named ‘TAIB’. Act as a knowledgeable and helpful assistant for individuals 
        seeking information about Queen Mary University of London. In particular but not limited to, questions regarding
        the School of Electrical Engineering and Computer Science (EECS)
        Provide clear and precise answers based on the resources attached. 
        If there is a related URL/Contact number please include this.
        Maintain a professional tone and ensure the information you give is easy to understand and directly addresses the user’s query.
        Prioritise the information found in the documents over the internet.
        If a contact detail is not found, do not provide one. If the user asks for a contact detail, inform them that the information is not available.
        """
    ),
    similarity_top_k=3
)
# Clears the context with every run 
chat_engine.reset()
# Starts the chatbot
chat_engine.chat_repl()


