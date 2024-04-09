
from azure.cosmos.aio import CosmosClient
from azure.cosmos import exceptions
from azure.cosmos.partition_key import PartitionKey

from configs.credential import HOST, MASTER_KEY, DATABASE_ID


def get_database_client():
     # Initialize the Cosmos client
     client = CosmosClient(HOST, MASTER_KEY)

     # Create or get a reference to a database
     try:
         database = client.create_database_if_not_exists(id=DATABASE_ID)
         print(f'Database "{DATABASE_ID}" created or retrieved successfully.')

     except exceptions.CosmosResourceExistsError:
         database = client.get_database_client(DATABASE_ID)
         print('Database with id \'{0}\' was found'.format(DATABASE_ID))

     return database


def get_container_client(container_id):
     database = get_database_client()
     # Create or get a reference to a container
     try:
         container = database.create_container(id=container_id, partition_key=PartitionKey(path='/partitionKey'))
         print('Container with id \'{0}\' created'.format(container_id))

     except exceptions.CosmosResourceExistsError:
         container = database.get_container_client(container_id)
         print('Container with id \'{0}\' was found'.format(container_id))

     return container

async def create_item(container_id, item):
    async with CosmosClient(HOST, credential=MASTER_KEY) as client:
        database = client.get_database_client(DATABASE_ID)
        container = database.get_container_client(container_id)
        await container.upsert_item(body=item)


async def get_items(container_id):
    items = []
    try:
        async with CosmosClient(HOST, credential=MASTER_KEY) as client:
            database = client.get_database_client(DATABASE_ID)
            container = database.get_container_client(container_id)
            async for item in container.read_all_items():
                items.append(item)
    except Exception as e:
        print(f"An error occurred: {e}")

    return items
