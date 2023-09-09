# Strite data hub

--------------------------------------------------------------------------------

[![SAI](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/SAI_badge_flat.svg)](https://sai.itmo.ru/)
[![ITMO](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/ITMO_badge_flat_rus.svg)](https://en.itmo.ru/en/)
[![RU](https://img.shields.io/badge/lang-ru-yellow.svg)](/README_ru.md)

This is a data hub for the Strite project. It is a collection of data sources and tools for data analysis.

## Documentation

- [Полная документация по библиотеке](https://strite-ru.github.io/strite-data-hub/)

* [How to bootstrap](#how-to-bootstrap)
  - [Requirements](#requirements)
    - [Install dependencies](#install-dependencies)
  - [Examples](#examples)
* [Project structure](#project-structure)
* [Getting started](#getting-started)
* [Acknowledgements](#acknowledgements)

## How to bootstrap

### Requirements

- Python 3.11
- **Ozon** authentication key
  - `Client-id`
  - `Api-Key`
- **Wildberries** authentication key
  - `Api-Key`
  - `Statistics-key`


Obtaining API keys for accessing the marketplace API can be done through your personal account 
on the website of the [Ozon](https://docs.ozon.ru/api/seller/#section/Kak-poluchit-dostup-k-Seller-API) 
and [Wildberries](https://openapi.wildberries.ru/#section/Obshee-opisanie/Avtorizaciya) marketplaces.


### Install dependencies

```
pip install git+https://github.com/strite-ru/strite-data-hub.git
```

### Examples

Initialization of an object with Ozon access (to receive data from the marketplace)

```python
from strite_data_hub.parsers.ozon import OzonAPI


ozon_api = OzonAPI(client_id="Your_Client-Id", key="Your_Api-Key")
```

Initializing an object with Wilderries access (for getting data from the marketplace)

```python
from strite_data_hub.parsers.wildberries import WildberriesAPI


wb_api = WildberriesAPI(statistics="Your_statistic-key", marketplace="Your_Api-Key")
```

## Project structure

Core library path is `strite_data_hub`. It contains folders with common structure of interaction with **Ozon** and **WildBerries**.

- `parsers` folder with marketplace interaction
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
- `general_datastructures` folder contains dataclasses entities
- `utils` folder contains several common types and helper functions
- `requirements.txt` contains requirements information

## Getting Started

This section describes the data format received from marketplaces and required for further use by other functions of the library:

- **Ozon**
  - *Goods*
    - [Item description objects](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D1%8B)
    - [Get a list of all store products](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%B2%D1%81%D0%B5%D1%85-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%BE%D0%B2-%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD%D0%B0)
    - [Get all products with given SKUs](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%B2%D1%81%D0%B5-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D1%8B-%D1%81-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8-%D0%B0%D1%80%D1%82%D0%B8%D0%BA%D1%83%D0%BB%D0%B0%D0%BC%D0%B8)
  - *Orders*
    - [Order Description Objects](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D1%8B)
    - [Receiving shipments](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B9)
    - [Get sticker data by shipment](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5-%D1%81%D1%82%D0%B8%D0%BA%D0%B5%D1%80%D0%B0-%D0%BF%D0%BE-%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8E)
    - [Submit a shipment for delivery](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%B5%D1%80%D0%B5%D0%B4%D0%B0%D1%82%D1%8C-%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B2-%D0%B4%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BA%D1%83)
    - [Create a shipping act](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C-%D0%B0%D0%BA%D1%82-%D0%BE%D1%82%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B8)
    - [Retrieving product information from shipping orders](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%B8-%D0%BE-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%D1%85-%D0%B8%D0%B7-%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%BE%D0%B2-%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F)
- **Wildberries**
  - *Goods*
    - [Item description objects](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D1%8B-1)
    - [Get a list of all store products](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%B0-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%BE%D0%B2-%D0%B8%D0%B7-%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82%D0%BF%D0%BB%D0%B5%D0%B9%D1%81%D0%B0)
    - [Get all products with given SKUs](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%B2%D1%81%D0%B5-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D1%8B-%D1%81-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8-%D0%B0%D1%80%D1%82%D0%B8%D0%BA%D1%83%D0%BB%D0%B0%D0%BC%D0%B8-1)
  - *Orders*
    - [Receiving new orders with product data](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BD%D0%BE%D0%B2%D1%8B%D1%85-%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%BE%D0%B2-%D1%81-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8-%D0%BE-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%B5)
    - [Cancel the order](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BE%D1%82%D0%BC%D0%B5%D0%BD%D0%B8%D1%82%D1%8C-%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7)
  - *Supplies*
    - [Supply Description Object](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BA%D0%B8)
    - [Get a list of supplies](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BE%D0%BA)
    - [Get delivery content](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BE%D0%B4%D0%B5%D1%80%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BA%D0%B8)
    - [Delivery Actions](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D1%8F-%D1%81-%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BA%D0%BE%D0%B9)
- **Store transactions** (The logic of work and the result of calls are unified for all marketplaces)
  - **Transactions**
    - [Transaction description object](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D1%82%D1%80%D0%B0%D0%BD%D0%B7%D0%B0%D0%BA%D1%86%D0%B8%D0%B8)
    - [Getting a list of transactions](https://github.com/strite-ru/strite-data-hub/blob/master/docs/parsing.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%B0-%D1%82%D1%80%D0%B0%D0%BD%D0%B7%D0%B0%D0%BA%D1%86%D0%B8%D0%B9)

## Acknowledgements

> This project is supported by ITMO University



