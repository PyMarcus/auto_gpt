import re
def a(response):
    word = ""
    for i, w in enumerate(response.split(".")):
        if "-" in w:
            if word != "":
                word += ', ' + w.split("-")[1]
            else:
                print(w.split('-'))

                word += w.split("-")[1]
    return word

print(a("Code smells: - Long method- Indirect access to variable - jos - dsa"))