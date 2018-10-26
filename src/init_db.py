import os

from tornado.ioloop import IOLoop
import tormysql

db_pool = tormysql.helpers.ConnectionPool(
    max_connections=20,
    idle_seconds=7200,
    wait_connection_timeout=3,
    host=os.getenv('MYSQL_HOST', '127.0.0.1'),
    user="root",
    passwd="example",
    charset="utf8"
)


async def init_db():
    tx = await db_pool.begin()
    try:
        await tx.execute("CREATE DATABASE IF NOT EXISTS tornado_ua;")
        await tx.execute("CREATE TABLE IF NOT EXISTS tornado_ua.words_data "
                         "(id VARCHAR(255) PRIMARY KEY NOT NULL,"
                         " word VARCHAR(255) NOT NULL, "
                         "frequency INT DEFAULT 0, "
                         "total_frequency INT DEFAULT 0 );")
    except Exception as e:
        print(e)
        await tx.rollback()
    else:
        print('commit')
        await tx.commit()

    await db_pool.close()


ioloop = IOLoop.instance()
ioloop.run_sync(init_db)
