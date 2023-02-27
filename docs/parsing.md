# Парсинг данных

Данный раздел описывает формат данных, полченный от маркетплейсов
и необходимый для дальнейшего использования другими функциями
библиотеки

## Ozon

### Товары

Объекты описания товара

```python
class OzonSku:
    type: Literal['fbs', 'dbs', 'fbo', 'rfbs']  # source
    id: int  # sku

class OzonProduct:
    id: int  # id
    vendor_code: str  # offer_id
    name: str  # name
    sizes: list[OzonSku]  # sizes
    image: str  # primary_image
    barcode: str  # barcode
```

#### Полчить список всех товаров магазина
```python
from strite_data_hub.parsers.ozon import OzonProduct, OzonAPI

# создание объекта для запросов в маркетплейс
my_market = OzonAPI(client_id=0000, key="xxx")

# получение списока объектов OzonProduct
my_products = OzonProduct.get_products(api=my_market) 
```

#### Получить все товары с данными артикулами
```python
from strite_data_hub.parsers.ozon import OzonProduct, OzonAPI

# создание объекта для запросов в маркетплейс
my_market = OzonAPI(client_id=0000, key="xxx")

my_articles = [
    "палочки_для_еды",
    "мягкая_игрушка_зверь"
]

# получение списока объектов OzonProduct по артикулам
my_products = OzonProduct.get_products_by_codes(api=my_market, vendor_codes=my_articles) 
```

### Заказы

Объекты описания заказов

```python
class OzonOrder:
    price: float
    vendor_code: str
    sku: int
    quantity: int

class OzonPosting:
    """
    Данные по отправлению
    """

    orderId: str  # order_number
    postingId: str  # posting_number
    barcode: str  # barcodes.lower_barcode
    processTo: datetime
    shipmentAt: Optional[datetime]
    deliverAt: Optional[datetime]
    orders: list[OzonOrder]
    status: str
```

#### Получение отправлений

```python
from strite_data_hub.parsers.ozon import OzonPosting, OzonAPI

# создание объекта для запросов в маркетплейс
my_market = OzonAPI(client_id=0000, key="xxx")

# Получение всех отправлений в статусе ожидает сборки
# Всего статусов 3
# awaiting_packaging - ожидает сборки
# awaiting_deliver - ожидает передачи в доставку
# delivering - доставляется

my_postings: list[OzonPosting] = OzonPosting.get_postings(api=my_market, status="awaiting_packaging")
```

#### Получить данные стикера по отправлению
```python
from strite_data_hub.parsers.ozon import OzonPosting, OzonAPI

# создание объекта для запросов в маркетплейс
my_market = OzonAPI(client_id=0000, key="xxx")

posting: OzonPosting = OzonPosting()

posting.get_sticker(api=my_market)
```

#### Передать отправление в доставку
```python
from strite_data_hub.parsers.ozon import OzonPosting, OzonAPI

# создание объекта для запросов в маркетплейс
my_market = OzonAPI(client_id=0000, key="xxx")

posting: OzonPosting = OzonPosting()

posting.close(api=my_market)
```

#### Создать акт отгрузки
```python
from datetime import datetime
from strite_data_hub.parsers.ozon import OzonPosting, OzonAPI

# создание объекта для запросов в маркетплейс
my_market = OzonAPI(client_id=0000, key="xxx")

OzonPosting.create_act(api=my_market, departure_date=datetime.now())
```

#### Получение информации о товарах из заказов отправления
```python
from strite_data_hub.parsers.ozon import OzonPosting, OzonProduct, OzonAPI, OzonOrder

# создание объекта для запросов в маркетплейс
my_market = OzonAPI(client_id=0000, key="xxx")

posting: OzonPosting = OzonPosting()

products : list[OzonProduct] = OzonOrder.get_products_info(api=my_market, orders=posting.orders)
```


## Wildberries

### Заказы

### Товары

### Поставки

### Склады