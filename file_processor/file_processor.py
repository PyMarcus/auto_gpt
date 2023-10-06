import logging
import os
import csv
import random
import sys

from network import GPTApiRequest


class FileProcessor:
    """
        File Processor class and respond by creating
        the csv file containing information about the
        downloaded codes.
    """

    def __init__(self, token, directory, phrase):
        """
         example directory = "../downloaded"
            phrase "../data/resultado_das_perguntas_ao_gpt.csv"
        """
        self.directory = directory
        self.phrase = phrase
        self.data = []
        self.__gpt = GPTApiRequest(token)

    def process_files(self):
        if not os.path.exists(self.directory):
            self.__log_error(f"Directory '{self.directory}' does not exist.")
            return
        for index, filename in enumerate(os.listdir(self.directory)):
            if filename.endswith(".java"):
                file_path = os.path.join(self.directory, filename)
                question = self.phrase + self.read_file_content(file_path)
                if len(question) < 32000: # excel tem limite de char por celula :(
                    self.data.append({
                        "Quantidade": str(index).replace('\n', ''),
                        "Codigo": file_path.replace("\\", '/').replace(',', ' ').replace('\n', '').replace('_', '/'),
                        "Pergunta":  question.replace(',', ' ').replace('"""', '').replace('//', '').replace('\n', '').replace(';', '').replace('\t', '').replace(' ', '') ,
                        "Resposta do Chat GPT": self.__gpt.ask(question).replace(',', ' ')
                    })

    def read_file_content(self, file_path):
        try:
            with open(file_path, 'r', encoding='latin1') as file:
                return file.read()
        except FileNotFoundError:
            self.__log_error(f"File '{file_path}' not found.")
            return ""
        except Exception as e:
            self.__log_error(f"An error occurred while reading '{file_path}': {str(e)}")
            return ""

    def save_to_csv(self, output_file):
        for item in self.data:
            item['Pergunta'] = item['Pergunta'].replace('\n', ' ')
            item['Resposta do Chat GPT'] = item['Resposta do Chat GPT'].replace('\n', ' ')
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Quantidade', 'Codigo', 'Pergunta', 'Resposta do Chat GPT']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)

    def __log_error(self, text: str) -> None:
        logging.basicConfig(filename='auto_gpt_file_processor_error.log', level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.error(text)


if __name__ == "__main__":
    directory_path = "../downloaded"
    output_csv_file = "../data/resultado_das_perguntas_ao_gpt.csv"
    start_phrase = "Im sharing some Java code and would appreciate your feedback." \
                   " Given the principles of design patterns, method length, and " \
                   "parameter count, can you point out anypotential concerns or " \
                   "anti-patterns or badsmell in the code below?"

    processor = FileProcessor(directory_path, start_phrase)
    processor.process_files()
    processor.save_to_csv(output_csv_file)