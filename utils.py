import io
import sys
import subprocess
import ast
import textwrap
import re
import sqlparse
import sqlite3
import black
import astor

class CodeOptimizer(ast.NodeTransformer):
    def visit_ListComp(self, node):
        # Convert list comprehensions to generator expressions where appropriate
        return ast.GeneratorExp(
            elt=node.elt,
            generators=node.generators
        )

    def visit_For(self, node):
        # Convert for loops to list comprehensions if applicable
        if isinstance(node.target, ast.Name) and isinstance(node.iter, ast.List):
            return ast.ListComp(
                elt=node.body[0].value,
                generators=[ast.comprehension(target=node.target, iter=node.iter, ifs=[])]
            )
        return self.generic_visit(node)

def optimize_code(source_code):
    # Parse the code into an AST
    tree = ast.parse(source_code)
    
    # Optimize the AST
    optimizer = CodeOptimizer()
    optimized_tree = optimizer.visit(tree)
    
    # Unparse the optimized AST back to source code using astor
    optimized_code = astor.to_source(optimized_tree)
    
    return optimized_code

def regex_optimization(source_code):
    # Define regex-based optimizations
    optimizations = {
        # Original to Optimized for counting matching characters
        r'A\s*=\s*\'([^\']+)\'\s*;\s*B\s*=\s*\'([^\']+)\'\s*;\s*N1\s*=\s*len\(A\)\s*;\s*N2\s*=\s*len\(B\)\s*;\s*i\s*=\s*0\s*;\s*C\s*=\s*0\s*;\s*while\s*\(N1\s*!=\s*0\s*and\s*N2\s*!=\s*0\):\s*if\s*A\[i\]==B\[i\]:\s*C\+=1\s*i\+=1\s*N1\-=1\s*N2\-=1\s*print\(C\)':
            r'''
A = '\1'
B = '\2'
C = sum(1 for a, b in zip(A, B) if a == b)
print(C)
            ''',
        # Example: Optimizing a loop for summing numbers
        r'(?P<name>\w+)\s*=\s*0\s*;\s*for\s*(?P<var>\w+)\s*in\s*range\((?P<start>\d+),\s*(?P<end>\d+)\):\s*{?\s*(?P<name2>\w+)\s*\+=\s*(?P<var2>\w+)\s*;?\s*}':
            r'''
{name} = sum(range({start}, {end}))
print({name})
            ''',
        # Add more optimizations as needed
    }

    # Apply regex optimizations
    for pattern, replacement in optimizations.items():
        source_code = re.sub(pattern, replacement, source_code, flags=re.DOTALL)

    return source_code

def run_python_code(code):
    output = io.StringIO()
    sys.stdout = output  # Redirect stdout to capture print output

    exec_globals = {}
    try:
        exec(code, exec_globals)
        return output.getvalue() if output.getvalue() else "No output produced."
    except Exception as e:
        return f"Error during execution: {e}"
    finally:
        sys.stdout = sys.__stdout__  # Reset redirect.

def execute_sql_query(query):
    try:
        connection = sqlite3.connect(":memory:")  # Create an in-memory database
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()  # Commit changes if it's an INSERT/UPDATE/DELETE
        results = cursor.fetchall()  # Fetch results for SELECT queries
        return results
    except Exception as e:
        return f"Error: {e}"
    finally:
        connection.close()  # Ensure the connection is closed

def run_sql_code(code):
    output = []
    # Split the input code into individual SQL statements
    statements = sqlparse.split(code)
    
    try:
        connection = sqlite3.connect(":memory:")  # Create an in-memory database
        cursor = connection.cursor()
        for statement in statements:
            statement = statement.strip()  # Clean up whitespace
            if statement:  # Skip empty statements
                cursor.execute(statement)
                connection.commit()  # Commit changes if it's an INSERT/UPDATE/DELETE
                if statement.lower().startswith("select"):
                    results = cursor.fetchall()  # Fetch results for SELECT queries
                    output.append(results)
        return output
    except Exception as e:
        return f"Error: {e}"
    finally:
        connection.close()  # Ensure the connection is closed

def format_python_code(code):
    try:
        return black.format_str(code, mode=black.Mode())
    except Exception as e:
        return f"Error: {e}"

def format_sql_code(code):
    return sqlparse.format(code, reindent=True, keyword_case='upper')

def optimize_python_code(code):
    # Save code to a temporary file with proper format and docstring
    with open("temp_code.py", "w", newline='\n') as file:
        file.write('"""Temporary code for pylint optimization."""\n')  # Adding a module docstring
        file.write(code.replace('\r\n', '\n').strip() + "\n")
    
    # Run pylint on the temporary file
    result = subprocess.run(
        ["pylint", "temp_code.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Clean up the temporary file
    subprocess.run(["del", "temp_code.py"], shell=True)  # Use `rm` for Unix-based systems

    # Check if pylint returned any output
    if result.stdout:
        return result.stdout
    else:
        return "No pylint output or an error occurred: " + result.stderr

