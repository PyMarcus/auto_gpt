# auto_gpt
Simple project to ask questions to gpt. Basically, it makes asynchronous requests to github repositories

### How does it work?

Basically, it will read the csv file that contains the https paths to the codes, on github. Once this is done, asynchronous requests will be made, with the user's CPU color number for these links, in order to download them, to the _downloaded_ folder.

As a result, a question will be added before each code and sent to the gpt chat, via API query - you will need to use an access token, available at: https://platform.openai.com/account/api- keys.
Finally, a .csv file will be created and can be opened as a spreadsheet to consult the results (respostas_do_gpt.csv).


### How to run:

    pip install -r requirements.txt

    python3 main.py


### observation:

A version of Python that supports asynchronous modules is required.
Tests performed with python3.11, but compatible with python 3.8 +
