import csv
import typing
import asyncio
import aiofiles
from dataclasses import dataclass


@dataclass
class Parser:
    """
    read the link base, in the csv file
    """
    def __init__(self, data_path: str) -> None:
        self.__data_path: str = data_path
        self.__links: typing.List[str] = list()

    def run(self):
        asyncio.run(self.__csv_reader())

    def get_links(self) -> typing.List[str]:
        return self.__links

    async def __csv_reader(self):
        async with aiofiles.open(self.__data_path, 'r') as csv_file:
            lines = await csv_file.readlines()
            csvreader = csv.reader(lines, delimiter=';')
            next(csvreader)
            for row in csvreader:
                # filtro apenas os que não forem none
                if row[4] != "none":
                    self.__links.append(str(row[-2]) + "+" + str(row[3]) + "+" + str(row[0]) + "+" +
                                       str(row[-4]) + "+" + str(row[-3]))
