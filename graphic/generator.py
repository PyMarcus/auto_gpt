import os
import typing
from pprint import pprint

import pandas as pd


def excel_to_csv(path: str) -> None:
    for file in os.listdir(path):
        if file.endswith(".xlsx"):
            data = pd.read_excel(os.path.join(path, file))
            data.to_csv(f'{os.path.join(path, file)}.csv', index=False, encoding='utf-8')
    concat_csv(path)


def parser(path: str) -> typing.Tuple:
    titles = ['Index', 'Index da base', 'Codigo', 'Badsmell da base',
              'Pergunta', 'Resposta do Chat GPT', 'Identificou algum badsmell?',
              'Badsmells identificados pelo GPT']
    csv_data = pd.read_csv("result.csv")
    csv_dict = csv_data.to_dict()
    index = csv_dict["Index"]
    index_base = csv_dict["Index da base"]
    yes_or_no = csv_dict["Identificou algum badsmell?"]
    bad_smells = csv_dict["Badsmells identificados pelo GPT"]
    bad_smells_base = csv_dict["Badsmell da base"]
    return statistics(index, index_base, yes_or_no, bad_smells_base, bad_smells)


def statistics(index: typing.Dict,
               index_base: typing.Dict,
               yes_or_no: typing.Dict,
               bad_smells_base: typing.Dict,
               bad_smells: typing.Dict) -> typing.Tuple:
    yes: int = 0
    no: int = 0
    yes_without_ans: int = 0
    index_base_arr: typing.List = []
    max_code_smell_base: typing.Dict[str, int] = {}
    gpt_bad_smells: typing.Dict[str, str] = {}
    for k, v in yes_or_no.items():
        if v == "Sim":
            yes += 1
        else:
            no += 1
    for yes_without_answer in zip(yes_or_no.values(), bad_smells.values(), index_base.values()):
        if yes_without_answer[0] == "Sim" and isinstance(yes_without_answer[1], float):
            yes_without_ans += 1
            index_base_arr.append(yes_without_answer[2])
    for max_bad_smell_base in bad_smells_base.values():
        max_code_smell_base.setdefault(max_bad_smell_base, 0)
    for k, v in bad_smells_base.items():
        max_code_smell_base[v] += 1
    for k, v in bad_smells.items():
        if not isinstance(v, float):
            [gpt_bad_smells.setdefault(key, 0) for key in v.split(",")]
    for k, v in bad_smells.items():
        if not isinstance(v, float):
            for key in v.split(","):
                gpt_bad_smells[key] += 1

    return yes, no, yes_without_ans, index_base_arr, max_code_smell_base, gpt_bad_smells


def concat_csv(directory: str) -> None:
    dataframes = []
    for file in os.listdir(directory):
        if file.endswith(".csv") and file != "result":
            path = os.path.join(directory, file)
            dataframe = pd.read_csv(path)
            dataframes.append(dataframe)
    result = pd.concat(dataframes, ignore_index=True)
    result.to_csv('result.csv', index=False, encoding='utf-8')


def run(path: str) -> typing.Tuple:
    # excel_to_csv(path)
    return parser(path)


if __name__ == '__main__':
    from collections import OrderedDict
    yes, no, yes_without_ans, index_base_arr, max_code_smell_base, gpt_bad_smells = run("gpt_data")
    print(f"IDENTIFICOU {yes} / NÃO IDENTIFICOU {no} -> {(yes / (yes + no) * 100):.2f} % DE IDENTIFICAÇÃO")
    print(f"IDENTIFICOU, MAS NÃO RESPEITOU O PARSE SOLICITADO: {yes_without_ans} VEZES , EQUIVALENTE A {((yes_without_ans/ yes) * 100):.2f}% DAS PERGUNTAS COM SIM")
    pprint(f"QUANTIDADE DE CODE SMELLS NA BASE {max_code_smell_base}")
    ordered_dict = OrderedDict(sorted(gpt_bad_smells.items(), key=lambda x: x[1], reverse=True))
    pprint(f"BADSMELLS IDENTIFICADOS PELO GPT {ordered_dict}")



