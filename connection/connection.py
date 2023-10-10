import typing

import asyncpg
import configparser
from contextlib import asynccontextmanager


class Connection:
    def __init__(self, ini_file_path: str) -> None:
        self.__ini_file_path = ini_file_path

    def get_gpt_key(self) -> str:
        parser = configparser.RawConfigParser()
        parser.read(self.__ini_file_path)
        return parser["gpt"].get("key")

    @asynccontextmanager
    async def get_conn(self) -> typing.Any:
        parser = configparser.RawConfigParser()
        parser.read(self.__ini_file_path)
        host = parser["database"].get("host")
        user = parser["database"].get("user")
        password = parser["database"].get("password")
        port = int(parser["database"].get("port"))
        database = parser["database"].get("database")
        try:
            pool = await asyncpg.create_pool(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
                min_size=3,
                max_size=10
            )
            async with pool.acquire() as connection:
                yield connection
        except Exception as e:
            print(f"Fail to connect into db {e}")

