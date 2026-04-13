from pydantic_settings import BaseSettings


class ExternalApiSettings(BaseSettings):
    CYBER_SPORT_RU: str = "https://www.cybersport.ru/players"

    def get_cyber_sport_ru(self) -> str:
        return self.CYBER_SPORT_RU
