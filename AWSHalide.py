from init import *
from config import *

def update_script():
    local('sed -i -e \'s/NAME_OUTPUT/' + NAME_OUTPUT + '/g\' ecs-worker/ecs-worker.sh')
    local('sed -i -e \'s/CODE/' + CODE + '/g\' ecs-worker/ecs-worker.sh')
    local('sed -i -e \'s/OUTPUT_EXT/' + OUTPUT_EXT + '/g\' ecs-worker/ecs-worker.sh')
    local('rm ecs-worker/ecs-worker.sh-e')

def destroy_queue():
    local('aws sqs delete-queue' +
          '    --queue-name ' + SQS_QUEUE_NAME + AWS_CLI_STANDARD_OPTIONS,capture=True)

# Initializes all the resouces necessary for use with AWS
def init():
    update_script()
    # Install required packages
    update_dependencies()
    # sets the AWS_BUCKET
    update_bucket()
    # create the queue based on the name
    update_queue()
    # create the lamba function ecs-worker-launcher/ecs-worker-launcher.js
    update_lambda()
    update_ecs()
    update_ecs_role_policy()
    show_bucket_name()

# New blank script
def destroy():
    local('cp storage/ecs-worker.sh ecs-worker/')
    destroy_queue()

# Create the zip by name
# Runs with -r option on zip
def upload_zip(zip_name):
    local('zip -j -r ' + zip_name + ' ' + PATH_TO_ZIP_DIR)
    # Copy over the zip into the bucket
    local('aws s3 cp ' + zip_name + ' s3://' + BUCKET_NAME + '/' + zip_name)
    local('rm ' + zip_name)

# List the contents of the chosen bucket
def list_bucket():
    local('aws s3 ls s3://' + BUCKET_NAME + '/')

# Download output to output_dir
def download_output(output_dir, name):
    local('aws s3 cp s3://' + BUCKET_NAME + '/' + name + OUTPUT_EXT + ' ' + output_dir)
