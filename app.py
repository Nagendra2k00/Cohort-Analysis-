import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
        font-family: 'Arial', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .footer {
        text-align: center;
        margin-top: 20px;
        font-size: 14px;
        color: #666;
    }
    h1, h2, h3 {
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main app title with emoji
st.title("📊 Customer Acquisition and Retention: A Cohort Analysis")

# Sidebar for navigation, links, and introduction with emojis
st.sidebar.title("📌 Navigation")
st.sidebar.markdown("""
- [Upload Data](#upload-data)
- [Dataset Overview](#dataset-overview)
- [Missing Data](#handle-missing-data)
- [Correlation Heatmap](#correlation-heatmap)
- [FAQ](#faq)
""")

st.sidebar.title("💡 Introduction")
st.sidebar.info("""
This app helps you analyze customer acquisition and retention using cohort analysis. 
Upload a CSV file with your data, explore it, and visualize important correlations. 
For any questions, check the FAQ section below.
""")

# File uploader section for CSV files with emoji
st.markdown("### 📂 Upload Data")
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Display dataset overview with emojis
        st.markdown("### 📊 Dataset Overview")
        st.write(f"Shape of the dataset: {df.shape[0]} rows, {df.shape[1]} columns")

        st.markdown("### 🔍 Preview of the dataset")
        st.dataframe(df.head())  # Display first few rows

        # Display columns for 'Columns in the dataset' and 'Missing Values in Each Column'
        col1, col2 = st.columns(2)

        # Column 1: Show Columns in the dataset
        with col1:
            st.markdown("### 🧾 Columns in the dataset")
            st.write(df.columns)

        # Column 2: Show Missing Values in Each Column
        with col2:
            st.markdown("### ⚠️ Missing Values in Each Column")
            st.write(df.isnull().sum())

        # Allow user to decide how to handle missing data with emoji
        st.markdown("### 🛠️ Handle Missing Data")
        missing_data_handling = st.radio(
            "Choose how to handle missing values:",
            ('Drop rows with missing values', 'Fill missing values', 'Do nothing')
        )

        if missing_data_handling == 'Drop rows with missing values':
            df = df.dropna()
            st.success("✅ Dropped rows with missing values. Updated dataset:")
            st.write(df.head())

        elif missing_data_handling == 'Fill missing values':
            # Filling missing 'Description' and 'CustomerID' values
            df['Description'].fillna('No Description', inplace=True)
            df['CustomerID'].fillna(-1, inplace=True)
            st.success("✅ Filled missing values in 'Description' and 'CustomerID'. Updated dataset:")
            st.write(df.head())
        
        # Dataset description
        st.markdown("### 📊 Statistical Summary of the Dataset")
        st.write(df.describe())

        # Identify numeric columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

        # Heatmap visualization for numeric columns
        if len(numeric_cols) > 0:
            if st.checkbox("Show Correlation Heatmap 🔥"):
                st.markdown("### 🔍 Correlation Heatmap")

                # Explanation of the heatmap
                st.write("""
                The heatmap below shows the correlation between different numeric columns in the dataset. 
                Correlation measures the strength of a relationship between two variables. 
                Values close to 1 indicate a strong positive correlation, while values close to -1 indicate a strong negative correlation.
                A value of 0 suggests no correlation.
                """)

                plt.figure(figsize=(10, 6))
                sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', linewidths=0.5)
                st.pyplot(plt)
        else:
            st.warning("⚠️ No numeric columns available for correlation analysis.")

    except Exception as e:
        st.error(f"🚨 An error occurred: {e}")

else:
    st.info("Please upload a CSV file to start the analysis.")

# FAQ Section with Accordion style and emojis
st.markdown("### ❓ FAQ")

with st.expander("1. What type of file can I upload?"):
    st.write("You can upload CSV files. Make sure the data is properly formatted with numeric values where applicable.")
    
with st.expander("2. How can I handle missing data?"):
    st.write("You can choose to either drop rows with missing values or fill them with default values like 'No Description' or -1 for missing 'CustomerID'.")

with st.expander("3. What is a correlation heatmap?"):
    st.write("A correlation heatmap shows the relationships between numeric variables. Positive correlations are shown in red, negative correlations in blue, and no correlation in white.")
    
with st.expander("4. How should I interpret the correlation values?"):
    st.write("""
        - A correlation of 1 indicates a perfect positive relationship.
        - A correlation of -1 indicates a perfect negative relationship.
        - A correlation close to 0 indicates no linear relationship.
    """)

with st.expander("5. Can I upload Excel files?"):
    st.write("No, this app currently only supports CSV files to avoid issues with Excel dependencies.")

# Footer with emoji and markdown
st.markdown("""
<div class='footer'>
    <p style='font-weight: bold;'>🙏 Thank you for using the app!</p>
    <p style='font-size: 18px; margin-top: 10px;'>Developed by <strong>Nagendra Kumar K S</strong></p>
</div>
""", unsafe_allow_html=True)
