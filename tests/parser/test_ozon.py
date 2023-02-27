from strite_data_hub.parsers.ozon import OzonPosting


def test_ozon_posting_parse():
    """Test OzonPosting.parse_from_dict"""

    di_data = {
        "result": {
            "postings": [
                {
                    "posting_number": "62149564-0042-1",
                    "order_id": 12011047774,
                    "order_number": "62149564-0042",
                    "status": "delivered",
                    "delivery_method": {
                        "id": 23459166662000,
                        "name": "Доставка Ozon самостоятельно, Красногорск",
                        "warehouse_id": 23459166662000,
                        "warehouse": "Олег",
                        "tpl_provider_id": 24,
                        "tpl_provider": "Доставка Ozon"
                    },
                    "tracking_number": "",
                    "tpl_integration_type": "ozon",
                    "in_process_at": "2023-01-15T06:25:45Z",
                    "shipment_date": "2023-01-16T12:00:00Z",
                    "delivering_date": "2023-01-16T17:44:09Z",
                    "cancellation": {
                        "cancel_reason_id": 0,
                        "cancel_reason": "",
                        "cancellation_type": "",
                        "cancelled_after_ship": False,
                        "affect_cancellation_rating": False,
                        "cancellation_initiator": ""
                    },
                    "customer": None,
                    "products": [
                        {
                            "price": "1199.000000",
                            "offer_id": "УТ-00015349",
                            "name": "Набор для настольного тенниса Top Team 400, 2 ракетки, 3 мяча",
                            "sku": 155024968,
                            "quantity": 1,
                            "mandatory_mark": [
                                ""
                            ],
                            "currency_code": "RUB"
                        }
                    ],
                    "addressee": None,
                    "barcodes": {
                        "upper_barcode": "%101%1720049505",
                        "lower_barcode": "200273445170000"
                    },
                    "analytics_data": None,
                    "financial_data": None,
                    "is_express": False,
                    "requirements": {
                        "products_requiring_gtd": [],
                        "products_requiring_country": [],
                        "products_requiring_mandatory_mark": [],
                        "products_requiring_rnpt": []
                    },
                    "parent_posting_number": "",
                    "available_actions": [],
                    "multi_box_qty": 1,
                    "is_multibox": False,
                    "substatus": "posting_received"
                },
                {
                    "posting_number": "41125036-0001-1",
                    "order_id": 4011090279,
                    "order_number": "41125036-0001",
                    "status": "delivered",
                    "delivery_method": {
                        "id": 23459166662000,
                        "name": "Доставка Ozon самостоятельно, Красногорск",
                        "warehouse_id": 23459166662000,
                        "warehouse": "Олег",
                        "tpl_provider_id": 24,
                        "tpl_provider": "Доставка Ozon"
                    },
                    "tracking_number": "",
                    "tpl_integration_type": "ozon",
                    "in_process_at": "2023-01-15T11:59:43Z",
                    "shipment_date": "2023-01-16T12:00:00Z",
                    "delivering_date": "2023-01-16T17:43:38Z",
                    "cancellation": {
                        "cancel_reason_id": 0,
                        "cancel_reason": "",
                        "cancellation_type": "",
                        "cancelled_after_ship": False,
                        "affect_cancellation_rating": False,
                        "cancellation_initiator": ""
                    },
                    "customer": None,
                    "products": [
                        {
                            "price": "2919.000000",
                            "offer_id": "УТ-00000979",
                            "name": "Ласты резиновые \"Дельфин\", размер 38-40",
                            "sku": 160232434,
                            "quantity": 1,
                            "mandatory_mark": [
                                ""
                            ],
                            "currency_code": "RUB"
                        }
                    ],
                    "addressee": None,
                    "barcodes": {
                        "upper_barcode": "%101%1721195962",
                        "lower_barcode": "400051135719000"
                    },
                    "analytics_data": None,
                    "financial_data": None,
                    "is_express": False,
                    "requirements": {
                        "products_requiring_gtd": [],
                        "products_requiring_country": [],
                        "products_requiring_mandatory_mark": [],
                        "products_requiring_rnpt": []
                    },
                    "parent_posting_number": "",
                    "available_actions": [],
                    "multi_box_qty": 1,
                    "is_multibox": False,
                    "substatus": "posting_received"
                },
                {
                    "posting_number": "49867145-0024-1",
                    "order_id": 4011155551,
                    "order_number": "49867145-0024",
                    "status": "delivered",
                    "delivery_method": {
                        "id": 23459166662000,
                        "name": "Доставка Ozon самостоятельно, Красногорск",
                        "warehouse_id": 23459166662000,
                        "warehouse": "Олег",
                        "tpl_provider_id": 24,
                        "tpl_provider": "Доставка Ozon"
                    },
                    "tracking_number": "",
                    "tpl_integration_type": "ozon",
                    "in_process_at": "2023-01-15T19:49:58Z",
                    "shipment_date": "2023-01-16T12:00:00Z",
                    "delivering_date": "2023-01-16T17:43:32Z",
                    "cancellation": {
                        "cancel_reason_id": 0,
                        "cancel_reason": "",
                        "cancellation_type": "",
                        "cancelled_after_ship": False,
                        "affect_cancellation_rating": False,
                        "cancellation_initiator": ""
                    },
                    "customer": None,
                    "products": [
                        {
                            "price": "1559.000000",
                            "offer_id": "УТ-00014742",
                            "name": "Набор для бадминтона WISH Fusiontec 770K (2 ракетки), синий/зеленый",
                            "sku": 155024935,
                            "quantity": 1,
                            "mandatory_mark": [
                                ""
                            ],
                            "currency_code": "RUB"
                        }
                    ],
                    "addressee": None,
                    "barcodes": {
                        "upper_barcode": "%101%1722970214",
                        "lower_barcode": "400051342996000"
                    },
                    "analytics_data": None,
                    "financial_data": None,
                    "is_express": False,
                    "requirements": {
                        "products_requiring_gtd": [],
                        "products_requiring_country": [],
                        "products_requiring_mandatory_mark": [],
                        "products_requiring_rnpt": []
                    },
                    "parent_posting_number": "",
                    "available_actions": [],
                    "multi_box_qty": 1,
                    "is_multibox": False,
                    "substatus": "posting_received"
                },
                {
                    "posting_number": "32210734-0030-1",
                    "order_id": 10011153887,
                    "order_number": "32210734-0030",
                    "status": "delivered",
                    "delivery_method": {
                        "id": 23459166662000,
                        "name": "Доставка Ozon самостоятельно, Красногорск",
                        "warehouse_id": 23459166662000,
                        "warehouse": "Олег",
                        "tpl_provider_id": 24,
                        "tpl_provider": "Доставка Ozon"
                    },
                    "tracking_number": "",
                    "tpl_integration_type": "ozon",
                    "in_process_at": "2023-01-15T20:15:40Z",
                    "shipment_date": "2023-01-16T12:00:00Z",
                    "delivering_date": "2023-01-16T17:44:15Z",
                    "cancellation": {
                        "cancel_reason_id": 0,
                        "cancel_reason": "",
                        "cancellation_type": "",
                        "cancelled_after_ship": False,
                        "affect_cancellation_rating": False,
                        "cancellation_initiator": ""
                    },
                    "customer": None,
                    "products": [
                        {
                            "price": "1379.000000",
                            "offer_id": "УТ-00018947",
                            "name": "Фитбол полумассажный Core GB-201 антивзрыв, синий пастель, 75 см",
                            "sku": 317622646,
                            "quantity": 1,
                            "mandatory_mark": [
                                ""
                            ],
                            "currency_code": "RUB"
                        }
                    ],
                    "addressee": None,
                    "barcodes": {
                        "upper_barcode": "%101%1723046645",
                        "lower_barcode": "600051349961000"
                    },
                    "analytics_data": None,
                    "financial_data": None,
                    "is_express": False,
                    "requirements": {
                        "products_requiring_gtd": [],
                        "products_requiring_country": [],
                        "products_requiring_mandatory_mark": [],
                        "products_requiring_rnpt": []
                    },
                    "parent_posting_number": "",
                    "available_actions": [],
                    "multi_box_qty": 1,
                    "is_multibox": False,
                    "substatus": "posting_received"
                },
                {
                    "posting_number": "45594988-0027-2",
                    "order_id": 13011178388,
                    "order_number": "45594988-0027",
                    "status": "delivered",
                    "delivery_method": {
                        "id": 23459166662000,
                        "name": "Доставка Ozon самостоятельно, Красногорск",
                        "warehouse_id": 23459166662000,
                        "warehouse": "Олег",
                        "tpl_provider_id": 24,
                        "tpl_provider": "Доставка Ozon"
                    },
                    "tracking_number": "",
                    "tpl_integration_type": "ozon",
                    "in_process_at": "2023-01-16T06:47:34Z",
                    "shipment_date": "2023-01-17T12:00:00Z",
                    "delivering_date": "2023-01-17T16:42:35Z",
                    "cancellation": {
                        "cancel_reason_id": 0,
                        "cancel_reason": "",
                        "cancellation_type": "",
                        "cancelled_after_ship": False,
                        "affect_cancellation_rating": False,
                        "cancellation_initiator": ""
                    },
                    "customer": None,
                    "products": [
                        {
                            "price": "2729.000000",
                            "offer_id": "УТ-00015337",
                            "name": "Ракетка н/т Donic Top Team 900",
                            "sku": 155024945,
                            "quantity": 1,
                            "mandatory_mark": [
                                ""
                            ],
                            "currency_code": "RUB"
                        }
                    ],
                    "addressee": None,
                    "barcodes": {
                        "upper_barcode": "%101%1723758275",
                        "lower_barcode": "200273880305000"
                    },
                    "analytics_data": None,
                    "financial_data": None,
                    "is_express": False,
                    "requirements": {
                        "products_requiring_gtd": [],
                        "products_requiring_country": [],
                        "products_requiring_mandatory_mark": [],
                        "products_requiring_rnpt": []
                    },
                    "parent_posting_number": "",
                    "available_actions": [],
                    "multi_box_qty": 1,
                    "is_multibox": False,
                    "substatus": "posting_received"
                },
            ],
            "has_next": False
        },
    }

    for item in di_data['result']['postings']:
        assert OzonPosting.parse_from_dict(item)
