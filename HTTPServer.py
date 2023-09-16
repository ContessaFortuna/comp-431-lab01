# Win Geigerman
__author__ = 730434613
import re
import sys
import os
absolute_path = os.path.dirname(os.path.abspath(__file__))

parse_errors = {
    -1: "ERROR -- Invalid Method token.",
    -2: "ERROR -- Invalid Absolute-Path token.",
    -3: "ERROR -- Invalid HTTP-Version token.",
    -4: "ERROR -- Spurious token before CRLF."
}

def split_tokens(input_command):
    split_command = input_command.split()
    while(len(split_command)<3):
        split_command+="notoken"
    thesplit = {
        "method": split_command[0],
        "request_url": split_command[1],
        "version_identifier": split_command[2]
    }
    thesplit["spurious"] = len(split_command)>3
    return thesplit
    


def verify_tokens(split_command):
    if(split_command["method"]!="GET"):
        # Invalid Method Token
        return -1
    filepath_regex = re.compile(r"\/(\d|[a-zA-Z]|\.|_|\/)*")
    if(filepath_regex.fullmatch(split_command["request_url"])==None):
        # Invalid Absolute-Path Token
        return -2
    version_regex = re.compile(r"HTTP\/\d+\.\d+")
    if(version_regex.fullmatch(split_command["version_identifier"])==None):
        # Invalid HTTP-Version Token
        return -3
    if(split_command["spurious"]):
        # Spurious token before CLRF
        return -4
    # On successful match of components
    return 1

def read_file(file_path):
    extension_regex = re.compile(r".*(\.txt|\.htm|\.html)$")
    if(extension_regex.fullmatch(file_path)==None):
        # 501 Not Implemented
        return "501 Not Implemented: "+file_path
    if(not os.path.isdir(file_path)):
       # 404 Not Found
       return "404 Not Found: "+file_path
    try:
        file = open(file_path,"r")
        return file.read()
    except IOError as e:
        # ERROR: <IOError message>
        return "ERROR: "+e
        

def parse_request(input_command):
    sys.stdout.write(input_command+"\n")
    spl_command = split_tokens(input_command)
    chk_verify = verify_tokens(spl_command)
    if(chk_verify<0):
        sys.stdout.write(parse_errors[chk_verify]+"\n")
        return -1
    sys.stdout.write("Method = "+spl_command["method"]+"\n")
    sys.stdout.write("Request-URL = "+spl_command["request_url"]+"\n")
    sys.stdout.write("HTTP-Version = "+spl_command["version_identifier"]+"\n")
    sys.stdout.write(read_file(os.path.join(absolute_path, spl_command["request_url"]))+"\n")

for line in sys.stdin:
    if(len(line)>1):
        parse_request(line)