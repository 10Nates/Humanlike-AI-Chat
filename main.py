import ollama

model = 'dolphin-mixtral:latest'
template = """
Alex: {question}
Olivia: """

chat = ""
with open("system.txt", "r") as file:
    chat += file.read()

def gen_next(question):
    global chat
    chat += template.format(question=question)
    response = ollama.generate(
        model='dolphin-mixtral:latest',
        raw=True,
        prompt=chat,
        options={
            'stop': ['<EOT>', 'Alex:', 'Olivia:', '\n\n'],
        }
    )
    chat += response['response']
    # print("-------\n" + chat + "\n-----------") # debug
    return response['response']

def main():
    while (True):
        # input
        question = input("You/Alex ('exit' to leave): ")
        if (question == 'exit'):
            break
        response = gen_next(question)
        print(f"Bot/Olivia: {response}")
    
    print("Bot/Olivia: Goodbye!") # give it a little character

if __name__ == "__main__":
    main()