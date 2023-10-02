node {
    stage('BuildServer') {
        sh '''
            cd server
            BUILD_DIR=build
            [ -d ${BUILD_DIR} ] && rm -rf ${BUILD_DIR}
            mkdir ${BUILD_DIR} && cd ${BUILD_DIR}
            cmake ..
            make
        '''
    }
}