#!groovy

pipeline {
    agent any
    options {
      timeout(time: 3, unit: 'MINUTES')
    }

    stages {
      stage ('Build binary file') {
        steps {
            sh 'scripts/build.sh'
        }
      }

      // TODO: Run linter
      // TODO: reformat code
      // TODO: Build OpenWrt/LEDE package
    }
    // TODO: add post block for Slack.
}
