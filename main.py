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

prompt_prompter = """Write a biography for a character named Alex, an OPINIONED professor at MIT who was just been asked the following question: "{question}"

Do NOT answer the question, and do NOT refer to the question; rather, write a background story and upbringing that led to Alex being an expert in the field that said question involves."""

sys_decohere = """You are DECOHERE, an AI designed to decohere and disguise AI generated content such that it passes as human. 
You are to respond to the input with its modification. Do NOT answer questions or modify meanings. Do NOT present yourself in your answer."""

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
    system = "".join(decohere(system))
    system += "\n\n-- The following is a conversation between Alex and Olivia, a colleague and close friend of Alex who have known each other since high school. --\n\n"

def decohere(prompt):
    stream = ollama.generate(
        model=model,
        raw=False, # standard question
        stream=True,
        system=sys_decohere,
        prompt=prompt,
        options={
            'temperature': 2 # ramp up
        }
    )
    for chunk in stream:
        yield chunk['response']

def gen_next(question):
    global chat_history
    chat_history += template.format(question=question)
    stream = ollama.generate(
        model=model,
        raw=True, # using the model template binds it to being more robotic
        stream=True,
        #system=system,
        prompt=system+chat_history,
        options={
            'temperature': 3, 
            # system prompt is long enough that a very high temperature is tolerable.
            # without the long prompt this temperature quickly devolves into complete gibberish.
            'repeat_penalty': 1.2,
            'stop': ['<EOT>', 'Alex:', 'Olivia:', '\n\n\n']
        }
    )
    for chunk in stream:
        chat_history += chunk['response']
        yield chunk['response']

def main():
    prompt_generated = False
    while (True):
        # input
        question = input(c("You/Olivia ('/prompt' for the generated system prompt, '/exit' to leave): ", "green"))

        #commands
        if (question == '/exit'):
            break
        elif (question == "/prompt"):
            print(c("System prompt: ", "yellow") + system)
            continue
        elif (question.startswith("/")):
            print(c("Unknown command", "red"))
            continue

        if not prompt_generated:
            print(c("Generating system prompt...", "yellow"))
            gen_system_prompt(question)
            prompt_generated = True

        res = ""
        # print(c("Generating first stage...", "yellow"))
        for r in gen_next(question):
            res += r

        print(c("Bot/Alex: ", "light_blue"), end="")
        for r in decohere(res):
            print(r, end="")
        print() #newline
    
    print(c("Bot/Alex: ", "light_blue") + "Goodbye!") # give it a little character

if __name__ == "__main__":
    print(c("Using " + model + ". You can change the model with --model [model]", "red"))
    main()