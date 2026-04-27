pipeline{
    agent any
    parameters{
        string(name:"Image_name", defaultValue:"codeexperts")
    }

    stages{
        stage ("git Checkout"){
            steps{
                git branch: 'Rel-001', url: 'https://github.com/Sukhanth-9821/mock.git'
            }

        }
        stage ("Install and Build"){
            steps{
                sh '''
                   python3 -m venv venv
                   . venv/bin/activate
                   pip install --upgrade pip
                   pip install -r requirements.txt
                '''
            }
        }
        stage ("Test"){
            steps{
                sh '''
                    venv/bin/python -m pytest
                '''
            }
        }

        stage ("Sonar"){
            steps{
                withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
                    sh '''
                    venv/bin/pysonar \
                    --sonar-host-url=http://sonarqube:9000 \
                    --sonar-token=sqp_db09236467dbaee9411d0e8c5379b698fd8d6c54 \
                    --sonar-project-key=demo2
                    '''
                }
            }
        }

        stage ("Docker Build"){
            steps{
                script{
                def dockerHome = tool 'dockertool', type: 'dockertool'
                env.PATH = "${dockerHome}/bin:${env.PATH}"
                
                sh """
                docker build -t "localhost:8085/${params.Image_name}:${env.BUILD_NUMBER} ."
                docker images
                """
            }
            }
        }
        
    }
}