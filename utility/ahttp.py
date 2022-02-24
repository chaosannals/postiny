from aiohttp import ClientSession

async def get(url):
    '''
    
    '''

    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def post(url, data):
    '''
    
    '''

    async with ClientSession() as session:
        async with session.post(url, data) as response:
            return await response