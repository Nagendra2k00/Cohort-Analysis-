import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Custom CSS for fonts (Quicksand for everything, including headings)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;600&display=swap');

    body {
        font-family: 'Quicksand', sans-serif;
        background-color: #f4f4f4;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Quicksand', sans-serif;
        color: #333;
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
    </style>
    """,
    unsafe_allow_html=True
)

# Main app title with Quicksand font
st.title("📊 Customer Acquisition and Retention: A Cohort Analysis")

# Sidebar for dataset information and instructions
st.sidebar.title("📝 Dataset Information")
st.sidebar.markdown("""
- 📂 Upload your CSV data in the main app.
- Explore an overview of the dataset, handle missing values, and analyze correlations.
- Visualize the data with correlation heatmaps.
""")

st.sidebar.title("💡 Tips and Instructions")
st.sidebar.info("""
- Ensure that your dataset has numeric columns to generate correlation heatmaps.
- Handle missing data wisely: you can drop rows or fill missing values.
""")

# File uploader section for CSV files
st.markdown("### 📂 Upload Data")
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, parse_dates=['InvoiceDate'])

        # Dataset overview
        st.markdown("### 📊 Dataset Overview")
        st.write(f"Shape of the dataset: {df.shape[0]} rows, {df.shape[1]} columns")
        st.dataframe(df.head())

        # Display columns and missing values
        col1, col2 = st.columns(2)

        # Column 1: Show Columns in the dataset
        with col1:
            st.markdown("### 🧾 Columns in the dataset")
            st.write(df.columns)

        # Column 2: Show Missing Values in Each Column
        with col2:
            st.markdown("### ⚠️ Missing Values in Each Column")
            st.write(df.isnull().sum())

        # Handle missing data
        st.markdown("### 🛠️ Handle Missing Data")
        missing_data_handling = st.radio(
            "Choose how to handle missing values:",
            ('Drop rows with missing values', 'Fill missing values', 'Do nothing')
        )

        if missing_data_handling == 'Drop rows with missing values':
            df = df.dropna()
            st.success("✅ Dropped rows with missing values.")
        elif missing_data_handling == 'Fill missing values':
            df.fillna({"Description": 'No Description', "CustomerID": -1}, inplace=True)
            st.success("✅ Filled missing values.")

        # Ensure 'InvoiceDate' is datetime
        if not pd.api.types.is_datetime64_any_dtype(df['InvoiceDate']):
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

        # Create 'InvoiceYearMonth' column
        df['InvoiceYearMonth'] = df['InvoiceDate'].map(lambda date: date.strftime('%Y-%m'))

        # Display the statistical summary after handling missing values
        st.markdown("### 📊 Statistical Summary of the Dataset")
        st.write(df.describe())

        # Cohort analysis
        st.markdown("### 📈 Cohort Analysis")

        # Assign cohort (first purchase month) to each customer
        df['CohortMonth'] = df.groupby('CustomerID')['InvoiceDate'] \
                               .transform('min') \
                               .dt.strftime('%Y-%m')

        # Calculate the number of months since the cohort month
        df['CohortIndex'] = ((df['InvoiceDate'].dt.year - pd.to_datetime(df['CohortMonth']).dt.year) * 12 + 
                             (df['InvoiceDate'].dt.month - pd.to_datetime(df['CohortMonth']).dt.month) + 1)

        # Group by CohortMonth and CohortIndex to get the count of unique customers
        cohort_data = df.groupby(['CohortMonth', 'CohortIndex']) \
                        .agg(n_customers=('CustomerID', 'nunique')) \
                        .reset_index()

        # Pivot the data to create a cohort table
        cohort_pivot = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='n_customers')

        # Calculate retention rate
        cohort_size = cohort_pivot.iloc[:, 0]
        retention = cohort_pivot.divide(cohort_size, axis=0)

        # Display the cohort table and retention table
        st.write("#### Cohort Counts Table")
        st.dataframe(cohort_pivot.fillna(''))

        st.write("#### Cohort Retention Table")
        st.dataframe(retention.applymap(lambda x: f"{x:.0%}" if pd.notnull(x) else ''))

        # Plotting the cohort retention heatmap
        st.write("#### Cohort Retention Heatmap")
        plt.figure(figsize=(12, 8))
        sns.heatmap(retention, annot=True, fmt='.0%', cmap='YlGnBu')
        plt.title('Cohort Retention Rates')
        plt.ylabel('Cohort Month')
        plt.xlabel('Cohort Index (Months Since First Purchase)')
        st.pyplot(plt)

        # Scatter Plot
        st.markdown("### 📊 Scatter Plot Analysis")
        st.write("Select two numeric variables to see their relationship.")

        # Identify numeric columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

        # Allow feature selection for scatter plot
        x_var = st.selectbox("Select X-axis variable", numeric_cols)
        y_var = st.selectbox("Select Y-axis variable", numeric_cols, index=1)

        if st.button("Generate Scatter Plot"):
            fig = px.scatter(df, x=x_var, y=y_var, color='Country', title=f"{y_var} vs {x_var}")
            st.plotly_chart(fig)

        # Mathematical explanation of retention rate calculation
        st.markdown("### 📐 Mathematical Calculation of Retention Rate")
        st.write("""
        Retention rate is calculated by dividing the number of customers in a cohort who made a purchase in a given month by the total number of customers in the cohort at the start. 
        The formula is:

        **Retention Rate (Month X) = (Number of Customers in Cohort who made a purchase in Month X) / (Total Number of Customers in Cohort initially)**

        For example, if 100 customers made a purchase in January and 60 of them made a purchase in February, the retention rate for February would be:

        **Retention Rate (Month 2) = 60 / 100 = 60%**
        """)

        # Displaying the cohort retention rates for each month mathematically
        st.write("Below is a visual representation of retention rates per cohort:")

        # Plotting a line chart for retention rates
        retention_line_chart = retention.T.plot(figsize=(10, 6), legend=False, marker='o')
        plt.title('Cohort Retention Rates Over Time')
        plt.ylabel('Retention Rate (%)')
        plt.xlabel('Cohort Index (Months Since First Purchase)')
        st.pyplot(plt)

    except Exception as e:
        st.error(f"🚨 An error occurred: {e}")

else:
    st.info("Please upload a CSV file to start the analysis.")

# FAQ Section using Accordion (Expander)
st.markdown("## ❓ Frequently Asked Questions (FAQ)")

with st.expander("What is Cohort Analysis?"):
    st.write("""
        Cohort analysis is a method of tracking groups of customers (cohorts) over time. A cohort is typically defined by a shared event, such as the first time a customer made a purchase. By analyzing cohorts, we can track retention rates and understand how customer behavior changes over time.
    """)

with st.expander("What do the terms 'Cohort Month' and 'Cohort Index' mean?"):
    st.write("""
        - **Cohort Month**: This represents the month in which customers made their first purchase.
        - **Cohort Index**: This represents how many months after the cohort month a customer made additional purchases. For example, a Cohort Index of 1 means purchases made in the same month as the first purchase, while 2 means purchases made one month after the first purchase.
    """)

with st.expander("What does the 'Cohort Retention Heatmap' show?"):
    st.write("""
        The heatmap visualizes customer retention over time. Each row represents a cohort (based on the month they first made a purchase), and each column shows the percentage of the original cohort that returned in subsequent months. Darker shades indicate higher retention rates, while lighter shades indicate lower retention. This helps to track the long-term behavior of customers.
    """)

with st.expander("What is the 'Cohort Retention Table'?"):
    st.write("""
        The Cohort Retention Table shows the retention rate of customers as percentages for each cohort. Each cell shows the percentage of customers from the initial cohort who made purchases in the corresponding month.
    """)

with st.expander("How is retention rate calculated?"):
    st.write("""
        Retention rate is calculated by dividing the number of customers in a cohort who made a purchase in a given month by the total number of customers in the cohort at the start. It helps businesses understand how many of their customers are coming back over time.
    """)

# Footer
st.markdown("""
<div class='footer'>
    <p style='font-weight: bold;'>🙏 Thank you for using the app!</p>
    <p style='font-size: 18px; margin-top: 10px;'>Developed by <strong>Nagendra Kumar K S</strong></p>
</div>
""", unsafe_allow_html=True)
