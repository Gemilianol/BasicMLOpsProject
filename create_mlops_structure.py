import os

# Define the project structure as a dictionary
project_structure = {
    ".github": {
        "workflows": {
            "ci-cd.yml": ""
        }
    },
    "data": {
        "raw": {},
        "processed": {},
        "external": {}
    },
    "docs": {
        "architecture.md": ""
    },
    "notebooks": {},
    "src": {
        "app": {
            "__init__.py": "",
            "routes.py": "",
            "models.py": "",
            "utils.py": ""
        },
        "config": {
            "dev.yaml": "",
            "prod.yaml": "",
            "logging.yaml": ""
        },
        "data": {
            "data_processing.py": ""
        },
        "features": {
            "feature_engineering.py": ""
        },
        "train": {
            "train_model.py": ""
        },
        "mlflow": {
            "mlflow_tracking.py": ""
        },
        "airflow": {
            "dags": {
                "ml_workflow.py": ""
            }
        },
        "kafka": {
            "kafka_producer.py": ""
        },
        "neo4j": {
            "neo4j_connection.py": ""
        },
        "monitoring": {
            "prometheus": {},
            "grafana": {}
        },
        "deployment": {
            "k8s": {
                "deployment.yaml": "",
                "service.yaml": ""
            },
            "helm": {
                "charts": {}
            }
        }
    },
    "tests": {
        "test_app.py": "",
        "test_data_processing.py": "",
        "test_mlflow.py": "",
        "test_neo4j.py": ""
    },
    "requirements.txt": "",
    "requirements-dev.txt": "",
    "Makefile": "",
    "Dockerfile": "",
    "docker-compose.yml": "",
    "README.md": "",
    ".gitignore": "",
    ".snyk": "",
    "prometheus.yml": ""
}

# Function to create directories and files
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)  # Create directory
            create_structure(path, content)    # Recurse into subdirectory
        else:
            with open(path, 'w') as f:
                f.write(content)  # Create file with optional content

# Specify the base path as the existing folder
base_path = "BasicMLOpsProject"  # Change this to your folder name

# Create the project structure
create_structure(base_path, project_structure)
print(f"Project structure created inside '{base_path}' successfully!")

