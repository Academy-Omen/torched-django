import os
import random
import json

import torch

from .model import NeuralNet
from .nltk_utils import bag_of_words, tokenize

from django.shortcuts import render


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, "intents.json")  # full path to text.

with open(file_path, "r") as json_data:
    intents = json.load(json_data)

FILE = os.path.join(module_dir, "data.pth")  # full path to text.
print("Here", FILE)
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


def home(request):

    # get user input from request
    input = request.GET.get("input")
    print("Input:", input)
    output = "Let's chat! (type 'quit' to exit)"

    if input == "quit":
        output = "Goodbye, You Just Quited"

    # ------------------------------------------

    sentence = tokenize(input)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                output = random.choice(intent["responses"])
    else:
        output = "I'm sorry, I don't understand."

    # ------------------------------------------

    context = {"input": input, "output": output}
    return render(request, "index.html", context)
