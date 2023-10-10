node {
    checkout scm

    // Build the Server
    stage('BuildServer') {
        sh '''
            cd server/
            ./build.sh
        '''
    }
}