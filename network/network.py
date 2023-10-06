import json
import asyncio
import typing
import aiofiles
import aiohttp
import logging
from parser import Parser
from threading import Thread
from bs4 import BeautifulSoup
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor


class Network:
    """
    Network class makes requests to the github
    repository , where the sources are located!
    """
    def __init__(self, data_path: str) -> None:
        """
        :param data_path: path to csv file with all links
        """
        self.__data_path: str = data_path
        self.__parser: Parser = Parser(data_path)
        self.__parser.run()

    def start(self) -> None:
        threads: typing.List[Thread] = []
        with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
            for link in self.__parser.get_links():
                link, smell = link.split("+")
                asyncio.run(self.__client(link, smell, executor))

    async def __client(self, link: str, smell: str, executor: ThreadPoolExecutor) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(executor, self.__fetch, link, smell)

    def __fetch(self, link: str, smell: str):
        async def get_data_from_repository():
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as response:
                    if response.status == 200:
                        try:
                            content = await response.text()
                            parse = BeautifulSoup(content, 'html.parser')  # em blob e rawlines
                            code = json.loads(parse.text)["payload"]["blob"]["rawLines"]
                            await self.__writecodes(link, "\n".join(code), smell)
                        except Exception as e:
                            self.__log_error(f"{e} {link}")
                    else:
                        try:
                            self.__log_error(f"[{response.status}]Fail to access: {link}")
                        except Exception as e:
                            ...
        asyncio.run(get_data_from_repository())

    async def __writecodes(self, name: str, content: str, smell) -> None:
        name = name.strip().replace('/', '_').replace('https:__', '').split("_#")[0]
        async with aiofiles.open(f"/downloaded/{smell}_{name}", 'w') as f:
            await f.write(content)

    def __log_error(self, text: str) -> None:
        logging.basicConfig(filename='auto_gpt_network_error.log', level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.error(text)


if __name__ == '__main__':
    network: Network = Network("../data/MLCQCodeSmellSamples.csv")
    network.start()
