pipeline{
    agent any

    stages{
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage ("git checkout"){
            steps{
                git branch: 'newbranch', url: 'https://github.com/Sukhanth-9821/newrepo_1.git'
            }
        }
        stage("Build"){
            steps{
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }
        stage("test"){
            steps{
                sh '''
                venv/bin/python -m pytest
                '''
            }
        }
        stage("sonarqube Analysis"){
            steps{
                script{
                def scannerHome = tool 'SonarScanner'
                withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
                    sh """
                    echo "SONAR SCANNERRR: ${scannerHome}"
                    ${scannerHome}/bin/sonar-scanner \
                    -Dsonar.projectKey=demo \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://sonarqube:9000 \
                    -Dsonar.login=$SONAR_TOKEN
                    """
                }
                }
            }
        }

        stage("Build Docker Image"){
            steps{
                script{
                    def dockerHome = tool name: 'dockertool', type: 'dockerTool'
                    
                    // Add Docker to PATH
                    env.PATH = "${dockerHome}/bin:${env.PATH}"

                    env.IMAGENAME = "localhost:8085/codeexperts:${env.BUILD_NUMBER}"
                    echo "Building Docker File with tag ${env.IMAGENAME}"
                    sh """
                    docker build -t ${env.IMAGENAME} .
                    docker images
                    """

                }
            }
        }
        stage ("Trivy Scan"){
	    steps {
		sh """
		    trivy image ${env.IMAGENAME}
		"""
	    }
	}
        
        
        stage("Nexus Login and Push"){
            steps{
                script{
                    withCredentials([usernamePassword(credentialsId: 'nexus-cred', passwordVariable: 'nexus_paswd', usernameVariable: 'nexus_user')]) {
                        
                        sh """
                        docker login localhost:8085 -u $nexus_user -p $nexus_paswd
                        docker push ${env.IMAGENAME}
                        
                        """
                    }
                 }
            }
        }
    }

}
