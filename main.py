import streamlit as st
from utils import run_python_code,run_sql_code, format_python_code, format_sql_code, optimize_python_code , regex_optimization, optimize_code
from streamlit_ace import st_ace
import textwrap

# Streamlit UI
st.title("Phoenix - Online Coding Platform")
st.write("This platform supports Python and SQL code execution, formatting, and optimization.")

# Language selection
language = st.selectbox("Select Language", ["Python", "SQL"])

# Code editor area with auto-suggestions
code = st_ace(
    language=language.lower(),  # Set the language for the editor
    theme="github",  # You can choose any theme you like
    height=300,
    placeholder="Write your code here..."
)

if language == "SQL":
    if st.button("Run Code"):
        result = run_sql_code(code)
        st.subheader("Output:")
        st.code(result)

    if st.button("Format SQL"):
        formatted_sql = format_sql_code(code)
        st.subheader("Formatted SQL Code:")
        st.code(formatted_sql)


# Button to execute the code
elif language == "Python":
    if st.button("Run Code"):
        output = run_python_code(code)
        st.subheader("Output:")
        st.code(output)
        
    if st.button("Format Python"):
        formatted_code = format_python_code(code)
        st.subheader("Formatted Python Code:")
        st.code(formatted_code)    
        
        
        

# if st.button("Format Python"):
#     formatted_code = format_python_code(code)
#     st.subheader("Formatted Python Code:")
#     st.code(formatted_code)

# if st.button("Optimize Python"):
#     optimization_result = optimize_python_code(code)
#     st.subheader("Optimization Result:")
#     st.code(optimization_result)

# code_input = st.text_area("Enter your Python code here:", height=300)
    
# if st.button("Optimize Python"):
#     if code:
#         output = optimize_python_code(code)
#         st.subheader("Optimization Result:")
#         st.text(output)
#     else:
#         st.warning("Please enter some code to optimize.")
# Newly added line

    if st.button("Optimize Python"):
        if code:
            # First, apply regex-based optimizations
            regex_optimized_code = regex_optimization(code)

            # Apply AST-based optimizations on regex-optimized code
            ast_optimized_code = optimize_code(regex_optimized_code)

            # Format the optimized code
            formatted_code = format_python_code(ast_optimized_code)

            # Display optimized code
            # st.subheader("Optimized and Formatted Code:")
            st.code(formatted_code)

            # Optionally, run the optimized code
            execution_output = run_python_code(formatted_code)
            st.subheader("Execution Output:")
            st.text(execution_output)
        else:
            st.warning("Please enter some code to optimize.")
        
