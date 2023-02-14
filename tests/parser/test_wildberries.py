from strite_data_hub.parsers import wildberries


def test_wb_parse_product_lazy_from_dict():
    """
    Test parsing product from dict
    """
    raw_data = {
        "nmID": 123456,
        "sizes": [
            {
                "techSize": "Test tech size",
                "skus": [
                    "5032781142964",
                ]
            }
        ],
        "object": "Test object",
        "brand": "Test brand",
        "vendorCode": "123456",
        "updateAt": "2022-08-10T10:16:52Z",
        "mediaFiles": [
            "https://images.wbstatic.net/c516x688/new/12345600-1.jpg",
            "https://images.wbstatic.net/c516x688/new/12345600-2.jpg"
        ],
    }

    product = wildberries.WbProduct.parse_from_dict(raw_data)

    assert product.id == 123456
    assert product.brand == "Test brand"
    assert product.vendor_code == "123456"
    assert product.category == "Test object"
    assert product.sizes == [
        wildberries.WbChart(
            id=None,
            skus=["5032781142964"],
            name="Test tech size",
            price=None
        )
    ]
    assert product.image == "https://images.wbstatic.net/c516x688/new/12345600-1.jpg"
    assert product.link == "https://www.wildberries.ru/catalog/123456/detail.aspx"


def test_wb_parse_product_full_from_dict():
    """
    Test parsing product from dict
    """

    raw_data = {
        "nmID": 123456,
        "vendorCode": "123456",
        "mediaFiles": [
            "https://images.wbstatic.net/c516x688/new/12345600-1.jpg",
            "https://images.wbstatic.net/c516x688/new/12345600-2.jpg"
        ],
        "sizes": [
            {
                "techSize": "Test tech size",
                "skus": [
                    "5032781142964",
                ],
                "price": 1000,
                "wbSize": "Test wb size",
                "chrtID": 123456,
            }
        ],
        "characteristics": [
            {
                "Бренд": "GlisH"
            },
            {
                "Наименование": "Тестовый товар"
            },
            {
                "Предмет": "Тестовый предмет"
            }
        ]
    }

    product = wildberries.WbProduct.parse_from_dict(raw_data)

    assert product.id == 123456
    assert product.brand == "GlisH"
    assert product.vendor_code == "123456"
    assert product.category == "Тестовый предмет"
    assert product.sizes == [
        wildberries.WbChart(
            id=123456,
            skus=["5032781142964"],
            name="Test tech size",
            price=1000
        )
    ]
    assert product.image == "https://images.wbstatic.net/c516x688/new/12345600-1.jpg"
    assert product.link == "https://www.wildberries.ru/catalog/123456/detail.aspx"
    assert product.name == "Тестовый товар"
