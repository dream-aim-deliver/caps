"""
Simple example of how mypy.api works
"""

import sys
from mypy import api

result = api.run(sys.argv[1:])

if result[0]:
    print("\nType checking report:\n")
    print(result[0])  # stdout

if result[1]:
    print("\nError report:\n")
    print(result[1])  # stderr

print("\nExit status:", result[2])
