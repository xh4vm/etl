import logging

from config import ELASTIC_CONFIG, ES_INDEX, POSTGRES_DSN, REDIS_CONFIG
from extractor import PostgreSQLExtractor
from loader import ElasticsearchLoader
from state import RedisState
from transformer import Transformer

if __name__ == '__main__':
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)

    logger = logging.getLogger(__name__)
    logger.info('Starting ETL process...')

    etl_state = RedisState(settings=REDIS_CONFIG)

    pg_extractor = PostgreSQLExtractor(dsn=POSTGRES_DSN, state=etl_state)
    data_transformer = Transformer()
    es_loader = ElasticsearchLoader(settings=ELASTIC_CONFIG, state=etl_state)

    while True:
        raw_data = pg_extractor.get_raw_data()
        data = data_transformer.transform(raw_data=raw_data)
        es_loader.load(data, ES_INDEX.movies)
