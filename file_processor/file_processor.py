import logging
import os
import csv
import re
from network import GPTApiRequest
from transformers import BertTokenizer



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

    def count_tokens(self, question: str) -> int:
        """
        Verifica a quantidade de tokens na pergunta, na versão free, são cerca de 4k tokens.+-
        """
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(question)))
        num_tokens = len(tokens)
        return num_tokens

    def process_files(self, total_lines: int) -> None:
        """total_lines = quantidade de linhas a serem preenchidas na planilha"""
        if not os.path.exists(self.directory):
            self.__log_error(f"Directory '{self.directory}' does not exist.")
            return
        for index, filename in enumerate(os.listdir(self.directory)):
            if filename.endswith(".java"):
                file_path = os.path.join(self.directory, filename)
                file_split = file_path.split("_")
                id_base = file_split[5]
                smell = file_split[6]
                url = "https://" + '/'.join(file_split[7:])
                question = self.phrase + self.read_file_content(file_path)
                if self.count_tokens(question) > 4000:
                    continue
                gpt_response = self.__gpt.ask(question).replace(',', ' ')
                gpt_response_parser = self.__gpt_response_parser(gpt_response)
                self.data.append({
                    "Index": str(index),
                    "Index da base":id_base,
                    "Codigo": url,
                    "Badsmell da base": smell,
                    "Pergunta":  question.strip().replace(',', '').replace('"""', '').replace('//', '').replace('\n', '').replace(';', '').replace('\t', ''),
                    "Resposta do Chat GPT": gpt_response.strip().replace('"""', '').replace('//', '').replace('\n', '').replace(';', '').replace('\t', ''),
                    "Identificou algum badsmell?": "Sim" if "yes" in gpt_response.lower() else "Nao",
                    "Badsmells identificados pelo GPT": gpt_response_parser.replace('"""', '').replace('//', '').replace('\n', '').replace(';', '').replace('\t', ''),
                })
                #pprint(self.data)
            if index == total_lines:
                break

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

    def __gpt_response_parser(self, response: str) -> str:
        """
        Esse parse é um pouco limitado, se o gpt atender às especificações, então, funciona corretamente.
        """
        pattern = r'\b([\w\s]+):'
        corresp = re.findall(pattern, response)
        return ','.join(corresp[1:])

    def save_to_csv(self, output_file):
        for item in self.data:
            item['Pergunta'] = item['Pergunta'].replace('\n', ' ')
            item['Resposta do Chat GPT'] = item['Resposta do Chat GPT'].replace('\n', ' ')
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Index', "Index da base", 'Codigo', 'Badsmell da base', 'Pergunta', 'Resposta do Chat GPT',
                          "Identificou algum badsmell?", "Badsmells identificados pelo GPT"]
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

    processor = FileProcessor("", directory_path, start_phrase)
    processor.process_files()
    processor.save_to_csv(output_csv_file)
