# Strite data hub

--------------------------------------------------------------------------------

[![SAI](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/SAI_badge_flat.svg)](https://sai.itmo.ru/)
[![ITMO](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/ITMO_badge_flat_rus.svg)](https://en.itmo.ru/en/)
[![ENG](https://img.shields.io/badge/lang-en-red.svg)](/README.md)

Предствленная библиотека предназначена для работы с API российских маркетплейсов: Ozon, Wildberries.

## Документация

[Полная документация](https://strite-ru.github.io/strite-data-hub/)

* [Как запустить](#как-запустить)
  - [Требования](#требования)
    - [Установка зависимостей](#установка-зависимостей)
  - [Примеры](#примеры)
* [Структура проекта](#структура-проекта)
* [Начало работы](#начало-работы)
* [Благодарности](#благодарности)

## Как запустить

### Требования

- Python 3.11
- **Ozon** ключ аутентификации
  - `Client-id`
  - `Api-Key`
- **Wildberries** ключ аутентификации
  - `Api-Key`
  - `Statistics-key`


Получение API-ключей для доступа к API можно сделать через личный кабинет на сайте маркетплейсов 
[Ozon](https://docs.ozon.ru/api/seller/#section/Kak-poluchit-dostup-k-Seller-API) и 
[Wildberries](https://openapi.wildberries.ru/#section/Obshee-opisanie/Avtorizaciya).


### Установка зависимостей

```
pip install git+https://github.com/strite-ru/strite-data-hub.git
```

### Примеры

Инициализация объекта с доступами Ozon (для получения данных из маркетплейса)

```python
from strite_data_hub.parsers.ozon import OzonAPI


ozon_api = OzonAPI(client_id="Your_Client-Id", key="Your_Api-Key")
```

Инициализация объекта с доступами Wilderries (для получения данных из маркетплейса)

```python
from strite_data_hub.parsers.wildberries import WildberriesAPI


wb_api = WildberriesAPI(statistics="Your_statistic-key", marketplace="Your_Api-Key")
```

## Структура проекта

Путь к основной библиотеке: `strite_data_hub`. 
Он содержит папки с общей структурой взаимодействия с **Ozon** и **WildBerries**.

- `parsers` папка с взаимодействием с маркетплейсом
  - `ozon`
    - `api`
    - `finance`
    - `orders`
    - `products`
  - `wildberries`
    - `api`
    - `finance`
    - `orders`
    - `products`
    - `warehouses`
- `general_datastructures` папка содержит сущности классов данных
- `utils` папка содержит несколько общих типов и вспомогательных функций
- `requirements.txt` содержит информацию о зависимостях

## Начало работы

[Полная документация](https://strite-ru.github.io/strite-data-hub/)

## Благодарности

> Проект поддерживается Университетом ИТМО.



