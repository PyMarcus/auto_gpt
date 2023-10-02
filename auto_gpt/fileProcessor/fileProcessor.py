import logging
import os
import csv
import random

class FileProcessor:
    """
        File Processor class and respond by creating
        the csv file containing information about the
        downloaded codes.
    """
    def __init__(self, directory, phrase):
        self.directory = directory
        self.phrase = phrase
        self.data = []

    def process_files(self):
        if not os.path.exists(self.directory):
            self.__log_error(f"Directory '{self.directory}' does not exist.")
            return

        for filename in os.listdir(self.directory):
            if filename.endswith(".java"):
                file_path = os.path.join(self.directory, filename)
                item_number = len(self.data) + 1
                code_name = filename
                question = self.phrase + self.read_file_content(file_path).replace('\n', ' ')
                response = self.generate_random_response()

                self.data.append({
                    "Nº": item_number,
                    "Código": code_name,
                    "Pergunta": question,
                    "Qual resposta do Chat GPT": response
                })

    def read_file_content(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            self.__log_error(f"File '{file_path}' not found.")
            return ""
        except Exception as e:
            self.__log_error(f"An error occurred while reading '{file_path}': {str(e)}")
            return ""

    def generate_random_response(self):
        # Generate a random response, you can modify this function as needed
        responses = ["Response 1", "Response 2", "Response 3"]
        return random.choice(responses)

    def save_to_csv(self, output_file):
        try:
            with open(output_file, 'w', newline='') as csvfile:
                fieldnames = ["Nº", "Código", "Pergunta", "Qual resposta do Chat GPT"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
                writer.writeheader()
                for row in self.data:
                    writer.writerow(row)
        except Exception as e:
            self.__log_error(f"An error occurred while writing to '{output_file}': {str(e)}")
    def __log_error(self, text: str) -> None:
        logging.basicConfig(filename='auto_gpt_file_processor_error.log', level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.error(text)

if __name__ == "__main__":
   
    directory_path = "../downloaded"
    output_csv_file = "../data/output.csv" 
    start_phrase = "I'm sharing some Java code and would appreciate your feedback. Given the principles of design patterns, method length, and parameter count, can you point out anypotential concerns or anti-patterns or badsmell in the code below? "

    processor = FileProcessor(directory_path, start_phrase)
    processor.process_files()
    processor.save_to_csv(output_csv_file)
