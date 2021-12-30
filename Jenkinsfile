// Example Jenkins pipeline with Cypress end-to-end tests running in parallel on 2 workers
// Pipeline syntax from https://jenkins.io/doc/book/pipeline/

// Setup:
//  before starting Jenkins, I have created several volumes to cache
//  Jenkins configuration, NPM modules and Cypress binary

// docker volume create jenkins-data
// docker volume create npm-cache
// docker volume create cypress-cache

// Start Jenkins command line by line:
//  - run as "root" user (insecure, contact your admin to configure user and groups!)
//  - run Docker in disconnected mode
//  - name running container "blue-ocean"
//  - map port 8080 with Jenkins UI
//  - map volumes for Jenkins data, NPM and Cypress caches
//  - pass Docker socket which allows Jenkins to start worker containers
//  - download and execute the latest BlueOcean Docker image

// docker run \
//   -u root \
//   -d \
//   --name blue-ocean \
//   -p 8080:8080 \
//   -v jenkins-data:/var/jenkins_home \
//   -v npm-cache:/root/.npm \
//   -v cypress-cache:/root/.cache \
//   -v /var/run/docker.sock:/var/run/docker.sock \
//   jenkinsci/blueocean:latest

// If you start for the very first time, inspect the logs from the running container
// to see Administrator password - you will need it to configure Jenkins via localhost:8080 UI
//    docker logs blue-ocean

pipeline {
  agent none

  stages {
    

    stage('locust load tests') {
      environment {
        // we will be recording test results aon JTL Reporter
        // to record we need to set an environment variable
        JTL_API_TOKEN="at-c7b7fd97-5e5d-4264-a8df-7395ce4dde2c"
      }
      agent {
    // this image provides everything needed to run Locust
    docker {
     image 'locustio/locust'
     args '-it --entrypoint='
    }
  }
      steps {
        // there a few default environment variables on Jenkins
        // on local Jenkins machine (assuming port 8080) see
        // http://localhost:8080/pipeline-syntax/globals#env
        echo "Running Locust load tests with build ${env.BUILD_ID} on ${env.JENKINS_URL}"

        sh 'locust -f locustfile.py --headless --users 1 --spawn-rate 1 -t 20s -H https://id.wikipedia.org'

      }
    }

    // this stage runs end-to-end tests, and each agent uses the workspace
    // from the previous stage
    stage('cypress parallel tests') {
      
      environment {
        // we will be recording test results and video on Cypress dashboard
        // to record we need to set an environment variable
        // we can load the record key variable from credentials store
        // see https://jenkins.io/doc/book/using/using-credentials/
        CYPRESS_API_URL="http://sorry-cypress_director_1:1234/"
        // because parallel steps share the workspace they might race to delete
        // screenshots and videos folders. Tell Cypress not to delete these folders
        CYPRESS_trashAssetsBeforeRuns = 'false'
      }

      // https://jenkins.io/doc/book/pipeline/syntax/#parallel
      parallel {
        // start several test jobs in parallel, and they all
        // will use Cypress Dashboard to load balance any found spec files
        stage('tester A') {
          agent {
    // this image provides everything needed to run Sorry Cypress
    docker {
     //image 'cypress/base:10'
     image 'sorry-cypress/included:9.1.1'
     args '-it --net external-network --entrypoint='
    }
  }
          steps {
            echo "Running sorry-cypress parallel tests with build ${env.BUILD_ID} on ${env.JENKINS_URL}"
            //sh "npm run e2e:record:parallel"
            sh "cy2 run --record --key XXX --parallel --ci-build-id ${env.BUILD_ID}"
            //sh "cy2 run --record --key XXX --parallel --ci-build-id  ${env.BUILD_ID}"
          }
        }

        // second tester runs the same command
        stage('tester B') {
          agent {
    // this image provides everything needed to run Sorry Cypress
    docker {
     //image 'cypress/base:10'
     image 'sorry-cypress/included:9.1.1'
     args '-it --net external-network --entrypoint='
    }
  }
          steps {
            echo "Running sorry-cypress parallel tests with build ${env.BUILD_ID} on ${env.JENKINS_URL}"
            //sh "npm run e2e:record:parallel"
            //sh "cy2 run --record --key XXX --parallel --ci-build-id  ${env.BUILD_ID}"
            sh "cy2 run --record --key XXX --parallel --ci-build-id ${env.BUILD_ID}"
          }
        }

        // third tester runs the same command
        stage('tester C') {
          agent {
    // this image provides everything needed to run Sorry Cypress
    docker {
     //image 'cypress/base:10'
     image 'sorry-cypress/included:9.1.1'
     args '-it --net external-network --entrypoint='
    }
  }
          steps {
            echo "Running sorry-cypress parallel tests with build ${env.BUILD_ID} on ${env.JENKINS_URL}"
            //sh "npm run e2e:record:parallel"
            //sh "cy2 run --record --key XXX --parallel --ci-build-id  ${env.BUILD_ID}"
            sh "cy2 run --record --key XXX --parallel --ci-build-id ${env.BUILD_ID}"
          }
        }
      }

    }
  }

  post {
    // shutdown the server running in the background
    always {
      echo 'Stopping local server'
      //sh 'pkill -f http-server'
    }
  }
}
