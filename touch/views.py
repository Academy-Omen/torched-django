import random
import json

import torch

from .model import NeuralNet
from .nltk_utils import bag_of_words, tokenize

from django.shortcuts import render


def home(request):

    # get user input from request
    input = request.GET.get("input")
    output = ""

    if input == "quit":
        output = "Goodbye, You Just Quited"

    context = {"input": input, "output": output}
    return render(request, "index.html", context)
