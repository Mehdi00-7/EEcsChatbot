import os
import pandas as pd
import openai
from deepeval.test_case import LLMTestCase
from deepeval.metrics import  ContextualRelevancyMetric, ContextualRecallMetric, FaithfulnessMetric, AnswerRelevancyMetric
from llama_index.core import  StorageContext,  load_index_from_storage
from pathlib import Path
from dotenv import load_dotenv

 # Add the OpenAI API key here

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenev("api_key")
storage_context = StorageContext.from_defaults(persist_dir=Path("")) # Add the path to the index here
index = load_index_from_storage(storage_context)

#This method will take in a query, output, expected_output and context and return an array of the metrics
def ragas(query,output,expected_output,context):
  #For each metric we specify the model and whether we are using strict mode. Strict mode being set to false means the metric wont be rounded to 0 or 1. 
  ragas_metrics = [ContextualRelevancyMetric(strict_mode=False, model = "gpt-3.5-turbo"), ContextualRecallMetric(strict_mode=False,model = "gpt-3.5-turbo"), FaithfulnessMetric(strict_mode=False,model = "gpt-3.5-turbo"), AnswerRelevancyMetric(strict_mode=False,model = "gpt-3.5-turbo")]
  test_case = LLMTestCase(
      input=query,
      actual_output=output,
      expected_output=expected_output,
      retrieval_context=[context],
    )
  scoreArray = []
  #Generates the score for each metric and adds to an array tp be returned
  for metric in ragas_metrics:
        metric.measure(test_case=test_case)
        score = metric.score
        scoreArray.append(score)
  return scoreArray


def getContext(csvQuery): #This function will get the context used to generate an answer from the index and return to be used for the metrics
    query_engine = index.as_query_engine(
        response_mode='no_text', # Set response mode to 'no_text' to only get the source nodes instead of the full response
    )
    print("this is the csv query", csvQuery)
    if len(csvQuery) == 0:
        return "No Context" #If the query is empty return no context
    query = csvQuery
    context = ''  # Initialize context as an empty string
    try:
        response = query_engine.query(query)
        for node in response.source_nodes:
            context += node.text
        print(context)
    except:
        context = "No Context"  # Reset context to "No Context" on exception
    return context  # Return the context, which will either be the accumulated text or "No Context"

if __name__ == '__main__':
    excel_file_path = "" # Add the path to the Excel file here
    output_excel_file_path = "" # Add the path to the output Excel file here

    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file_path)

    # Define new columns to be added
    new_columns = ['ContextualRelevancy', 'ContextualRecall', 'Faithfulness', 'AnswerRelevency']
    for col in new_columns:
        df[col] = None  # Initialize new columns with None values

        # Earlier parts of your code remain unchanged
    counter = 1
    # Iterate over the rows of the Excel sheet and adds the metrics for each query
    for x, row in df.iterrows():
        query = row['query ']
        output = row['output']
        expected_output = row['expected_output']
        context = getContext(query)
        # print(context)
        ragasArray = ragas(query, output, expected_output, context)
        print(ragasArray)
        
        if context == "No Context":
            for col in new_columns:
                df.at[x, col] = "No Context, Invalid"
        else:
            df.at[x, 'ContextualRelevancy'] = ragasArray[0]
            df.at[x, 'ContextualRecall'] = ragasArray[1]
            df.at[x, 'Faithfulness'] = ragasArray[2]
            df.at[x, 'AnswerRelevency'] = ragasArray[3]   

        print("Query ",counter)
        counter += 1

    # Write the updated DataFrame back to a new Excel file
    df.to_excel(output_excel_file_path, index=False)


