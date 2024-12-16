pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "localhost:5000"  // 本地 Docker Registry 地址
        DOCKER_IMAGE_NAME = "hello-container"  // 镜像名称
        GIT_REPO = "https://github.com/yinzhipeng123/kafka_demo.git"  // GitHub 项目地址
        DOCKER_USERNAME = "myuser"  // 本地 Docker Registry 用户名
        DOCKER_PASSWORD = "ganxie123!"  // 本地 Docker Registry 密码
    }

    stages {
        stage('Checkout') {
            steps {
                // 拉取 GitHub 项目
                git url: "${GIT_REPO}", branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // 创建 Dockerfile
                    sh '''
                    echo "FROM python:3.9-slim" > Dockerfile
                    echo "COPY hello.py /app/hello.py" >> Dockerfile
                    echo "CMD python -u /app/hello.py" >> Dockerfile
                    '''
                    // 构建 Docker 镜像
                    sh "docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Login to Docker Registry') {
            steps {
                script {
                    // 登录到本地 Docker Registry
                    sh "echo ${DOCKER_PASSWORD} | docker login ${DOCKER_REGISTRY} -u ${DOCKER_USERNAME} --password-stdin"
                }
            }
        }

        stage('Push to Local Registry') {
            steps {
                script {
                    // 推送 Docker 镜像到本地 Docker Registry
                    sh "docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:latest"
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    // 启动容器并确保它持续输出 hello.py 的结果
                    sh "docker run -d --rm ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:latest"
                }
            }
        }
    }
}
