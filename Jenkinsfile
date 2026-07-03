pipeline {
    agent any

    environment {
        ACR_REGISTRY = 'registry.cn-hangzhou.aliyuncs.com/uscene'
        ACR_CREDS   = credentials('acr-creds')
        KUBECONFIG  = credentials('kubeconfig-test')
        IMAGE_TAG   = "${BUILD_NUMBER}-${GIT_COMMIT.take(7)}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${ACR_REGISTRY}/uscene-backend:${IMAGE_TAG} ."
                sh "docker tag ${ACR_REGISTRY}/uscene-backend:${IMAGE_TAG} ${ACR_REGISTRY}/uscene-backend:test-latest"
            }
        }

        stage('Push to ACR') {
            steps {
                sh "docker login -u ${ACR_CREDS_USR} -p ${ACR_CREDS_PSW} ${ACR_REGISTRY}"
                sh "docker push ${ACR_REGISTRY}/uscene-backend:${IMAGE_TAG}"
                sh "docker push ${ACR_REGISTRY}/uscene-backend:test-latest"
            }
        }

        stage('Run Migrate Job') {
            steps {
                sh '''
                    # Delete old migrate job if exists
                    kubectl --kubeconfig=${KUBECONFIG} delete job uscene-migrate -n uscene-test --ignore-not-found

                    # Substitute env vars in YAML and apply
                    export ACR_REGISTRY IMAGE_TAG
                    envsubst < k8s/migrate-job.yaml | \
                    kubectl --kubeconfig=${KUBECONFIG} apply -f -

                    # Wait for migration to complete
                    kubectl --kubeconfig=${KUBECONFIG} wait --for=condition=complete \
                        job/uscene-migrate -n uscene-test --timeout=120s
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    kubectl --kubeconfig=${KUBECONFIG} \
                        set image deployment/uscene-backend \
                        backend=${ACR_REGISTRY}/uscene-backend:${IMAGE_TAG} \
                        -n uscene-test
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                    kubectl --kubeconfig=${KUBECONFIG} \
                        rollout status deployment/uscene-backend \
                        -n uscene-test --timeout=120s
                '''
            }
        }
    }

    post {
        failure {
            echo "Deploy FAILED: uscene-backend ${IMAGE_TAG}"
        }
        success {
            echo "Deploy OK: uscene-backend ${IMAGE_TAG}"
        }
    }
}
