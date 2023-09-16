import difflib
import json
import os
import sys
import subprocess
import filecmp
import pprint

from test_samples import num_tests, TESTS_FOLDER
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
path_to_file = 'HTTPServer.py'

for test in range(1, num_tests + 1):
	print(test)
	#os.system('rm -rf /autograder/submission/retr_files && mkdir /autograder/submission/retr_files')
	# TODO: check that this can detect CRLF errors at end of line
	with open(TESTS_FOLDER + '/out' + str(test) +'.txt', newline='\r\n') as fp:
		expected = fp.read().splitlines()
		print(BLUE, end="")
		print(expected, end="")
		print(NC)

	with open(TESTS_FOLDER + '/in' + str(test) +'.txt') as infile:
		kiddo = subprocess.run(['python3', path_to_file],
							   universal_newlines=True, stdin=infile, stdout=subprocess.PIPE, timeout=5)
		diff = list(difflib.unified_diff(kiddo.stdout.splitlines(), expected))
		print(kiddo.stdout.splitlines())
		print("---------------------------------\n")
		print("Diff Result:")
		if diff==[]:
			print(GREEN, end="")
		else:
			print(RED, end="")
		print(diff)
		print(NC)
		print("---------------------------------")
		print("---------------------------------\n")



