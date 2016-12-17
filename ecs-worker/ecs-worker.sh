#!/bin/bash

#
# Uses the AWS CLI utility to fetch a message from SQS, fetch a ZIP file from S3 that was specified in the message,
# Ouput of Halide is then output to the bucket
#

region=${AWS_REGION}
queue=${SQS_QUEUE_URL}

# Fetch messages and render them until the queue is drained.
while [ /bin/true ]; do
    # Fetch the next message and extract the S3 URL to fetch the POV-Ray source ZIP from.
    echo "Fetching messages fom SQS queue: ${queue}..."
    result=$(aws sqs receive-message --queue-url ${queue} --region ${region} \
            --wait-time-seconds 20 --query Messages[0].[Body,ReceiptHandle] \
            | sed -e 's/^"\(.*\)"$/\1/')

    if [ -z "${result}" ]; then
        echo "No messages left in queue. Exiting."
        exit 0
    else
        echo "Message: ${result}."

        receipt_handle=$(echo ${result} | sed -e 's/^.*"\([^"]*\)"\s*\]$/\1/')
        echo "Receipt handle: ${receipt_handle}."

        bucket=$(echo ${result} | sed -e 's/^.*arn:aws:s3:::\([^\\]*\)\\".*$/\1/')
        echo "Bucket: ${bucket}."

        key=$(echo ${result} | sed -e 's/^.*\\"key\\":\s*\\"\([^\\]*\)\\".*$/\1/')
        echo "Key: ${key}."

        base=${key%.*}
        ext=${key##*.}

        if [ \
            -n "${result}" -a \
            -n "${receipt_handle}" -a \
            -n "${key}" -a \
            -n "${base}" -a \
            -n "${ext}" -a \
            "${ext}" = "zip" \
        ]; then
            mkdir -p work
            pushd work


            echo "Copying ${key} from S3 bucket ${bucket}..."
            aws s3 cp s3://${bucket}/${key} . --region ${region}
            echo "Unzipping ${key}..."

            unzip ${key}

            # EXECUTION
            g++ image.cpp -g -I /root/halide_master/include -I /root/halide_master/tools -L /root/halide_master/bin -lHalide -I/usr/include/libpng12 -lpng12 -o bright -std=c++11 ; LD_LIBRARY_PATH=/root/halide_master/bin ./bright

            # MINE AGAIN
            if [ -f brighter.png ]; then
                echo "Copying output to bucket"
                aws s3 cp brighter.png s3://${bucket}/${key}.png
            else
                echo "ERROR: Halide did not generate output.txt"
            fi

            echo "Cleaning up..." >> cool.txt
            popd
            /bin/rm -rf work

            echo "Deleting message..." >> cool.txt
            aws sqs delete-message \
                --queue-url ${queue} \
                --region ${region} \
                --receipt-handle "${receipt_handle}"

        else
            echo "ERROR: Could not extract S3 bucket and key from SQS message." >> cool.txt
        fi
    fi
done
