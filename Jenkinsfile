pipeline {
    agent any

    environment {
        REMOTE_USER = 'ubuntu'
        REMOTE_HOST = '3.110.120.39'
        REMOTE_DIR = '/opt/custom-addon'
        GITHUB_REPO = 'https://github.com/jatincreliution/Odoo-module.git'
        BRANCH = 'main'  // Change branch if necessary
    }
    
    triggers {
        githubPush()  // Trigger on push
    }

    stages {
        stage('Deploy to Odoo Server') {
            steps {
                sshagent(['odoo-ssh-key']) {
                    sh """
                        # SSH into the server, and create the directory as odoo18 user
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} \\
                        'sudo mkdir -p ${REMOTE_DIR} && sudo chown -R odoo18:odoo18 ${REMOTE_DIR}'

                        # Now pull the repo, again as odoo18 user
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} \\
                        'if [ -d "${REMOTE_DIR}/.git" ]; then \\
                             cd ${REMOTE_DIR} && git pull origin ${BRANCH}; \\
                         else \\
                             sudo -u odoo18 git clone ${GITHUB_REPO} ${REMOTE_DIR}; \\
                         fi'
                    """
                }
            }
        }

        stage('Restart Odoo') {
            steps {
                sshagent(['odoo-ssh-key']) {
                    sh """
                        # Restart Odoo service
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} \\
                        'sudo systemctl restart odoo18'
                    """
                }
            }
        }
    }
}
