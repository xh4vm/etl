import logging
from pydantic import BaseSettings, Field
import backoff


logger = logging.getLogger(__name__)


class PostgreSQLSettings(BaseSettings):
    dbname : str = Field(..., env='DB_NAME')
    user : str = Field(..., env='DB_USER')
    password : str = Field(..., env='DB_PASSWORD')
    host : str = Field(..., env='DB_HOST')
    port : int = Field(..., env='DB_PORT')


class RedisSettings(BaseSettings):
    host : str = Field(..., env='REDIS_HOST')
    port : int = Field(..., env='REDIS_PORT')


class ElasticsearchSettings(BaseSettings):
    protocol : str = Field(..., env='ES_PROTOCOL') 
    user : str = Field(..., env='ES_USER') 
    password : str = Field(..., env='ES_PASSWORD') 
    host : str = Field(..., env='ES_HOST')
    port : int = Field(..., env='ES_PORT')


POSTGRES_DSN = PostgreSQLSettings()
REDIS_CONFIG = RedisSettings()
ELASTIC_CONFIG = ElasticsearchSettings()

BACKOFF_CONFIG = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    # "max_tries": APP_CONFIG.backoff_max_retries,
}  