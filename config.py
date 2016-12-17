# Constants (User configurable)

FULL_NAME_AND_EMAIL = 'Norman Ponte <nponte@domain.com>'  # For Dockerfile/POV-Ray builds.
APP_NAME = 'HalideWorker'  # Used to generate derivative names unique to the application.

DOCKERHUB_USER = 'nponte'
DOCKERHUB_EMAIL = 'normanponte@gmail.com'
DOCKERHUB_REPO = 'private'
DOCKERHUB_TAG = DOCKERHUB_USER + '/' + DOCKERHUB_REPO + ':' + APP_NAME

AWS_REGION = 'us-east-1'
AWS_PROFILE = 'default'  # The same profile used by your AWS CLI installation

SSH_KEY_NAME = '769-ec2-key-pair.pem'  # Expected to be in ~/.ssh
ECS_CLUSTER = 'arn:aws:ecs:us-east-1:447155461961:cluster/my-ecs-cluster'

PATH_TO_ZIP_DIR='/Users/nponte/Desktop/testeer/PhotoBlur'
BUCKET_NAME='nponte-halide-run'

NAME_OUTPUT='brighter.png'
OUTPUT_EXT='.png'
CODE='g++\ image.cpp\ -g\ -I\ \/root\/halide_master\/include\ -I\ \/root\/halide_master\/tools\ -L\ \/root\/halide_master\/bin\ -lHalide\ -I\/usr\/include\/libpng12\ -lpng12\ -o\ bright\ -std=c++11\ ;\ LD_LIBRARY_PATH=\/root\/halide_master\/bin\ .\/bright'
