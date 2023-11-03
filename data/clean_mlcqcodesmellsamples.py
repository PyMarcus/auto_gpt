import csv
import time

from cachetools import cached, TTLCache
import typing
from typing import Tuple, List, Any

import requests
from csv import DictReader


class CleanMLCQ:
    """
    Limpa o arquivo csv, removendo severity none
    tambem, remove links invalidos (status code 404)
    """

    cache = TTLCache(maxsize=1000, ttl=3600)

    def __init__(self, csvfile_path: str) -> None:
        self.__csvfile_path: str = csvfile_path

    def __read_csv(self) -> list[Any]:
        filtered_data = []
        with open(self.__csvfile_path, mode='r', newline='', encoding='utf-8') as csvfile:
            csv_reader = DictReader(csvfile, delimiter=';')
            for row in csv_reader:
                if row is not None:
                    new_row = self.__parser(row)
                    if new_row is not None:
                        response = self.__check_links(new_row[13])
                        if response is True:
                            print(f"saving id: {new_row[0]} from {new_row[13]}")
                            filtered_data.append(new_row[0])
        return filtered_data

    def __write_csv(self):
        data = self.__read_csv()
        with open("ids.txt", 'w') as id:
            for ids in data:
                id.writelines(ids + '\n')

    @cached(cache)
    def __check_links(self, link: str) -> bool:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                return True
            time.sleep(3)
        except:
            return False

    def __parser(self, row: typing.Dict) -> typing.Any:
        id = row['id']
        reviewer_id = row['reviewer_id']
        sample_id = row['sample_id']
        smell = row['smell']
        severity = row['severity']
        review_timestamp = row['review_timestamp']
        code_type = row['type']
        code_name = row['code_name']
        repository = row['repository']
        commit_hash = row['commit_hash']
        path = row['path']
        start_line = row['start_line']
        end_line = row['end_line']
        link = row['link']
        is_from_industry_relevant_project = row['is_from_industry_relevant_project']
        return id, reviewer_id, sample_id, smell, severity, review_timestamp, code_type, \
            code_name, repository, commit_hash, path, start_line, end_line, link, is_from_industry_relevant_project

    def run(self) -> None:
        self.__write_csv()
        print("OK")


if __name__ == '__main__':
    cmlcq: CleanMLCQ = CleanMLCQ("removidos.csv")
    cmlcq.run()
