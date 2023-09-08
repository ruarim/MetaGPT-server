import fire
from startup import main

def runModel(prompt):
    fire.Fire(main(prompt))
