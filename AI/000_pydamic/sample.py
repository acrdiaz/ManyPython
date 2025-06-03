# my first example of using pydantic_ai
#
#---
# create a virtual environment python
#   python -m venv myenv
# activate the virtual environment python
#   myenv\Scripts\activate
# install the module
#   pip install pydantic-ai
#---
# create requirements.txt
#   pip freeze > requirements.txt
# install the requirements
#   pip install -r requirements.txt
# run the script in windows python
#   set GEMINI_API_KEY=your_api_key
#   echo %GEMINI_API_KEY%
#   python sample.py
# deactivate the virtual environment
#   deactivate

# create a virtual environment uv
#   uv venv --python 3.13.1
# activate the virtual environment uv
#   .venv\Scripts\activate
# initialize, install the module
#   uv init .
#   uv add pydantic-ai
# create requirements.txt
#   uv export -o requirements.txt
# install the requirements
#   uv pip install -r requirements.txt
# run the script in windows uv
#   set GEMINI_API_KEY=your_api_key
#   echo %GEMINI_API_KEY%
#   uv run sample.py
#   python sample.py
# deactivate the virtual environment
#   deactivate

# remove the virtual environment in windows/mac/linux
#   rmdir /s myenv
#   rm -rf myenv
#   rm -rf myenv
# remove the requirements in windows/mac/linux
#   del requirements.txt
#   rm requirements.txt
#   rm requirements.txt

# Notes
#   [notice] A new release of pip is available: 24.3.1 -> 25.0.1
#   [notice] To update, run: python.exe -m pip install --upgrade pip

# program output
#  "Hello, World!" originated as an example program in Brian Kernighan's 1972 Bell Laboratories internal memorandum, "Programming in C: A Tutorial."


from pydantic_ai import Agent

agent = Agent (
    'google-gla:gemini-2.0-flash',
    system_prompt='Be concise, reply with one sentence.',
)

result = agent.run_sync ('What is todays date?')  
print (result.data)
