import logging
import time
import traceback
from typing import Literal

from requests import Response, Session

from strite_data_hub.parsers.utils import requests_retry_session


def wb_request(url: str,
               api_data: dict,
               version: Literal["new", "old"] = "new",
               method: str = "GET",
               content_type: str = "application/json",
               **kwargs):
    while True:
        try:
            params = kwargs.pop("params", None)
            if version == "old":
                params = {
                    "token": api_data['token'],
                    **params
                }

            headers = {
                "Content-Type": content_type
            }
            if version == "new":
                headers["Authorization"] = api_data['marketplace']

            session: Session = requests_retry_session()
            response: Response = session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=15,
                verify=False,
                params=params,
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
