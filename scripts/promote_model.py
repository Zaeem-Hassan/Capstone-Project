# promote model

import os
import mlflow

def promote_model():
    # Set up DagsHub credentials for MLflow tracking
    dagshub_token = os.getenv("CAPSTONE_TEST")
    if not dagshub_token:
        raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    dagshub_url = "https://dagshub.com"
    repo_owner = "Zaeem-Hassan"
    repo_name = "Capstone-Project"

    # Set up MLflow tracking URI
    mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

    client = mlflow.MlflowClient()
    model_name = "my_model"

    try:
        # Get the model version with "staging" alias
        staging_model = client.get_model_version_by_alias(model_name, "staging")
        staging_version = staging_model.version
        print(f"Found model version {staging_version} with 'staging' alias")
    except Exception as e:
        print(f"No model found with 'staging' alias: {e}")
        # Fallback: get the latest version
        versions = client.search_model_versions(f"name='{model_name}'")
        if not versions:
            raise ValueError(f"No versions found for model '{model_name}'")
        staging_version = max(v.version for v in versions)
        print(f"Using latest version: {staging_version}")

    # Try to remove "production" alias from previous version (if exists)
    try:
        prod_model = client.get_model_version_by_alias(model_name, "production")
        print(f"Removing 'production' alias from version {prod_model.version}")
        client.delete_registered_model_alias(model_name, "production")
    except Exception:
        print("No existing 'production' alias found")

    # Set "production" alias on the staging version
    client.set_registered_model_alias(
        name=model_name,
        alias="production",
        version=staging_version
    )
    print(f"Model version {staging_version} promoted to 'production' alias")

if __name__ == "__main__":
    promote_model()