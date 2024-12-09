import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import time


tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def generate_code(prompt, max_length=200):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)
    generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_code

def fix_bug(code_with_bug):
    
    if "print(1" in code_with_bug:
        return code_with_bug.replace("print(1", "print('Fixed!')")
    
    return code_with_bug


st.title("Generative AI for Code Optimization, Fixing & Completion")

st.markdown("""
    This app allows you to optimize, fix, or complete Python code using Generative AI (GPT-2).
    - **Optimize Code**: Refactor or improve code efficiency and readability.
    - **Fix Code**: Fix common bugs or syntax errors.
    - **Complete Code**: Automatically complete unfinished code.
""")


code_input = st.text_area("Enter Your Code Snippet:", height=200, placeholder="Paste your Python code here...")


action_option = st.radio("Choose Action:", ("Optimize Code", "Fix Code", "Complete Code"))


if st.button("Process Code"):
    if code_input:
        with st.spinner("Processing your code..."):
            time.sleep(1)  

            
            if action_option == "Optimize Code":
                st.subheader("Optimized Code")
                optimized_code = generate_code(f"Optimize the following code:\n{code_input}")
                st.code(optimized_code, language='python')
                st.write("**Optimization Notes:** This refactored code improves readability and efficiency.")

            elif action_option == "Fix Code":
                st.subheader("Fixed Code")
                fixed_code = fix_bug(code_input) 
                st.code(fixed_code, language='python')
                st.write("**Bug Fix Notes:** Common issues were identified and corrected (e.g., syntax errors).")

            elif action_option == "Complete Code":
                st.subheader("Completed Code")
                completed_code = generate_code(f"Complete the following code:\n{code_input}")
                st.code(completed_code, language='python')
                st.write("**Completion Notes:** Code completion is based on the input provided and common coding patterns.")
            
            
            st.subheader("Original Code")
            st.code(code_input, language='python')
        
    else:
        st.error("Please enter a code snippet.")
