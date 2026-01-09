import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="2D & 3D Math Explorer", layout="wide")

def main():
    st.title("Partial Derivative Explorer (2D & 3D)")
    st.markdown("Visualize the function $f(x, y)$ in both 2D (Contour) and 3D (Surface).")

    # --- Sidebar Inputs ---
    with st.sidebar:
        st.header("Settings")
        func_input = st.text_input("Enter Function f(x, y):", value="x**2 - y**2")
        var_input = st.text_input("Derivative w.r.t:", value="x")
        
        st.subheader("Grid Range")
        range_val = st.slider("Axis Range (+/-)", 1.0, 10.0, 5.0)
        resolution = st.slider("Resolution (Grid Density)", 20, 100, 50)

    # --- Main Logic ---
    if func_input and var_input:
        try:
            # 1. Math Calculation (SymPy)
            x, y = sp.symbols('x y')
            expr = sp.sympify(func_input)
            var_symbol = sp.symbols(var_input)
            derivative = sp.diff(expr, var_symbol)

            # Display Math Formulas
            st.subheader("Mathematical Results")
            col1, col2 = st.columns(2)
            with col1:
                st.info("Function:")
                st.latex(f"f(x, y) = {sp.latex(expr)}")
            with col2:
                st.success(f"Partial Derivative (w.r.t {var_input}):")
                st.latex(f"\\frac{{\\partial f}}{{\\partial {var_input}}} = {sp.latex(derivative)}")

            # 2. Prepare Data for Plotting
            x_vals = np.linspace(-range_val, range_val, resolution)
            y_vals = np.linspace(-range_val, range_val, resolution)
            X, Y = np.meshgrid(x_vals, y_vals)

            # Convert to numerical function
            f_lambdified = sp.lambdify((x, y), expr, 'numpy')
            Z = f_lambdified(X, Y)

            # Handle constant functions
            if isinstance(Z, (int, float)):
                Z = np.full_like(X, Z)

            # --- Visualizations ---
            st.subheader("Visualizations")
            
            # Create Tabs for 2D and 3D
            tab1, tab2 = st.tabs(["🧊 3D Surface (Interactive)", "🗺️ 2D Contour (Top View)"])

            # Plot 1: 3D Surface
            with tab1:
                fig_3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
                fig_3d.update_layout(
                    title=f'3D Surface: {func_input}',
                    autosize=True,
                    height=600,
                    scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z')
                )
                st.plotly_chart(fig_3d, use_container_width=True)
                st.caption("Drag to rotate. Scroll to zoom.")

            # Plot 2: 2D Contour
            with tab2:
                fig_2d = go.Figure(data=[go.Contour(z=Z, x=x_vals, y=y_vals, colorscale='Viridis')])
                fig_2d.update_layout(
                    title=f'2D Contour Map: {func_input}',
                    autosize=True,
                    height=600,
                    xaxis_title='X',
                    yaxis_title='Y'
                )
                st.plotly_chart(fig_2d, use_container_width=True)
                st.caption("Darker regions are lower values, lighter regions are higher values.")

        except Exception as e:
            st.error(f"Error: {e}")
            st.warning("Please check your function syntax (e.g. use x**2 for square).")

if __name__ == "__main__":
    main()
