from celery import Celery
import logging

from config import ELASTIC_CONFIG, ES_INDEX, POSTGRES_DSN, REDIS_CONFIG, CELERY_CONFIG
from extractor import PostgreSQLExtractor
from loader import ElasticsearchLoader
from state import RedisState
from transformer import Transformer


celery = Celery(
    CELERY_CONFIG.name, 
    backend=CELERY_CONFIG.backend,
    broker=CELERY_CONFIG.broker
)


@celery.task
def etl():
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)

    logger = logging.getLogger(__name__)
    logger.info('Starting ETL process...')

    etl_state = RedisState(settings=REDIS_CONFIG)

    pg_extractor = PostgreSQLExtractor(dsn=POSTGRES_DSN, state=etl_state)
    data_transformer = Transformer()
    es_loader = ElasticsearchLoader(settings=ELASTIC_CONFIG, state=etl_state)

    raw_data = pg_extractor.get_raw_data()
    data = data_transformer.transform(raw_data=raw_data)
    es_loader.load(data, ES_INDEX.movies)


@celery.on_after_configure.connect
def setup_etl_periodic_task(sender, **kwargs):
    sender.add_periodic_task(30.0, etl.s(), name='Update ETL every 30 seconds.')
