import streamlit as st
import sympy as sp

# Set page configuration
st.set_page_config(page_title="Partial Derivative Calculator", page_icon="∫")

def main():
    st.title("Partial Derivative Calculator")
    st.write("Enter a mathematical function and choose a variable to calculate its partial derivative.")

    # Input: The mathematical function
    func_input = st.text_input(
        "Enter a function (e.g., x**2 + y**2 + sin(x*y)):",
        value="x**2 + y**2"
    )

    # Input: The variable to differentiate with respect to
    var_input = st.text_input(
        "Variable to differentiate with respect to (e.g., x):",
        value="x"
    )

    # Button to trigger calculation
    if st.button("Calculate Derivative"):
        if not func_input or not var_input:
            st.error("Please enter both a function and a variable.")
        else:
            try:
                # Parse the variable string into a SymPy symbol
                var_symbol = sp.symbols(var_input)
                
                # Parse the function string into a SymPy expression
                # transform input to handle implicit multiplication if needed, standard python syntax preferred
                expr = sp.sympify(func_input)
                
                # Check if the variable is actually in the expression
                if var_symbol not in expr.free_symbols and not expr.is_constant():
                     st.warning(f"Note: The variable '{var_input}' does not appear in the function. The derivative will be 0.")

                # Calculate partial derivative
                derivative = sp.diff(expr, var_symbol)

                # Display results
                st.subheader("Result:")
                
                # Display the input function in LaTeX
                st.latex(f"f = {sp.latex(expr)}")
                
                # Display the derivative in LaTeX
                st.latex(f"\\frac{{\\partial f}}{{\\partial {var_input}}} = {sp.latex(derivative)}")

                st.success("Calculation successful!")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.info("Tip: Use Python syntax for math operations (e.g., use '**' for power, 'sin()' for sine).")

if __name__ == "__main__":
    main()
