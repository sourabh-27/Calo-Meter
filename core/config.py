import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator, AnyUrl, RedisDsn
import os
import datetime
import platform
import logging, logging.config
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    
    API_V1_STR: str = "/api/cm/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY_CM: str = os.getenv("SECRET_KEY_CM")
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 * 10
    SERVER_NAME: str = 'localhost'
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"
    redis_dsn = os.getenv("REDIS_HOST")
    WRITEKEY: str = os.getenv("WRITEKEY")
    DEVICETYPE: str = os.getenv("DEVICETYPE")
    BACKEND_CORS_ORIGINS: List[str] = ["*", "http://localhost", "http://localhost:4200", "http://localhost:3000", "http://localhost:4000", "http://localhost:8000", "http://localhost:8080" ]
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = 'CalorieMeter'
    SENTRY_DSN: Optional[HttpUrl] = 'https://public@sentry.example.com/1'

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v
    
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_USERNAME: str = os.getenv("MYSQL_USERNAME")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_DBNAME: str = os.getenv("MYSQL_DBNAME")
    SQLALCHEMY_DATABASE_URI: Optional[AnyUrl] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AnyUrl.build(
            scheme="mysql",
            user=values.get("MYSQL_USERNAME"),
            password=values.get("MYSQL_PASSWORD"),
            host=values.get("MYSQL_HOST"),
            path=f"/{values.get('MYSQL_DBNAME') or ''}",
        )


    class Config:
        case_sensitive = True

    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'm!zkr$$#&k=pfl%ibr^bwus*bv92((73=$skgj_n!@p)luhi3h'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    ALLOWED_HOSTS = ['127.0.0.1']

    MIDDLEWARE = []

    # Database
    # https://docs.djangoproject.com/en/2.0/ref/settings/#databases

    # Local db settings

    # Internationalization
    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'Asia/Kolkata'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/

    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    print(platform.system())
    if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
        os.makedirs(str(os.path.join(BASE_DIR, 'logs')))


    if platform.system() in ['Linux', 'Darwin']:
        LOG_PATH  = os.path.join(BASE_DIR,'logs/debug-' + datetime.datetime.now().strftime('%d_%m_%Y') + '.log')
    else:
        LOG_PATH  = os.path.join(BASE_DIR,'logs\debug-' + datetime.datetime.now().strftime('%d_%m_%Y') + '.log')
    
    print(LOG_PATH)

    USERS_OPEN_REGISTRATION: bool = True

    # if not os.path.exists(LOG_PATH):
    #     with open(LOG_PATH,'w+') as f:
    #         f.write('Starting caloriemeter log')
    #         f.close()
    
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format' : "[%(levelname) -10s %(asctime)s %(name) -10s %(funcName) -10s %(lineno) -5d: %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
        },
        'handlers': {
            'null': {
                'level':'DEBUG',
                'class':'logging.NullHandler',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': LOG_PATH,
                'formatter': 'standard',
            },
            'console':{
                'level':'INFO',
                'class':'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
           
            'caloriemeter': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }

    logging.config.dictConfig(LOGGING)


settings = Settings()

