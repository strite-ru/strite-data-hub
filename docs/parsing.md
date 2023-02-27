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

### Товары

Объекты описания товара

```python
class WbChart:
    """
    Объект хранения размеров
    """
    id: Optional[int]  # chrtID
    skus: list[str]  # Массив баркодов
    name: str  # techSize Размер поставщика
    price: Optional[int]  # price

class WbCharacteristic:
    """
    Объект хранения характеристик
    """
    key: list[str]
    value: Any

class WbProduct:
    """
    Объект хранения товара
    """
    id: int  # nmID
    name: Optional[str]  # none
    sizes: list[WbChart]  # sizes
    image: str  # mediaFiles[0]
    vendor_code: str  # vendorCode
    link: str  # generate
    brand: str  # brand
    category: str  # object
    characteristics: Optional[list[WbCharacteristic]]
```

#### Получение списка товаров из маркетплейса
```python
from strite_data_hub.parsers.wildberries import WildberriesAPI, WbProduct, WbChart, WbCharacteristic

# создание объекта для запросов в маркетплейс
my_market = WildberriesAPI(marketplace="xxx", statistics="sss")

my_products: list[WbProduct] = WbProduct.get_products(api=my_market)
```

#### Получить все товары с данными артикулами

```python
from strite_data_hub.parsers.wildberries import WildberriesAPI, WbProduct, WbChart, WbCharacteristic

# создание объекта для запросов в маркетплейс
my_market = WildberriesAPI(marketplace="xxx", statistics="sss")

my_articles = [
    "палочки_для_еды",
    "мягкая_игрушка_зверь"
]

my_products: list[WbProduct] = WbProduct.get_products_by_codes(api=my_market, vendor_codes=my_articles)
```

### Заказы

Объекты описания заказов

```python
class WbOrder:
    deliveryType: Literal['fbs', 'dbs']  # Тип доставки: fbs - доставка на склад, dbs - доставка силами поставщика.
    vendor_code: str
    chartId: int
    orderId: str  # orderUId
    id: int
    rid: str  # rid
    createdAt: datetime
    warehouseId: int
    supplyId: Optional[str]
    barcode: list[str]  # skus
    price: int  # price
    product: Optional[WbProduct] = None
    sticker: Optional[WbSticker] = None
```

#### Получение новых заказов с данными о товаре

```python
from strite_data_hub.parsers.wildberries import WbOrder, WbSticker, WbProduct, WildberriesAPI

# создание объекта для запросов в маркетплейс
my_market = WildberriesAPI(marketplace="xxx", statistics="sss")

new_orders = WbOrder.get_new_orders(api=my_market)

for order in new_orders:
    product_info: WbProduct = order.get_product(api=my_market)
    sticker: WbSticker = order.get_sticker(api=my_market)
```

#### Отменить заказ

```python
from strite_data_hub.parsers.wildberries import WbOrder, WildberriesAPI

# создание объекта для запросов в маркетплейс
my_market = WildberriesAPI(marketplace="xxx", statistics="sss")

order: WbOrder = WbOrder(...)

order.cancel(api=my_market)
```

### Поставки

Объект описания поставок

```python
class WbSupply:
    id: str
    done: bool
    name: str
    createdAt: datetime
    scanAt: Optional[datetime]  # scanDt
    closedAt: Optional[datetime]
    orders: Optional[list[WbOrder]] = None
```

#### Получить список поставок

```python
from strite_data_hub.parsers.wildberries import WildberriesAPI, WbSupply

# создание объекта для запросов в маркетплейс
my_market = WildberriesAPI(marketplace="xxx", statistics="sss")

supplies = WbSupply.get_supplies(api=my_market)
```

#### Получить содержение поставки

```python
from strite_data_hub.parsers.wildberries import WildberriesAPI, WbSupply

# создание объекта для запросов в маркетплейс
my_market = WildberriesAPI(marketplace="xxx", statistics="sss")

supplies = WbSupply.get_supplies(api=my_market)

for supply in supplies:
    orders = supply.get_orders(api=my_market)
```

#### Действия с поставкой

```python
from strite_data_hub.parsers.wildberries import WildberriesAPI, WbSupply

# создание объекта для запросов в маркетплейс
my_market = WildberriesAPI(marketplace="xxx", statistics="sss")

supply = next(iter(WbSupply.get_supplies(api=my_market)), None)

if supply:
    # Добавление заказа
    supply.add_order(api=my_market, order_id="id_заказа")
    # Закрытие поставки
    supply.close(api=my_market)
    # Отменить поставку
    supply.cancel(api=my_market)
    # Удалить (пустую) поставку
    supply.delete(api=my_market)
```
