import asyncio
import typing
import openai


class GPTApiRequest:
    """asks the chosen question to gpt, with the code, and returns the answer"""
    def __init__(self, TOKEN: str) -> None:
        self.__TOKEN: str = TOKEN
        self.__url: str = "https://api.openai.com/v1/engines/davinci-codex/completions"
        self.__response = []

    def __request(self, question: str) -> str:
        try:
            openai.api_key = self.__TOKEN
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-instruct-0914",
                temperature=0.2,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            return response
        except Exception as e:
            return f"Fail to connect: {e}"

    def ask(self, question: str) -> str:
        return self.__request(question)


if __name__ == '__main__':
    gpt = GPTApiRequest("TOKEN")
    print(gpt.ask("what your name?"))
