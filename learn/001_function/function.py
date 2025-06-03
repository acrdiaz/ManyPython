# this is a function file

def checkName(name):
    # Check if the name is "Alice"
    if name.lower() == "alice":
        return "Hi, Alice!"
    else:
        return "Hello, stranger!"

def readName():
    print("What is your name?")
    name = input()
    return name

def main():
    name = readName()
    message = checkName(name)
    print(message)

if __name__ == "__main__":
    main()
else:
    print("function.py is imported")

# end of file