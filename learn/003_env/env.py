# env.py

import os
import sys

print(">>>>>>>>> Hi")

print("a")
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
print(path)

print("b")
api_key = os.getenv('GEMINI_API_KEY')
print(api_key)

print(">>>>>>>>> Done.")