pipeline {
  agent {
    kubernetes {
      label 'vessl-jenkins'
      yamlFile 'jenkins-agent.yaml'
    }

  }
  stages {
    stage('Checkout') {
      steps {
        git(branch: 'main', credentialsId: 'github-repository-credential	', url: 'https://github.com/vessl-ai/vessl-jenkins-example.git')
      }
    }

    stage('Create vessl remote experiment') {
      steps {
        container(name: 'vessl') {
          sh 'pip install -r requirements.txt'
          sh 'python -u vessl_run_experiment.py'
          script {
            expr_number = readFile('vessl-experiment-number.txt').trim()
            println "Experiment number: ${expr_number}"
            VESSL_EXPERIMENT_NUMBER = "${expr_number}"
          }
        }
      }
    }

    stage('Register model') {
      steps {
        container(name: 'vessl') {
          script {
            println "Experiment number to register: ${VESSL_EXPERIMENT_NUMBER}"
          }
          sh 'VESSL_EXPERIMENT_NUMBER=$(cat vessl-experiment-number.txt) python -u vessl_model_register.py'
        }
      }
    }

  }
  environment {
    VESSL_API_TOKEN = credentials('vessl-api-token')
    VESSL_ORGANIZATION = 'vessl-ai'
    VESSL_PROJECT = 'jenkins-test'
    VESSL_MODEL_REPOSITORY = 'jenkins-test'
    VESSL_CLUSTER_NAME = 'aws-apne2-prod1'
    VESSL_RESOURCE_SPEC_NAME = 'v1.cpu-4.mem-13'
    VESSL_KERNEL_IMAGE_URL = 'quay.io/vessl-ai/kernels:py38-202303150331'
    VESSL_EXPERIMENT_NUMBER = ''
  }
}
