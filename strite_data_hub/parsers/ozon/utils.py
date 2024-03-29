from dataclasses import dataclass
from typing import List

from strite_data_hub.parsers.ozon import OzonWarehouse


@dataclass(frozen=True)
class OzonCluster:
    name: str
    regions: List[str]
    warehouses: List[OzonWarehouse]

def get_clusters_with_warehouses() -> List[OzonCluster]:
    """Списк кластеров с привязанными складами"""
    return [
        OzonCluster(name="Москва и МО",
                    warehouses=[
                        OzonWarehouse(id="15431806189000", name="ХОРУГВИНО_РФЦ"),
                        OzonWarehouse(id="19262731541000", name="Хоругвино_РФЦ_НЕГАБАРИТ"),
                        OzonWarehouse(id="1020000435290000", name="ГРИВНО_РФЦ"),
                        OzonWarehouse(id="23902289166000", name="ПУШКИНО_2_РФЦ"),
                        OzonWarehouse(id="23948599159000", name="ПЕТРОВСКОЕ_РФЦ"),
                        OzonWarehouse(id="1020000268887000", name="ПАВЛО_СЛОБОДСКОЕ_РФЦ_НЕГАБАРИТ"),
                        OzonWarehouse(id="1020000115166000", name="ЖУКОВСКИЙ_РФЦ")
                    ],
                    regions=["Москва", "Московская"]
        ),
        OzonCluster(name="Северо-запад",
                    warehouses=[
                        OzonWarehouse(id="23903599483000", name="СПБ_БУГРЫ_РФЦ"),
                        OzonWarehouse(id="1020000613861000", name="СПБ_ШУШАРЫ_РФЦ"),
                        OzonWarehouse(id="18044249781000", name="Санкт_Петербург_РФЦ")
                    ],
                    regions=["Вологодская", "Карелия", "Ленинградская", "Мурманская", "Новгородская", "Псковская", "Санкт-Петербург"]
        ),
        OzonCluster(name="Центр",
                    warehouses=[
                        OzonWarehouse(id="23021125185000", name="ТВЕРЬ_РФЦ"),
                        OzonWarehouse(id="1020000241710000", name="СОФЬИНО_РФЦ"),
                        OzonWarehouse(id="23843917228000", name="ПУШКИНО_1_РФЦ")
                    ],
                    regions=["Архангельская", "Брянская", "Владимирская", "Ивановская", "Калужская", "Камчатский", "Коми", "Костромская", "Курская", "Липецкая", "Магаданская", "Орловская", "Рязанская", "Саха /Якутия/", "Смоленская", "Тамбовская", "Тверская", "Тульская", "Ярославская", "Ярославская"]
        ),
        OzonCluster(name="Юг",
                    warehouses=[
                        OzonWarehouse(id="23684735180000", name="ВОРОНЕЖ_МРФЦ"),
                        OzonWarehouse(id="23601604393000", name="НОВОРОССИЙСК_МРФЦ"),
                        OzonWarehouse(id="1020000267736000", name="АДЫГЕЙСК_РФЦ"),
                        OzonWarehouse(id="17717042026000", name="Ростов_на_Дону_РФЦ"),
                    ],
                    regions=["Адыгея", "Астраханская", "Белгородская", "Волгоградская", "Воронежская", "Дагестан", "Кабардино-Балкарская", "Карачаево-Черкесская", "Краснодарский", "Крым", "Ростовская", "Севастополь", "Северная Осетия - Алания", "Ставропольский"]
        ),
        OzonCluster(name="Урал",
                    warehouses=[
                        OzonWarehouse(id="18044570445000", name="Екатеринбург_РФЦ_НОВЫЙ")
                    ],
                    regions=["Курганская", "Пермский", "Свердловская", "Тюменская", "Ханты-Мансийский Автономный округ - Югра", "Челябинская", "Ямало-Ненецкий"]
        ),
        OzonCluster(name="Поволжье",
                    warehouses=[
                        OzonWarehouse(id="23599177351000", name="НИЖНИЙ_НОВГОРОД_РФЦ"),
                        OzonWarehouse(id="23128509046000", name="САМАРА_РФЦ"),
                        OzonWarehouse(id="18044494830000", name="Казань_РФЦ_НОВЫЙ")
                    ],
                    regions=["Башкортостан", "Кировская", "Марий Эл", "Мордовия", "Нижегородская", "Оренбургская", "Пензенская", "Самарская", "Саратовская", "Татарстан", "Удмуртская", "Ульяновская", "Чувашская Республика"]
        ),
        OzonCluster(name="Сибирь",
                    warehouses=[
                        OzonWarehouse(id="22296628035000", name="КРАСНОЯРСК_МРФЦ"),
                        OzonWarehouse(id="18044341087000", name="Новосибирск_РФЦ_НОВЫЙ")
                    ],
                    regions=["Алтайский", "Бурятия", "Иркутская", "Кемеровская область - Кузбасс", "Красноярский", "Новосибирская", "Омская", "Томская", "Тыва", "Хакасия", "Алтай"]
        ),
        OzonCluster(name="Дальний Восток",
                    warehouses=[
                        OzonWarehouse(id="21225173751000", name="Хабаровск_РФЦ"),
                    ],
                    regions=["Амурская", "Приморский", "Хабаровский"]
        ),
        OzonCluster(name="Калининград",
                    warehouses=[
                        OzonWarehouse(id="22294782253000", name="КАЛИНИНГРАД_МРФЦ"),
                    ],
                    regions=["Калининградская"]
        ),
        OzonCluster(name="Казахстан",
                    warehouses=[
                        OzonWarehouse(id='1020000367015000', name='АСТАНА_РФЦ'),
                        OzonWarehouse(id='1020000310007000', name='АЛМАТЫ_МРФЦ'),
                    ],
                    regions=[]
        ),
    ]