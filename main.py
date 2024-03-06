import ollama

model = 'dolphin-mixtral:latest'
template = """
Olivia: {question}
Alex: """

system = "About Alex: "
chat_history = ""
#with open("system.txt", "r") as file:
#    system += file.read()

def gen_system_prompt(question):
    global system
    prompt_prompter = """Write detailed lore for a character named Alex, a professor at MIT who was just been asked the following question: "{question}"

Do not answer the question, rather write a background story and upbringing that led to Alex being an expert in the field that said question involves."""
    response = ollama.generate(
        model=model,
        raw=False, # standard question
        prompt=prompt_prompter.format(question=question)
    )
    system += response['response']
    system += "\n\nYou are Alex, having a conversation with Olivia, a colleague.\n"
    
    

def gen_next(question):
    global chat_history
    chat_history += template.format(question=question)
    response = ollama.generate(
        model=model,
        raw=False,
        system=system,
        prompt=chat_history,
        options={
            'temperature': 3, 
            # system prompt is long enough that a very high temperature is tolerable
            # without the long prompt this temperature quickly devolves into complete gibberish.
            'stop': ['<EOT>', 'Alex:', 'Olivia:', '\n\n'],
        }
    )
    chat_history += response['response']
    # print("-------\n" + chat + "\n-----------") # debug
    return response['response']

def main():
    while (True):
        # input
        question = input("You/Olivia ('exit' to leave): ")
        if (question == 'exit'):
            break
        gen_system_prompt(question)
        response = gen_next(question)
        print(f"Bot/Alex: {response}")
    
    print("Bot/Alex: Goodbye!") # give it a little character

if __name__ == "__main__":
    main()