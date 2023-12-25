from langchain_helper import *

import streamlit as st
st.title("Atliq T-Shirts Database QA 👕")
question=st.text_input("Ask Your Question:")
if question:
    chain=get_few_shot_db_chain()
    answer=chain.run(question)
    st.header("Answer:")
    st.write(answer)