# Strite data hub

--------------------------------------------------------------------------------

[![SAI](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/SAI_badge_flat.svg)](https://sai.itmo.ru/)
[![ITMO](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/ITMO_badge_flat_rus.svg)](https://en.itmo.ru/en/)
[![RU](https://img.shields.io/badge/lang-ru-yellow.svg)](/README_ru.md)

This is a data hub for the Strite project. It is a collection of data sources and tools for data analysis.

## Documentation

[Full docs](https://strite-ru.github.io/strite-data-hub/)


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

[Full docs](https://strite-ru.github.io/strite-data-hub/)

## Acknowledgements

> This project is supported by ITMO University



