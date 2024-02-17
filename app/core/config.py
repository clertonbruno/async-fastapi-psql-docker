from typing import Any

from pydantic import BaseSettings, Field, PostgresDsn, validator


class Settings(BaseSettings):
    VERSION: str = Field("0.0.1")
    PROJECT_NAME: str = Field("Inventory Management with FastAPI and Postgres")
    POSTGRES_USER: str = Field("postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("password", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("inventory_db", env="POSTGRES_DB")
    POSTGRES_HOST: str = Field("localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: int | str = Field("5432", env="POSTGRES_PORT")
    POSTGRES_ECHO: bool = Field(False, env="POSTGRES_ECHO")
    POSTGRES_POOL_SIZE: int = Field(10, env="POSTGRES_POOL_SIZE")
    ASYNC_POSTGRES_URI: PostgresDsn | None

    class Config:
        case_sensitive = True
        env_file = ".env"

    @validator("ASYNC_POSTGRES_URI", pre=True)
    def assemble_db_connection(
        cls, uri_value: str | None, values: dict[str, Any]
    ) -> Any:
        """
        Assembles the database connection URI.

        Args:
          uri_value (str | None): The URI value.
          values (dict[str, Any]): The dictionary of values.

        Returns:
          Any: The assembled database connection URI.
        """

        if isinstance(uri_value, str):
            return uri_value

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=str(values.get("POSTGRES_PORT")),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
