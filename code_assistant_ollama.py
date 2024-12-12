import streamlit as st
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

model = OllamaLLM(model="codellama")

completion_template = """
You are an AI for Python code completion. Your task is to complete the given Python code snippet. Ensure the code is syntactically and logically correct.

Code Snippet: {context}

Complete the code:
"""

optimization_template = """
You are an AI for optimizing Python code. Your task is to improve the given Python code snippet by making it more efficient, readable, and following best practices.

Code Snippet: {context}

Optimize the code:
"""

review_template = """
You are an AI for reviewing Python code. Your task is to find potential bugs, logical errors, or stylistic issues in the given Python code snippet, and suggest fixes or improvements.

Code Snippet: {context}

Review and fix the code:
"""

completion_prompt = ChatPromptTemplate.from_template(template=completion_template)
optimization_prompt = ChatPromptTemplate.from_template(template=optimization_template)
review_prompt = ChatPromptTemplate.from_template(template=review_template)

completion_chain = completion_prompt | model
optimization_chain = optimization_prompt | model
review_chain = review_prompt | model

def complete_code(code_snippet):
    try:
        result = completion_chain.invoke({"context": code_snippet})
        if isinstance(result, str):
            return result.strip()
        else:
            return "Unexpected result format."
    except Exception as e:
        return f"Error generating code: {e}"

def optimize_code(code_snippet):
    try:
        result = optimization_chain.invoke({"context": code_snippet})
        if isinstance(result, str):
            return result.strip()
        else:
            return "Unexpected result format."
    except Exception as e:
        return f"Error optimizing code: {e}"

def review_code(code_snippet):
    try:
        result = review_chain.invoke({"context": code_snippet})
        if isinstance(result, str):
            return result.strip()
        else:
            return "Unexpected result format."
    except Exception as e:
        return f"Error reviewing code: {e}"

if 'in_code' not in st.session_state:
    st.session_state.in_code = ''

if 'completed_code' not in st.session_state:
    st.session_state.completed_code = ''

if 'optimized_code' not in st.session_state:
    st.session_state.optimized_code = ''

if 'reviewed_code' not in st.session_state:
    st.session_state.reviewed_code = ''

code_input = st.text_area("Enter your Python code snippet:", value=st.session_state.in_code, height=200)

if st.button('Generate Code Completion'):
    code_to_complete = code_input.strip()
    if code_to_complete:
        completed_code = complete_code(code_to_complete)
        if completed_code.startswith("Error"):
            st.error(completed_code)
        else:
            st.session_state.completed_code = completed_code
            st.success("Code completion generated!")
    else:
        st.warning("Please enter some code to complete!")

if st.button('Optimize Code'):
    code_to_optimize = code_input.strip()
    if code_to_optimize:
        optimized_code = optimize_code(code_to_optimize)
        if optimized_code.startswith("Error"):
            st.error(optimized_code)
        else:
            st.session_state.optimized_code = optimized_code
            st.success("Code optimization completed!")
    else:
        st.warning("Please enter some code to optimize!")

if st.button('Review and Fix Code'):
    code_to_review = code_input.strip()
    if code_to_review:
        reviewed_code = review_code(code_to_review)
        if reviewed_code.startswith("Error"):
            st.error(reviewed_code)
        else:
            st.session_state.reviewed_code = reviewed_code
            st.success("Code review and fixes completed!")
    else:
        st.warning("Please enter some code to review and fix!")

if st.session_state.completed_code:
    st.text_area("Completed Code", value=st.session_state.completed_code, height=200)

if st.session_state.optimized_code:
    st.text_area("Optimized Code", value=st.session_state.optimized_code, height=200)

if st.session_state.reviewed_code:
    st.text_area("Reviewed and Fixed Code", value=st.session_state.reviewed_code, height=200)

if st.button("Reset Editor"):
    st.session_state.in_code = ""
    st.session_state.completed_code = ""
    st.session_state.optimized_code = ""
    st.session_state.reviewed_code = ""
    st.success("Editor cleared!")
