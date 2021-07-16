from django.shortcuts import render


def home(request):

    # get user input from request
    input = request.GET.get("input")
    output = ""

    if input == "quit":
        output = "Goodbye, You Just Quited"

    context = {"input": input, "output": output}
    return render(request, "index.html", context)
