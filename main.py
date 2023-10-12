import time
from file_processor import FileProcessor
from network import Network
from connection import Connection


if __name__ == '__main__':
    conn = Connection("config.ini")
    start = time.time()
    """
    # Executar primeiro para baixar os códigos da base para pasta downloaded
    nw = Network("data/MLCQCodeSmellSamples.csv")
    nw.start()
    # feito isso, executar o codigo abaixo:
    """
    TOKEN: str = conn.get_gpt_key() # token da open ai
    codes: str = "downloaded"  # quais codigos serao enviados ao gpt
    question: str = """I need to check if the code below contains code smells (aka bad smells). If there are any code
                     smells, list which ones are present. Please start your answer with "YES I found bad smells"
                      when you find any bad smell. Otherwise, start your answer with "NO, I did not find any bad smell".
                       When you start to answer the bad smell itself, always put in your answer "the bad smells are:"
                        amongst the text your answer.And ALWAYS separate it this way:1.Big method: explanation"""
    requests = FileProcessor(TOKEN, codes, question)
    requests.process_files(300)
    requests.save_to_csv("respostas_do_gpt.csv")
    print(f"Complete > {time.time() - start}s")