import os
from pathlib import Path

# scenario a
name = "John"
prompt = f"Hi, {name} how are you?"
print(prompt)

# scenario b
cwd = os.getcwd()
if '002_string_interpolation' not in cwd:
    os.chdir(Path(cwd).joinpath('learn\\002_string_interpolation'))

file_path = "content.txt"
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        prompt = file.read()
else:
    raise FileNotFoundError(f"The file '{file_path}' does not exist.")

programming_language = "Python"
summary_prompt = prompt.format(name=name, language=programming_language)
print(summary_prompt)