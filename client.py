import aiohttp
from asyncio import run


async def main():

    async with aiohttp.ClientSession() as session:

        """ POST """
        # response = await session.post('http://127.0.0.1:8080/adverts/',
        #                               json={'header': 'header_2',
        #                                     'description': 'description_1',
        #                                     'owner': 'owner_1'
        #                                     })
        # print(await response.json())

        """ GET """

        response = await session.get("http://127.0.0.1:8080/adverts/2")
        print(await response.json())

        """ DELETE """
        # response = await session.delete("http://127.0.0.1:8080/adverts/1")
        # print(await response.json())

        """ PATCH """
        # response = await session.patch('http://127.0.0.1:8080/adverts/2',
        #                               json={'header': 'header_FIXED',
        #                                     })
        # print(await response.json())


run(main())