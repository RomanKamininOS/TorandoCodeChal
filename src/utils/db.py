import base64
import logging
import rsa
from tornado.options import options

from pymysql import DatabaseError

from utils import sha_hash

update_words_query = """
INSERT INTO words_data(id, word, frequency, total_frequency) 
       VALUES('{id}', '{word}', {frequency}, {frequency})
       ON DUPLICATE KEY UPDATE total_frequency=total_frequency+{frequency};
"""

get_words_query = """
SELECT word, frequency, total_frequency FROM words_data ORDER BY frequency DESC;
"""


async def update_words_data(words_data, pool):
    """ Uses connection pool to write words data into DB"""
    with await pool.Connection() as conn:
        try:
            with conn.cursor() as cursor:
                for word, frequency in words_data.items():
                    word_hash = sha_hash(word)
                    encrypted_word = rsa.encrypt(word.encode('utf8'), options.public_key)
                    encrypted_word = base64.b64encode(encrypted_word).decode('utf8')
                    query = update_words_query.format(id=word_hash,
                                                      word=encrypted_word,
                                                      frequency=frequency)
                    await cursor.execute(query)
        except DatabaseError as e:
            logging.error('SQL error: {}'.format(e))
            await conn.rollback()
        else:
            logging.info('SQL committed')
            await conn.commit()

    await pool.close()


async def get_words_data(pool):
    """ Uses connection pool to get words data from DB"""
    with await pool.Connection() as conn:
        with conn.cursor() as cursor:
            await cursor.execute(get_words_query)
            words_data = cursor.fetchall()
    await pool.close()
    words_data = [(rsa.decrypt(base64.b64decode(x[0]), options.private_key).decode('utf8'), x[1], x[2])
                  for x in words_data]
    return words_data
