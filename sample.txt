pipeline{
    agent any
    parameters {
        string(name: "IMAGE_TAG", defaultValue: "70", description: "Enter Image Tag:")
        choice(name: "DEPLOY_ENV", choices: ["QA", "PROD"], description: "Select Environment")
    }
    environment{
        GIT_REPO = "https:///${gituser}:${gitpasswd}@github.com/Sukhanth-9821/codeexpert_deployment.git"
        BRANCH = 'master'
        FILE_PATH = "${params.DEPLOY_ENV == 'QA' ? 'gistapi/dev/values.yaml' : 'gistapi/prod/values.yaml'}"
    }
    stages{
        stage ("SCM Clone"){
            steps{
                git 'https://github.com/Sukhanth-9821/codeexpert_deployment.git'
            }

        }
        stage ("Update Version"){
            steps{
                sh """ sed -i 's/tag: .*/tag: ${params.IMAGE_TAG}/g' ${FILE_PATH} 
                cat ${FILE_PATH} 
                """
            }

        }
        stage ("Approval for PROD"){
            when {
                expression { params.DEPLOY_ENV == "PROD" }
            }
            steps {
                input message: "Deploying to PROD. Do you approve?", ok: "Yes, Deploy"
            }
        }
        stage ("git push"){
            steps{
            withCredentials([usernamePassword(credentialsId: 'gitCred', passwordVariable: 'gitpasswd',
             usernameVariable: 'gituser')]) {



            sh """ 

            git config user.email "sukhanthwhitehat@gmail.com"
            git config user.name "sukhanth"
            git add ${FILE_PATH} 
            git commit -m "Update image tag to ${params.IMAGE_TAG}" || echo "No changes to commit" 
            git push "https:///${gituser}:${gitpasswd}@github.com/Sukhanth-9821/codeexpert_deployment.git" ${BRANCH} 
            
            """

                }
            }
        }
        stage ("Argo deployment"){
            steps{
                sh """
                echo "Argo URL:https://localhost:8090/applications/argocd/gistapi-repo-app"
                echo "Deploying using Argocd"
                """
            }
        }
       
    }
}
