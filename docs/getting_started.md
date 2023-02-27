# Начало работы


## Требования

-  [Python 3.11](https://www.python.org/downloads/release/python-3110/).

Для работы с библиотекой необходимо выполнить несколько шагов

## Шаг 0. Установка библиотеки

Установить библиотеку на свой компьютер или сервер. Для этого можно использовать менеджер пакетов, например, pip для Python.

```commandline
pip install git+https://github.com/strite-ru/strite-data-hub.git
```

## Шаг 1. Получение доступов

Получить API-ключи для доступа к API маркетплейсов. Это можно сделать через личный кабинет на сайте маркетплейсов.

### Ozon

Результатом получение доступов будет два значения

> Client-Id =
> 
> Api-Key =


### Wildberries

Для работы библиотеки необходимо выпустить 2 ключа

> Ключ маркетплейса
> 
> Ключ статистики


## Шаг 2. Импорт библиотеки

### Инициализация объекта с доступами Ozon (для получение данных из маркетплейса)

```python
from strite_data_hub.parsers.ozon import OzonAPI


ozon_api = OzonAPI(client_id="Ваш_Client-Id", key="Ваш_Api-Key")
```

### Инициализация объекта с доступами Wilderries (для получение данных из маркетплейса)

```python
from strite_data_hub.parsers.wildberries import WildberriesAPI


wb_api = WildberriesAPI(statistics="Ваш_ключ_статистики", marketplace="Ваш_ключ_маркетплейса")
```