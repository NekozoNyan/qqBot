import os
from gino import Gino
from .log import logger

db = Gino()

async def init():
    uri = os.environ['DATABASE_URI']
    # if not uri:
    # uri = 'postgresql://meow:kbjwyyany@postgres:5432/meow'
    await db.set_bind(uri)
    await db.gino.create_all()
    logger.info(f"Database loaded successfully!")