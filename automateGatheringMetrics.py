import os 
import openai
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.memory import ChatMemoryBuffer

load_dotenv()
# Set OpenAI API key
openai.api_key = os.getenv("api_key")

# Load the index from the local directory
storage_context = StorageContext.from_defaults(persist_dir=Path(""))
index = load_index_from_storage(storage_context)

# Create a memory buffer for the chatbot
memory = ChatMemoryBuffer.from_defaults()

# Create the chat engine with custom configuration
chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt=(
        """You are a chatbot named ‘TAIB’. Act as a knowledgeable and helpful assistant for individuals 
        seeking information about Queen Mary University of London. In particular but not limited to, questions regarding
        Residential questions and IT-related issues.
        Provide clear and precise answers based on the resources attached. 
        If there is a related URL/Contact number please include this.
        Maintain a professional tone and ensure the information you give is easy to understand and directly addresses the user’s query.
        Prioritise the information found in the documents over the internet.
        If a contact detail is not found, do not provide one. If the user asks for a contact detail, inform them that the information is not available.
        """
        # Ive removed the line in the prompt from this regarding the school of EECS as this is now a general chatbot
        # This was neccessry as it kept giving eecs related answers to non eecs questions
    ),
    similarity_top_k=3
) 
# Load the Excel file
df = pd.read_excel('')

# Ensure there is an 'output' column and change its data type to object
if 'output' not in df.columns:
    df['output'] = pd.Series(dtype='object')
else:   
    df['output'] = df['output'].astype('object')

# Process each query and save the response
for idx, row in df.iterrows():
    query = row['query ']  # Notice the space after 'query'
    response = chat_engine.query(query)  # Process the query through the chat engine
    df.at[idx, 'output'] = response  # Save the response in the 'output' column

# Save the updated DataFrame back to Excel
df.to_excel('', index=False)
