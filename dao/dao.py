from connection import Connection


class Dao:
    def __init__(self) -> None:
        self.__conn = Connection("../config.ini")

    async def insert_into(self, **kwargs) -> None:
        async with self.__conn.get_conn() as conn:
            await conn.execute("")
