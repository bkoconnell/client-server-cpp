#!/usr/bin/env bash
set -euox pipefail

BUILD_DIR=build

# If a build directory exists, recursively remove it
[ -d ${BUILD_DIR} ] && rm --recursive --force ${BUILD_DIR}

# Then make a new build directory
mkdir ${BUILD_DIR} && cd ${BUILD_DIR}

# Configure the CMake project and generate the build system
cmake ..

# Call the build system to compile/link the project
cmake --build .

# Capture errors on stderr
error() {
    printf "${red}!!! %s${reset}\\n" "${*}" 1>&2
  }