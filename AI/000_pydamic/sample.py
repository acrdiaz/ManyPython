# my first example of using pydantic_ai
#
# create a virtual environment
#   python -m venv myenv
# activate the virtual environment
#   myenv\Scripts\activate
# install the module
#   pip install pydantic-ai
# create requirements.txt
#   pip freeze > requirements.txt
# install the requirements
#   pip install -r requirements.txt
# run the script in windows
#   set GEMINI_API_KEY=your_api_key
#   echo %GEMINI_API_KEY%
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

result = agent.run_sync ('Where does "hello world" come from?')  
print (result.data)
