# Streamlit Sales Analysis Application

A multilingual web application built with Streamlit for analyzing and visualizing online store sales data. The application supports multiple languages (Russian, English, Chinese) and allows users to upload their own data for analysis.

## Features

- **Data Analysis**: Upload and analyze sales data from CSV and Excel files
- **Filtering**: Filter data by date range and city
- **KPI Metrics**: Display key performance indicators (total sales, average daily sales, maximum sales)
- **Visualizations**: Interactive charts showing sales trends over time, by city, and by day of week
- **Multilingual Support**: Interface available in Russian, English, and Chinese
- **Custom Data Upload**: Users can upload their own CSV/Excel files with supported format
- **Docker Support**: Containerized application for easy deployment

## Supported Data Format

The data file must contain the following columns:
- 'Date': sale date (in YYYY-MM-DD format)
- 'City': customer's city
- 'First Name': customer's first name
- 'Last Name': customer's last name
- 'Amount': purchase amount (numeric value)
- 'Currency': currency of the purchase (e.g., RUB, USD, EUR)

## Installation and Setup

### Prerequisites
- Python 3.11 or higher
- Docker (for containerized deployment)

### Local Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/streamlit-sales-analysis.git
cd streamlit-sales-analysis
```

2. Create a virtual environment:
```bash
python -m venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run web_app/app.py
```

The application will be available at http://localhost:8501

### Docker Deployment
1. Build the Docker image:
```bash
docker build -t streamlit-sales-app .
```

2. Run the container:
```bash
docker run -p 8501:8501 streamlit-sales-app
```

## Usage

1. Launch the application
2. Upload your sales data file (CSV or Excel format)
3. Apply filters as needed (date range, city)
4. View KPI metrics and interactive visualizations
5. Switch between languages using the language selector

## Technologies Used

- Python 3.11
- Streamlit
- Pandas
- Plotly
- OpenPyXL
- Docker

## Project Structure

```
├── .github/workflows/      # GitHub Actions workflows
├── web_app/               # Main application code
│   ├── app.py             # Main application file
│   ├── analysis.py        # Data analysis module
│   ├── data_loader.py     # Data loading module
│   ├── plotting.py        # Visualization module
│   └── pages/faq.py       # FAQ page
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── agents.md              # Agent documentation
```

## Testing

Run the application tests:
```bash
python -m pytest web_app/test_analysis.py -v
```

## Agents

The application implements a multi-agent architecture:

### 1. Data Analysis Agent
- Responsible for computing metrics and statistical analysis
- Uses the analysis.py module
- Ensures accuracy and efficiency of calculations

### 2. Visualization Agent
- Handles creation of charts and diagrams
- Uses the plotting.py module
- Provides clear data representation

### 3. Data Loading Agent
- Manages data loading and preprocessing
- Uses the data_loader.py module
- Handles various file formats (CSV, Excel)

### 4. Internationalization Agent
- Manages multilingual interface support
- Handles translations and localization
- Ensures correct display of data in different languages

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.