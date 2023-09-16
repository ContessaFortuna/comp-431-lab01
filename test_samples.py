import os


TESTS_FOLDER = "./tests"
num_tests = 0

if not os.path.exists(TESTS_FOLDER):
    os.mkdir(TESTS_FOLDER)


# 1) Test the basic implementation parameters (successful, file not found, not implemented, multiple input) 

with open(TESTS_FOLDER + "/in1.txt", "w") as f:
    f.write(
        "GET /index.html HTTP/1.0\r\n"
        "GET /index2.html HTTP/1.0\r\n"
        "GET /cat.png HTTP/1.0\r\n"
    )

with open(TESTS_FOLDER + "/out1.txt", "w") as f:
    f.write(
        "GET /index.html HTTP/1.0\r\n"
        "Method = GET\n"
        "Request-URL = /index.html\n"
        "HTTP-Version = HTTP/1.0\n"
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<body>\n"
        "<h1>COMP431</h1>\n"
        "</body>\n"
        "</html>\n"
        "GET /index2.html HTTP/1.0\r\n"
        "Method = GET\n"
        "Request-URL = /index2.html\n"
        "HTTP-Version = HTTP/1.0\n"
        "404 Not Found: /index2.html\n"
        "GET /cat.png HTTP/1.0\r\n"
        "Method = GET\n"
        "Request-URL = /cat.png\n"
        "HTTP-Version = HTTP/1.0\n"
        "501 Not Implemented: /cat.png\n"
    )
num_tests += 1

# 2) Test invalid method call
with open(TESTS_FOLDER + "/in2.txt", "w") as f:
    f.write(
        "get index.html HTTP/1.0\r\n"
    )

with open(TESTS_FOLDER + "/out2.txt", "w") as f:
    f.write(
        "get index.html HTTP/1.0\r\n"
        "ERROR -- Invalid Method token.\n"
    )
num_tests += 1

# 3) Test io error issue
with open(TESTS_FOLDER + "/in3.txt", "w") as f:
    f.write(
        "GET /index©.html HTTP/1.0\r\n"
    )

with open(TESTS_FOLDER + "/out3.txt", "w") as f:
    f.write(
        "GET /index©.html HTTP/1.0\r\n"
        "ERROR -- Invalid Absolute-Path token.\n"
    )
num_tests += 1

# 4) Test invalid HTTP version
with open(TESTS_FOLDER + "/in4.txt", "w") as f:
    f.write("GET /index.html HTTP/a.0\r\n")

with open(TESTS_FOLDER + "/out4.txt", "w") as f:
    f.write(
        "GET /index.html HTTP/a.0\r\n"
        "ERROR -- Invalid HTTP-Version token.\n"
    )
num_tests += 1

# 5) Test spurious characters before CRLF
with open(TESTS_FOLDER + "/in5.txt", "w") as f:
    f.write(
        "GET /index.html HTTP/1.0 X\r\n"
    )


with open(TESTS_FOLDER + "/out5.txt", "w") as f:
    f.write(
        "GET /index.html HTTP/1.0 X\r\n"
        "ERROR -- Spurious token before CRLF.\n"
    )
num_tests += 1


# 6) Test file retrieval within folder and txt extension
with open(TESTS_FOLDER + "/in6.txt", "w") as f:
    f.write(
        "GET /files/hello.txt HTTP/1.0 \r\n"
    )


with open(TESTS_FOLDER + "/out6.txt", "w") as f:
    f.write(
        "GET /files/hello.txt HTTP/1.0 \r\n"
        "Method = GET\n"
        "Request-URL = /files/hello.txt\n"
        "HTTP-Version = HTTP/1.0\n"
        "Hello from COMP 431\n"
    )
num_tests += 1
