import os 
import sys 
import pathlib
import boto3
import s3Functions as s3f

cur_dir = "/"

def cwlocn () :
    print(cur_dir)
    return 0

def chlocn (s3, new_path) :

    # edge case 1
    if new_path == '.':
        return 0

    # edge case 2
    if (new_path == '..' or new_path == '../') and cur_dir != "/":
        new_path = cur_dir.rsplit('/', 1)[0]

    # edge case 3
    if new_path == '../..' or new_path == '../../':
        new_path = cur_dir.rsplit('/', 1)[0]
        new_path = new_path.rsplit('/', 1)[0]

    # if empty go to '/'
    if len(new_path) < 1:
        new_path = '/'

    # edge case 4
    if new_path == '/':
        globals()["cur_dir"] = new_path
        return 0

    # remove following '/'
    if new_path[-1] == '/':
        new_path = new_path[:-1]


    # change relative path to absolute
    if new_path[0] != '/' and new_path[0] != '.':
        if cur_dir == '/':
            new_path = cur_dir + new_path
        else:
            new_path = cur_dir + '/' + new_path

    
    resources = s3f.get_all_resources(s3)
    for res in resources:
        if s3f.verify_s3_path(res, new_path):
            globals()["cur_dir"] = new_path
            return 0
    
    # relative path given
    print("Cannot change folder, to invalid path.")
    print("Please try again. Ex:")
    print("    chlocn ../ or chlocn /my-awesome-bucket")
    return 1

def main():
    
    # connect to aws
    try:
        s3, s3_res = s3f.initialize_aws()
        print("Welcome to the AWS S3 Storage Shell (S5)")
        print("You are now connected to your S3 storage")
    except:
        print("Welcome to the AWS S3 Storage Shell (S5)")
        print("You could not be connected to your S3 storage")
        print("Please review procedures for authenticating your account on AWS S3")

    exit_commands = {"exit", "quit"}

    # dictionary mapping function names to pointers
    extra_functions = {
        "create_bucket": s3f.create_bucket,
        "locs3cp": s3f.locs3cp
    }

    # S5 shell loop
    abort_shell = False
    while (not abort_shell) :
        print("S5> ", end="")
        word_string = input()
        word_arr = word_string.split(' ')

        # exit or quit - must match exactly
        if word_string in exit_commands:
            abort_shell = True

        # cloud functions
        elif word_arr[0] in extra_functions:
            ret = extra_functions[word_arr[0]](s3, *word_arr[1::])

        # directory functions
        elif word_arr[0] == "cwlocn":
            cwlocn()

        elif word_arr[0] == "chlocn":
            
            # use '/' if nothing given
            cd_path = "/"
            if len(word_arr) > 1:
                cd_path = word_arr[1]    
            
            chlocn(s3, cd_path)

        elif word_arr[0] == "list":

            # use current directory if nothing given
            list_path = cur_dir
            if len(word_arr) > 1 and len(word_arr[1]) > 0:
                list_path = word_arr[1]

            s3f.get_list(s3, list_path)

        # pass command to normal shell
        else:
            os.system(word_string)

    print("Exiting S5... goodbye")

if __name__ == "__main__":
    main()
