node {
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
}