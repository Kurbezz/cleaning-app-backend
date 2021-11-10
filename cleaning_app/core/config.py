from pydantic import BaseSettings


class EnvConfig(BaseSettings):
    SERVER_PREFIX: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_TLS: bool = False
    MAIL_SSL: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    SECRET: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


env_config = EnvConfig()
