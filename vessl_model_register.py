import os
import sys

import vessl
from model import MNISTCNNRunner

VESSL_API_TOKEN = os.environ.get("VESSL_API_TOKEN", "")
VESSL_ORGANIZATION_NAME = os.environ.get("VESSL_ORGANIZATION", "")
VESSL_PROJECT_NAME = os.environ.get("VESSL_PROJECT", "")
VESSL_MODEL_REPOSITORY = os.environ.get("VESSL_MODEL_REPOSITORY", "")
VESSL_EXPERIMENT_NUMBER = os.environ.get("VESSL_EXPERIMENT_NUMBER", "")

if VESSL_EXPERIMENT_NUMBER == "":
    raise Exception("No experiment number provided, aborting model creation")
print(f"Registering model for experiment {VESSL_EXPERIMENT_NUMBER}")

vessl.configure(
    access_token=VESSL_API_TOKEN,
    organization_name=VESSL_ORGANIZATION_NAME,
    project_name=VESSL_PROJECT_NAME,
)

experiment = vessl.read_experiment(experiment_number=int(VESSL_EXPERIMENT_NUMBER))
if experiment.status == "failed":
    print("experiment had failed, aborting model creation")
    exit(0)

model = vessl.create_model(
    repository_name=VESSL_MODEL_REPOSITORY,
    repository_description=f"Created from jenkins job {os.environ.get('JOB_NAME', '')}".strip(),
    experiment_id=int(experiment.id),
)
vessl.register_model(
    repository_name=VESSL_MODEL_REPOSITORY,
    model_number=model.number,
    runner_cls=MNISTCNNRunner,
    requirements=["torch"],
)
print(f"Registered model: {VESSL_MODEL_REPOSITORY}/{model.number}")
