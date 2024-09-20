# Customer Acquisition and Retention: A Cohort Analysis App

## 📊 Overview

This Streamlit application provides a comprehensive tool for performing cohort analysis on customer acquisition and retention data. It offers an intuitive interface for uploading CSV data, visualizing cohort retention, and gaining insights into customer behavior over time.

## 🌟 Features

- **Data Upload**: Easy CSV file upload functionality
- **Data Overview**: Quick glimpse of dataset shape and preview
- **Missing Data Handling**: Options to drop or fill missing values
- **Cohort Analysis**: 
  - Cohort counts table
  - Retention rate calculation
  - Interactive cohort retention heatmap
- **Scatter Plot Analysis**: Customizable scatter plots for variable relationships
- **Mathematical Explanations**: Clear breakdown of retention rate calculations
- **FAQ Section**: Comprehensive explanations of key concepts

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cohort-analysis-app.git
   cd cohort-analysis-app
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the App

Execute the following command in your terminal:

```
streamlit run app.py
```

The app will open in your default web browser.

## 📘 How to Use

1. **Upload Data**: Use the file uploader to import your CSV file.
2. **Explore Dataset**: View the dataset overview, column information, and handle missing data.
3. **Analyze Cohorts**: Examine the cohort counts table and retention rates.
4. **Visualize Data**: 
   - Study the cohort retention heatmap
   - Create custom scatter plots
5. **Learn More**: Expand the FAQ section for detailed explanations of concepts and calculations.

## 📊 Data Format

Ensure your CSV file includes the following columns:
- `InvoiceDate`: Date of purchase (YYYY-MM-DD format)
- `CustomerID`: Unique identifier for each customer
- Other relevant columns (e.g., `Quantity`, `UnitPrice`, `Country`)

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io/): For the web application framework
- [Pandas](https://pandas.pydata.org/): For data manipulation and analysis
- [Seaborn](https://seaborn.pydata.org/) & [Matplotlib](https://matplotlib.org/): For static visualizations
- [Plotly Express](https://plotly.com/python/plotly-express/): For interactive plots

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! if you want to contribute.

## 👤 Author

**Nagendra Kumar K S**

- GitHub: [@Nagendra Kumar K S](https://github.com/Nagendra2k00)
- LinkedIn: [@Nagendra Kumar K S](https://linkedin.com/in/nagendrakumarks)


Don't forget to star ⭐ this repository if you found it helpful!
