# AWS S3 Shell 

*This project was a part of the Cloud Computing course at the University of Guelph*

The AWS S3 Shell is intended to mimic the shell of a bash user while containing additional AWS functionality, where S3 objects can be manipulated as if they exist on your local file system. Any commands that are not recognized will be passed to the underlying shell for execution. The idea is that these kinds of tools could be parts of your shell on launch, enabling seamless interaction with cloud storage.

### Requirements

* python3
* boto3 SDK
* AWS python libraries installed
* setup S5-S3.conf in the working directory containing AWS credentials (example below)

#### S5-S3.conf example

```
[default]
aws_access_key_id = someAwsAccessKeyIdHere
aws_secret_access_key = someAwsSecretAccessKeyHere
```

### Usage

`python3 s3Shell.py`

You will be greeted with a welcome message and confirmation of the AWS connection.

### Commands 

*Note: unknown commands will be passed to the underlying shell for execution*

| Command       | Effect        |
|:------------- |:--------------|
| locs3cp       | Copies a local file to an S3 location mimicking `cp`    |
| create_bucket | Creates a bucket in the user's S3 space                 |
| chlocn        | Changes location in S3 space mimicking `cd`             |
| cwlocn        | Displays the current S3 directory mimicking `pwd`       |
| list          | Displays the contents of an S3 directory mimicking `ls` |

