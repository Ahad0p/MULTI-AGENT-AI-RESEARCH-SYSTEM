@Library('Shared') _

pipeline {
agent { label "ahad" }

```
environment {
    SONAR_HOME = tool "Sonar"
    IMAGE_NAME = "ahadkhan021/multi-agent-ai-research-system"
}

parameters {
    string(
        name: 'DOCKER_TAG',
        defaultValue: 'latest',
        description: 'Docker Image Tag'
    )
}

stages {

    stage("Workspace Cleanup") {
        steps {
            cleanWs()
        }
    }

    stage("Git: Checkout Code") {
        steps {
            script {
                code_checkout(
                    "https://github.com/Ahad0p/MULTI-AGENT-AI-RESEARCH-SYSTEM.git",
                    "main"
                )
            }
        }
    }

    stage("Trivy: Filesystem Scan") {
        steps {
            script {
                trivy_scan()
            }
        }
    }

    stage("OWASP: Dependency Check") {
        steps {
            script {
                owasp_dependency()
            }
        }
    }

    stage("SonarQube: Analysis") {
        steps {
            script {
                sonarqube_analysis(
                    "Sonar",
                    "multi-agent-research",
                    "multi-agent-research"
                )
            }
        }
    }

    stage("SonarQube: Quality Gate") {
        steps {
            script {
                sonarqube_code_quality()
            }
        }
    }

    stage("Docker: Build Image") {
        steps {
            script {
                docker_build(
                    "multi-agent-ai-research-system",
                    "${params.DOCKER_TAG}",
                    "ahadkhan021"
                )
            }
        }
    }

    stage("Docker: Push Image") {
        steps {
            script {
                docker_push(
                    "multi-agent-ai-research-system",
                    "${params.DOCKER_TAG}",
                    "ahadkhan021"
                )
            }
        }
    }

    stage("Kubernetes: Deploy") {
        steps {
            script {

                withCredentials([
                    string(credentialsId: 'groq-api-key', variable: 'GROQ_API_KEY'),
                    string(credentialsId: 'tavily-api-key', variable: 'TAVILY_API_KEY')
                ]) {

                    sh '''
                    kubectl create namespace multi-agent-research --dry-run=client -o yaml | kubectl apply -f -

                    kubectl create secret generic multi-agent-research-secrets \
                      --namespace=multi-agent-research \
                      --from-literal=GROQ_API_KEY=$GROQ_API_KEY \
                      --from-literal=TAVILY_API_KEY=$TAVILY_API_KEY \
                      --dry-run=client -o yaml | kubectl apply -f -

                    kubectl apply -f k8s/configmap.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    '''
                }
            }
        }
    }

    stage("Verify Deployment") {
        steps {
            sh '''
            kubectl get pods -n multi-agent-research
            kubectl get svc -n multi-agent-research
            '''
        }
    }
}

post {

    success {
        archiveArtifacts artifacts: '*.xml', followSymlinks: false
        echo "Pipeline completed successfully."
    }

    failure {
        echo "Pipeline failed."
    }
}
```

}
