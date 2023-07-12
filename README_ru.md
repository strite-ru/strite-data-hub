# Strite data hub

--------------------------------------------------------------------------------

[![SAI](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/SAI_badge_flat.svg)](https://sai.itmo.ru/)
[![ITMO](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/ITMO_badge_flat_rus.svg)](https://en.itmo.ru/en/)
[![ENG](https://img.shields.io/badge/lang-en-red.svg)](/README.md)

Предствленная библиотека предназначена для работы с API российских маркетплейсов: Ozon, Wildberries.

## Документация


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

Данный раздел описывает формат данных, полученный от маркетплейсов
и необходимый для дальнейшего использования другими функциями
библиотеки:

- **Ozon**
  - *Товары*
    - [Объекты описания товара](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D1%8B)
    - [Получить список всех товаров магазина](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%B2%D1%81%D0%B5%D1%85-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%BE%D0%B2-%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD%D0%B0)
    - [Получить все товары с данными артикулами](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%B2%D1%81%D0%B5-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D1%8B-%D1%81-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8-%D0%B0%D1%80%D1%82%D0%B8%D0%BA%D1%83%D0%BB%D0%B0%D0%BC%D0%B8)
  - *Заказы*
    - [Объекты описания заказов](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D1%8B)
    - [Получение отправлений](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B9)
    - [Получить данные стикера по отправлению](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5-%D1%81%D1%82%D0%B8%D0%BA%D0%B5%D1%80%D0%B0-%D0%BF%D0%BE-%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8E)
    - [Передать отправление в доставку](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%B5%D1%80%D0%B5%D0%B4%D0%B0%D1%82%D1%8C-%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B2-%D0%B4%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BA%D1%83)
    - [Создать акт отгрузки](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C-%D0%B0%D0%BA%D1%82-%D0%BE%D1%82%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B8)
    - [Получение информации о товарах из заказов отправления](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%B8-%D0%BE-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%D1%85-%D0%B8%D0%B7-%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%BE%D0%B2-%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F)
- **Wildberries**
  - *Товары*
    - [Объекты описания товара](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D1%8B-1)
    - [Получение списка товаров из маркетплейса](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%B0-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%BE%D0%B2-%D0%B8%D0%B7-%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82%D0%BF%D0%BB%D0%B5%D0%B9%D1%81%D0%B0)
    - [Получить все товары с данными артикулами](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%B2%D1%81%D0%B5-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D1%8B-%D1%81-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8-%D0%B0%D1%80%D1%82%D0%B8%D0%BA%D1%83%D0%BB%D0%B0%D0%BC%D0%B8-1)
  - *Заказы*
    - [Получение новых заказов с данными о товаре](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BD%D0%BE%D0%B2%D1%8B%D1%85-%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%BE%D0%B2-%D1%81-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8-%D0%BE-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%B5)
    - [Отменить заказ](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BE%D1%82%D0%BC%D0%B5%D0%BD%D0%B8%D1%82%D1%8C-%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7)
  - *Supplies*
    - [Объект описания поставок](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BA%D0%B8)
    - [Получить список поставок](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BE%D0%BA)
    - [Получить содержание поставки](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BE%D0%B4%D0%B5%D1%80%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BA%D0%B8)
    - [Действия с поставкой](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D1%8F-%D1%81-%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BA%D0%BE%D0%B9)
- **Транзакции по магазину** (Логика работы и результат вызовов унифицирована для всех маркетплейсов)
  - **Транзакции**
    - [Объект описания транзакций](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D1%82%D1%80%D0%B0%D0%BD%D0%B7%D0%B0%D0%BA%D1%86%D0%B8%D0%B8)
    - [Получение списка транзакций](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%B0-%D1%82%D1%80%D0%B0%D0%BD%D0%B7%D0%B0%D0%BA%D1%86%D0%B8%D0%B9)

## Благодарности

> Проект поддерживается Университетом ИТМО.



