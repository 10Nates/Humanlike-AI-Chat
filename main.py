import ollama
import sys
from termcolor import colored as c

# constants
model = 'dolphin-mixtral:latest'
if "--model" in sys.argv:
    model = sys.argv[sys.argv.index("--model") + 1]
template = """
Olivia: {question}
Alex: """

# "Lore" works better. Probably tagging into DnD characters or something.
prompt_prompter = """Write detailed lore for a character named Alex, an OPINIONED professor at MIT who was just been asked the following question: "{question}"

Do not answer the question, rather write a background story and upbringing that led to Alex being an expert in the field that said question involves."""

#globals
system = ""
chat_history = ""

def gen_system_prompt(question):
    global system
    response = ollama.generate(
        model=model,
        raw=False, # standard question
        prompt=prompt_prompter.format(question=question)
    )
    system = response['response']
    system += "\n\n-- The following is a conversation between Alex and Olivia, a colleague and close friend of Alex who have known each other since high school. --\n\n"
    
def gen_next(question):
    global chat_history
    chat_history += template.format(question=question)
    response = ollama.generate(
        model=model,
        raw=True, # using the model template binds it to being more robotic
        #system=system,
        prompt=system+chat_history,
        options={
            'temperature': 3, 
            # system prompt is long enough that a very high temperature is tolerable.
            # without the long prompt this temperature quickly devolves into complete gibberish.
            'repeat_penalty': 1.2,
            'stop': ['<EOT>', 'Alex:', 'Olivia:'],
        }
    )
    chat_history += response['response']
    # print("-------\n" + chat + "\n-----------") # debug
    return response['response']

def main():
    while (True):
        # input
        question = input(c("You/Olivia ('/prompt' for last system prompt, '/exit' to leave): ", "green"))

        #commands
        if (question == '/exit'):
            break
        elif (question == "/prompt"):
            print(f"Last system prompt: {system}")
            continue
        elif (question.startswith("/")):
            print(c("Unknown command", "red"))
            continue

        gen_system_prompt(question)
        response = gen_next(question)
        print(c("Bot/Alex: ", "light_blue") + response)
    
    print(c("Bot/Alex: ", "light_blue") + "Goodbye!") # give it a little character

if __name__ == "__main__":
    print(c("Using " + model + ". You can change the model with --model [model]", "red"))
    main()