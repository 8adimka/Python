import datetime
import json
from pathlib import Path

def foo(**kwargs):
    return {v: k for k, v in kwargs.items()}
 
foo(a=1, b=2)

if __name__ == "__main__":
    print(foo(a=1, b=2))
