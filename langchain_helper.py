from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.prompts.chat import ChatPromptTemplate
from sqlalchemy import create_engine
from sqlalchemy.dialects.mssql import pymssql
from langchain.llms import GooglePalm
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mssql_prompt
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_experimental.sql import SQLDatabaseChain


import pyodbc
import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from few_shots import *


def get_few_shot_db_chain():
        
    # Building GooglePalm llm model 
    load_dotenv()
    llm=GooglePalm(google_api_key=os.environ['GOOGLE_API_KEY'],temperature=0)

    # Creating database object
    db = SQLDatabase.from_uri(
        database_uri="mssql+pyodbc://rohan:RadhaVallabh3@RadhaVallabha\ROHAN_SQL_SERVER/atliq_tshirts?driver=ODBC+Driver+17+for+SQL+Server",sample_rows_in_table_info=3)
    
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    to_vectorize=[" ".join(x.values()) for x in few_shots]
    vectorstore=Chroma.from_texts(to_vectorize,embedding=embeddings,metadatas=few_shots)
    example_selector=SemanticSimilarityExampleSelector(vectorstore=vectorstore,k=2)

    mssql_prompt = """You are an MS SQL expert. Given an input question, first create a syntactically correct MS SQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most 2 results using the TOP clause as per MS SQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in square brackets ([]) to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CAST(GETDATE() as date) function to get the current date, if the question involves "today".
    Use the following format:

    Question: Question here
    SQLQuery: SQL Query to run
    SQLResult: Result of the SQLQuery
    Answer: Final answer here
    No pre-amble.
    """

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    few_shot_prompt=FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=mssql_prompt,
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info"])
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True,prompt=few_shot_prompt)
    return chain


if __name__=='__main__':
    chain=get_few_shot_db_chain()
    print(chain.run("How many total Polo shirts are in stock?"))
