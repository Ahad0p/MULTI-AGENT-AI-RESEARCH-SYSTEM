@Library('Shared') _

pipeline {

agent { label "ahad" }

environment {
    SONAR_HOME = tool "Sonar"
}

parameters {
    string(
        name: 'DOCKER_TAG',
        defaultValue: '',
        description: 'Docker image tag'
    )
}

stages {

    stage("Validate Parameters") {
        steps {
            script {
                if (params.DOCKER_TAG == '') {
                    error("DOCKER_TAG must be provided")
                }
            }
        }
    }

    stage("Workspace Cleanup") {
        steps {
            script {
                cleanWs()
            }
        }
    }

    stage("Git: Code Checkout") {
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

    stage("SonarQube: Code Analysis") {
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
}

post {

    success {

        archiveArtifacts(
            artifacts: '*.xml',
            allowEmptyArchive: true
        )

        build job: "Multi-Agent-GitOps",
        parameters: [
            string(
                name: 'DOCKER_TAG',
                value: "${params.DOCKER_TAG}"
            )
        ]
    }

    failure {

        emailext(
            attachLog: true,
            subject: "CI Pipeline Failed - ${env.JOB_NAME}",
            body: """
            Build Failed

            Project: ${env.JOB_NAME}
            Build Number: ${env.BUILD_NUMBER}

            ${env.BUILD_URL}
            """,
            to: "ahadkhan.ai306@gmail.com"
        )
    }
}

}
