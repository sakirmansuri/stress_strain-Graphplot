import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

def plot_stress_strain(d, L, P_values, l_values):
    # Calculate cross-sectional area
    A = (np.pi / 4) * (d ** 2)
    
    # Compute strain and stress values
    strain_values = [(L - l) / L for l in l_values]
    stress_values = [P / A for P in P_values]
    
    # Sort values to ensure smooth interpolation
    sorted_data = sorted(zip(strain_values, stress_values))
    strain_values, stress_values = zip(*sorted_data)
    
    # Generate smooth curve using interpolation
    strain_smooth = np.linspace(min(strain_values), max(strain_values), 300)
    stress_smooth = make_interp_spline(strain_values, stress_values, k=3)(strain_smooth)
    
    # Plot graph
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(strain_smooth, stress_smooth, color='b', linestyle='-', label='Smooth Stress-Strain Curve')
    ax.plot(strain_values, stress_values, color='g', linestyle='--', marker='o', label='Data Points')
    
    # Marking key points
    labels = ["Zero Load", "Initial Load", "Elastic Limit", "Yield Point", "Lower Yield Point", "UTS", "Fracture"]
    for i, txt in enumerate(labels):
        ax.scatter(strain_values[i], stress_values[i], color='r')
        ax.text(strain_values[i], stress_values[i], txt, fontsize=9, verticalalignment='bottom')
    
    # Labels and Title
    ax.set_xlabel("Strain")
    ax.set_ylabel("Stress (N/mm²)")
    ax.set_title("Stress-Strain Curve")
    ax.legend()
    ax.grid(True)
    
    # Display plot in Streamlit
    st.pyplot(fig)

# Streamlit UI
st.title("Stress-Strain Curve Generator By Sakir")
st.sidebar.header("Input Parameters")

d = st.sidebar.number_input("Enter the diameter (mm):", min_value=1.0, value=10.0, step=0.1)
L = st.sidebar.number_input("Enter the initial length (mm):", min_value=1.0, value=100.0, step=0.1)

labels = ["Zero Load", "Initial Load", "Elastic Limit", "Yield Point", "Lower Yield Point", "Maximum Load (UTS)", "Fracture Load"]
P_values = []
l_values = []

st.sidebar.subheader("Load Inputs (N)")
for label in labels:
    P_values.append(st.sidebar.number_input(f"{label}:", min_value=0.0, value=1000.0, step=100.0))

st.sidebar.subheader("Corresponding Lengths (mm)")
for label in labels:
    l_values.append(st.sidebar.number_input(f"Length at {label}:", min_value=1.0, value=99.0, step=0.1))

if st.sidebar.button("Generate Stress-Strain Graph"):
    plot_stress_strain(d, L, P_values, l_values)
