# MLOps Project: Inflation Prediction

## Overview

This project is an MLOps pipeline designed to predict inflation rates using economic indicators such as exchange rates, money supply, interest rates, and commodity prices. The pipeline integrates best practices for machine learning development, deployment, and monitoring.

Key highlights:
- **Data Processing:** Cleaning, aggregation, and feature engineering for time series data.
- **Model Training:** Comparison of AutoARIMA and Multiple Linear Regression models.
- **Deployment:** Docker and Kubernetes-based production setup with monitoring.
- **Monitoring:** Prometheus and Grafana integration for performance tracking.

## Quickstart

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mlops_project.git
   cd mlops_project

2. Create and activate a virtual environment:
python -m venv myvenv
source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

Training the Model
Run the training script:
python src/train/train_model.py
This script trains the models and saves the best one in the models/ directory.

Running the Application
To start the Flask application locally:
python src/app/routes.py

For Docker:
docker-compose up

Documentation
Detailed documentation can be found in the docs/ directory:

Project Architecture
Model Training and Evaluation

Contributing
Contributions are welcome! Please see the CONTRIBUTING.md file for guidelines.


