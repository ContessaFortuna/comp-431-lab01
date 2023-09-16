# Win Geigerman
__author__ = 730434613
import re
import sys
import os

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

def read_file(pathname):
    extension_regex = re.compile(r".*(\.txt|\.htm|\.html)$")
    if(extension_regex.fullmatch(pathname)==None):
        # 501 Not Implemented
        return "501 Not Implemented: "+pathname
    fullpath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    if(not os.path.isdir(fullpath)):
       # 404 Not Found
       return "404 Not Found: "+pathname
    try:
        file = open(fullpath,"r")
        return file.read()
    except IOError as e:
        # ERROR: <IOError message>
        return "ERROR: "+str(e)
        

def parse_request(input_command):
    sys.stdout.write(input_command)
    spl_command = split_tokens(input_command)
    chk_verify = verify_tokens(spl_command)
    if(chk_verify in range(-4,0)):
        sys.stdout.write(parse_errors[chk_verify]+"\n")
        return -1
    sys.stdout.write("Method = "+spl_command["method"]+"\n")
    sys.stdout.write("Request-URL = "+spl_command["request_url"]+"\n")
    sys.stdout.write("HTTP-Version = "+spl_command["version_identifier"]+"\n")
    sys.stdout.write(read_file(spl_command["request_url"])+"\n")

for line in sys.stdin:
    if(len(line)>1):
        parse_request(line)