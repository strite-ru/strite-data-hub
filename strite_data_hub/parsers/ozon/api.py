import logging
import time
import traceback
from dataclasses import dataclass
from typing import Self

from requests import Response, Session
from strite_data_hub.parsers.utils import requests_retry_session


@dataclass(frozen=True)
class OzonAPI:
    client_id: int
    key: str

    base_url: str = "https://api-seller.ozon.ru/"

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        """
        :param raw_data: Client-Id and Api-Key
        :return: OzonAPI
        """
        return cls(
            client_id=raw_data['Client-Id'],
            key=raw_data['Api-Key']
        )

    def __dict__(self) -> dict:
        return {
            "Client-Id": self.client_id,
            "Api-Key": self.key
        }

    def request(self,
                url: str,
                method: str = "POST",
                content_type: str = "application/json",
                **kwargs):
        headers = {
            "Client-Id": str(self.client_id),
            "Api-Key": self.key,
            "Content-Type": content_type
        }

        while True:
            try:
                session: Session = requests_retry_session()
                response: Response = session.request(
                    method=method,
                    url=self.base_url+url,
                    headers=headers,
                    timeout=15,
                    verify=False,
                    **kwargs
                )

                session.close()
            except Exception as x:
                logging.error(traceback.print_exc())
                logging.error(x.__class__.__name__)
                if x.__class__.__name__ != "ReadTimeout":
                    raise ConnectionError("Ошибка отправки запроса в маркетплейс") from x
                time.sleep(5)
            else:
                if response.status_code == 401:
                    raise Exception("Маркетплейс отказал в доступе")
                if response.status_code == 429:
                    raise ValueError("Маркетплейс попросил не спамить запросам")
                if not response.ok:
                    logging.error(response.content)
                    raise ValueError("Маркетплейс ответил что-то невнятное")

                if response.headers.get("Content-Type") == "application/json":
                    return response.json()
                else:
                    return response.content
