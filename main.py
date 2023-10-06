import time
from file_processor import FileProcessor
from network import Network


if __name__ == '__main__':
    start = time.time()
    network: Network = Network("data/MLCQCodeSmellSamples.csv")
    print("[+]Downloading source codes from github...")
    network.start()
    TOKEN: str = ""  # token da open ai
    codes: str = "downloaded"  # quais codigos serao enviados ao gpt
    question: str = "Im sharing some Java code and would appreciate your feedback." \
                   " Given the principles of design patterns, method length, and " \
                   "parameter count, can you point out anypotential concerns or " \
                   "anti-patterns or badsmell in the code below?"
    print("[+]Asking gpt questions...")
    requests = FileProcessor(TOKEN, codes, question)
    requests.process_files()
    requests.save_to_csv("respostas_do_gpt.csv")
    print(f"Complete > {time.time() - start}s")
