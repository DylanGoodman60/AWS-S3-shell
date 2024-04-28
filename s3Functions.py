# Dylan Goodman 1102172 goodmand@uoguelph.ca
# list_buckets bucket_list and initialize_aws 

import boto3
import configparser
import os

# copies a local file to a Cloud (S3) location
def locs3cp ( s3, local_file=None, s3_path=None) :
    try:
        # must fill in params
        if local_file is None or s3_path is None:
            raise Exception
        
        # must be a string and start with /
        if (isinstance(local_file, str) == False) or (s3_path[0] != '/'):
            raise Exception

        # separate bucket from path
        bucket, pathname = s3_path.split('/', 2)[1], s3_path.split('/', 2)[2]
        result = s3.upload_file(os.path.basename(local_file), bucket, pathname)
    except:
        print("Copy was unsuccessful. Ensure the bucket and")
        print("local file exist and that the path is correct")
        print("Ex:")
        print("    locs3cp catpictures/mycat.jpg /cis4010b01/mycat.jpg")
        return 1
    return 0

# creates a bucket in the user's S3 space following naming conventions
def create_bucket ( s3, bname=None) :
    try:
        # must be a non empty string that starts with /
        if (isinstance(bname, str) == False) or (len(bname) < 2) or (bname[0] != '/'):
            raise Exception

        s3.create_bucket(Bucket=bname[1::], CreateBucketConfiguration={'LocationConstraint': 'ca-central-1'})
    except:
        print("Cannot create bucket")
        print("It is possible this bucket name already exists")
        print("Please follow proper naming conventions. Ex:")
        print("    create_bucket /<myfirstbucket>")
        return 1
    return 0

def get_all_resources (s3) :
    resources = []
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        # List objects in the bucket
        objects = s3.list_objects_v2(Bucket=bucket['Name'])

        # add objects to resources
        for obj in objects.get('Contents', []):
            resources.append("/" + bucket['Name'] + "/" + obj['Key'])
        
        # add empty buckets
        if ("/" + bucket['Name']) not in resources:
            resources.append("/" + bucket['Name'])

    # reverse order sort to make it easier to filter out redundant entries
    return sorted(resources, key=lambda x: len(x), reverse=True)

# does an array contain an element that is a prefix of a given string
def contains_prefix(prefix, arr):
    for a in arr:
        if prefix in a:
            return True
    return False    

def get_list ( s3, list_path) :
    resources = get_all_resources(s3)
    printed = []

    # remove following '/' if they added it
    if len(list_path) != 1:
        if list_path[-1] == '/':
            list_path = list_path[:-1]

    for res in resources:

        # verify each path if it isn't root case
        if list_path == "/" or verify_s3_path(res, list_path):
            
            # check for redundant prints
            if not contains_prefix(res, printed):
                printed.append(res)

    # empty directory should print nothing
    if len(printed) == 1 and printed[0] == list_path:
        return 0

    for p in sorted(printed):
        if list_path != "/":

            # splice non-useful parts of string
            p = p[len(list_path)+1:]
        print(p)

    # if nothing was printed
    if len(printed) == 0:
        print("This S3 location was invalid or empty")
        print("please try a different path. Ex:")
        print("    list /my-awesome-bucket")
        return 1
    return 0

def verify_s3_path(res, list_path):
    if res == list_path:
        return True

    # is given path a prefix of a resource?
    if (res[:len(list_path)] == list_path):

        # is given path complete and has a forward slash following?
        if len(res) >= len(list_path) + 1 and res[len(list_path)] == '/':
            return True
    
    return False        


def initialize_aws () :

    #  Find AWS access key id and secret access key information
    #  from configuration file
    config = configparser.ConfigParser()
    config.read("S5-S3.conf")
    aws_access_key_id = config['default']['aws_access_key_id']
    aws_secret_access_key = config['default']['aws_secret_access_key']

    #  Establish an AWS session
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    #  Set up client and resources
    s3 = session.client('s3')
    s3_res = session.resource('s3')

    return s3, s3_res
