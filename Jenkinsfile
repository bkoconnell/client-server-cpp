node {

    environment {
        NEXUS_LOGIN = 'nexuslogin'
    }

    checkout scm

    /* ***************** */
    /* TEST LINT SCRIPTS */
    /* ***************** */

    // Test Lint Directory Names
    stage('Test-Lint-Directory-Names') {
        sh 'python3 --version'
        sh 'python3 pipeline_scripts/test_lint_directory_names.py'
    }

    /* **** */
    /* LINT */
    /* **** */

    // Lint Directory Names
    stage('Lint-Directory-Names') {
        sh 'python3 --version'
        sh 'python3 pipeline_scripts/lint_directory_names.py --root . --exclude .git .vscode server/build client/build pipeline_scripts/__pycache__ pipeline_scripts/tests'
        archiveArtifacts artifacts: 'pipeline_scripts/tmp/lint_directory_names.log', followSymlinks: false
    }
    
    /* ***** */
    /* BUILD */
    /* ***** */

    // Build the Server
    stage('Build-Server') {
        sh '''
        cd server/
        bash -x build.sh
        '''
        archiveArtifacts artifacts: 'server/build/src/main', followSymlinks: false, fingerprint: true
    }

    /* ******* */
    /* DELIVER */
    /* ******* */

    // Upload build-server executable to Nexus repo
    stage('Deliver-Server-Build') {
        nexusArtifactUploader(
            credentialsId: 'nexuscredentials',
            groupId: 'server-build-gcc',
            nexusUrl: 'localhost:8081',
            nexusVersion: 'nexus3',
            protocol: 'http',
            repository: 'client-server-cpp',
            version: 'v0.1',
            artifacts: [
                [artifactId: 'main',
                classifier: 'latest',
                file: 'server/build/src/main',
                type: '']]
        )
    }
}