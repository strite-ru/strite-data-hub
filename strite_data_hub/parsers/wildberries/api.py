import logging
import time
import traceback
from dataclasses import dataclass
from typing import Self

from requests import Response, Session
from strite_data_hub.parsers.utils import requests_retry_session


@dataclass(frozen=True)
class WildberriesAPI:
    statistics: str
    marketplace: str

    base_url: str = "https://suppliers-api.wildberries.ru/"

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        return cls(
            statistics=raw_data['statistics'],
            marketplace=raw_data['marketplace']
        )

    def __dict__(self) -> dict:
        return {
            "statistics": self.statistics,
            "marketplace": self.marketplace
        }

    def marketplace_request(self,
                            url: str,
                            method: str = "GET",
                            content_type: str = "application/json",
                            **kwargs):
        headers = {
            "Content-Type": content_type,
            "Authorization": self.marketplace
        }
        while True:
            try:
                session: Session = requests_retry_session()
                response: Response = session.request(
                    method=method,
                    url=self.base_url + url,
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
                    raise ValueError("Маркетплейс ответил что-то невнятное")

                if response.headers.get("Content-Type") == "application/json":
                    return response.json()
                else:
                    return response.content

    def statistics_request(self,
                           url: str,
                           method: str = "GET",
                           content_type: str = "application/json",
                           **kwargs):
        params = {
            "key": self.statistics,
            **kwargs.pop("params", None)
        }
        headers = {
            "Content-Type": content_type,
            **kwargs.pop("headers", None)
        }
        while True:
            try:
                session: Session = requests_retry_session()
                response: Response = session.request(
                    method=method,
                    url=url,
                    timeout=15,
                    verify=False,
                    params=params,
                    headers=headers,
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
                    raise ValueError("Маркетплейс ответил что-то невнятное")

                if response.headers.get("Content-Type") == "application/json":
                    return response.json()
                else:
                    return response.content
