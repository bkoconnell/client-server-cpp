node {
    checkout scm

    /* **** */
    /* LINT */
    /* **** */

    // Lint Directory Names
    stage('Lint-Directory-Names') {
        sh 'python3 --version'
        sh 'python3 pipeline_scripts/test_lint_directory_names.py'
        sh 'python3 pipeline_scripts/lint_directory_names.py --root . --exclude .git .vscode server/build client/build pipeline_scripts/__pycache__ pipeline_scripts/tests'
    }
    
    /* ***** */
    /* BUILD */
    /* ***** */

    // Build the Server
    stage('Build-Server') {
        sh '''
        cd server/
        ./build.sh
        '''
    }
}