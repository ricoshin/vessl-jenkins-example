import os
import time

import vessl

VESSL_API_TOKEN = os.environ.get("VESSL_API_TOKEN", "")
VESSL_ORGANIZATION_NAME = os.environ.get("VESSL_ORGANIZATION", "")
VESSL_PROJECT_NAME = os.environ.get("VESSL_PROJECT", "")
VESSL_CLUSTER_NAME = os.environ.get("VESSL_CLUSTER_NAME", "aws-apne2-prod1")
VESSL_RESOURCE_SPEC_NAME = os.environ.get("VESSL_RESOURCE_SPEC_NAME", "v1.cpu-4.mem-13")
VESSL_KERNEL_IMAGE_URL = os.environ.get("VESSL_KERNEL_IMAGE_URL", "quay.io/vessl-ai/kernels:py38-202303150331")
GIT_COMMIT = os.environ.get("GIT_COMMIT", "")
JENKINS_BUILD_TAG = os.environ.get("BUILD_TAG", "")
timeout = 30 * 60   # 30 minutes

vessl.configure(
    access_token=VESSL_API_TOKEN,
    organization_name=VESSL_ORGANIZATION_NAME,
    project_name=VESSL_PROJECT_NAME,
)
try:
    experiment = vessl.create_experiment(
        cluster_name=VESSL_CLUSTER_NAME,
        kernel_resource_spec_name=VESSL_RESOURCE_SPEC_NAME,
        kernel_image_url=VESSL_KERNEL_IMAGE_URL,

        git_ref_mounts=[f"/model:github/vessl-ai/jenkins-test/{GIT_COMMIT}"], # <provider>/<owner>/<repo>/<commit>
        start_command=f"pip install -r /model/requirements.txt && python /model/main.py --save-model --save-image",
        message=f"Created by Jenkins build: {JENKINS_BUILD_TAG}"
    )
    experiment_id = experiment.id
    print(f"Spawned experiment: {VESSL_ORGANIZATION_NAME}/{VESSL_PROJECT_NAME}:{experiment.number}")
    with open("./vessl-experiment-number.txt", "w") as f:
        f.write(str(experiment.number))

    start = time.time()
    while experiment.status in ["running", "initializing", "queued", "pending"]:
        time.sleep(30)
        new_experiment = vessl.read_experiment_by_id(experiment_id=int(experiment_id))
        if new_experiment is not None:
            experiment = new_experiment
        if time.time() - start > timeout:
            raise Exception("Experiment timed out")
        print("Waiting for experiment to complete...")



except Exception as e:
    print(e)
    exit(1)
