pipeline{
    agent any

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
    }
}