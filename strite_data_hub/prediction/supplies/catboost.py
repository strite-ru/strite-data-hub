from datetime import datetime, timedelta

import numpy as np
from catboost import CatBoostRegressor
import pandas as pd

from strite_data_hub.parsers.ozon import OzonPosting, OzonProduct
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import mean_absolute_error as MAE
from sklearn.metrics import median_absolute_error as MdAE

def calculate_metrics(actual, predicted, model=""):
    def MdAPE(actual, predicted):
        return np.median((np.abs(np.subtract(actual, predicted) / actual))) * 100

    def rmse_na(y_true, y_pred):
        idx = np.logical_not(np.logical_or(np.isnan(y_true), np.isnan(y_pred)))
        y_true = y_true[idx]
        y_pred = y_pred[idx]
        se = (y_true - y_pred) ** 2
        mse = np.mean(se)
        rmse = np.sqrt(mse)
        return rmse

    def mae_na(y_true, y_pred):
        mask = ~np.isnan(y_true)
        y_true = y_true[mask]
        y_pred = y_pred[mask]
        mae = np.abs(y_true - y_pred).mean()
        return mae

    def mdae_na(y_true, y_pred):
        mask = ~np.isnan(y_true)
        y_true = y_true[mask]
        y_pred = y_pred[mask]
        mae = np.abs(y_true - y_pred)
        return np.nanmedian(mae)

    def mdape_na(y_true, y_pred):
        mask = ~np.isnan(y_true)
        y_true = y_true[mask]
        y_pred = y_pred[mask]
        mape = np.abs((y_true - y_pred) / y_true)
        return np.nanmedian(mape) * 100

    any_nan = np.isnan(predicted).any()

    if (any_nan):
        rmse = rmse_na(actual, predicted)
        mae = mae_na(actual, predicted)
        mdae = mdae_na(actual, predicted)
        mdape = mdape_na(actual, predicted)

        print(f'RMSE for model {model} : {rmse.round(3)}')
        print(f'MAE for model {model} : {mae.round(3)}')
        print(f'MdAE for model {model} : {mdae.round(3)}')
        print(f'MdAPE for model {model} : {mdape.round(3)}')
    else:
        rmse = np.sqrt(MSE(actual, predicted))
        mae = MAE(actual, predicted)
        mdae = MdAE(actual, predicted)
        mdape = MdAPE(actual, predicted)

        print(f'RMSE for model {model} : {rmse.round(3)}')
        print(f'MAE for model {model} : {mae.round(3)}')
        print(f'MdAE for model {model} : {mdae.round(3)}')
        print(f'MdAPE for model {model} : {mdape.round(3)}')


def train_model_by_ozon_postings(products: list[OzonProduct], postings: list[OzonPosting]) -> (CatBoostRegressor, list):
    def prepare_data(_postings: list[OzonPosting]):
        raw_data = []
        for product in products:
            # find all posting with this product
            p_postings = [p for p in _postings if any(o.vendor_code == product.vendor_code for o in p.orders)]

            if len(p_postings) == 0:
                continue

            # find min date
            min_date = min([p.processTo for p in p_postings])
            # find max date
            max_date = max([p.processTo for p in p_postings])

            # between min and max date
            for day in range(0, (max_date - min_date).days):
                _day = min_date + timedelta(days=day)

                # for hour in range(0, 24):
                    # find posting in this day and hour
                p_posting = next((p for p in p_postings if p.processTo.day == _day.day and p.processTo.month == _day.month), None)

                quantity = 0
                if p_posting is not None:
                    # find order in posting
                    o_product = next((o for o in p_posting.orders if o.vendor_code == product.vendor_code), None)
                    if o_product is not None:
                        quantity = o_product.quantity

                # Продано за вчера, за 3 дня назад, за 7 дней назад
                sales_days = [0, 0, 0]

                # calc sales
                for _p in p_postings:
                    # find all orders in this posting with processTo between _day - 1 and _day
                    if _day.day - 1 <= _p.processTo.day < _day.day and _p.processTo.month == _day.month:
                        sales_days[0] += sum([o.quantity for o in _p.orders if o.vendor_code == product.vendor_code])
                    # find all orders in this posting with processTo between _day - 3 and _day
                    if _day.day - 3 <= _p.processTo.day < _day.day and _p.processTo.month == _day.month:
                        sales_days[1] += sum([o.quantity for o in _p.orders if o.vendor_code == product.vendor_code])
                    # find all orders in this posting with processTo between _day - 7 and _day
                    if _day.day - 7 <= _p.processTo.day < _day.day and _p.processTo.month == _day.month:
                        sales_days[2] += sum([o.quantity for o in _p.orders if o.vendor_code == product.vendor_code])

                raw_data.append({
                    'price': product.price,
                    'vendor_code': product.vendor_code,
                    'quantity': quantity,
                    'sales_days_0': sales_days[0],
                    'sales_days_1': sales_days[1],
                    'sales_days_2': sales_days[2],
                    'month': _day.month,
                    'day_of_week': _day.weekday(),
                    # 'hour': hour,
                })

        return raw_data

    last_date = max([p.processTo for p in postings])
    train_data = prepare_data([p for p in postings if p.processTo < last_date - timedelta(days=7)])
    test_data = prepare_data([p for p in postings if p.processTo >= last_date - timedelta(days=7)])

    model = CatBoostRegressor(iterations=int(len(train_data)), learning_rate=0.05, depth=12, loss_function='RMSE')
    data = pd.DataFrame(train_data)
    print(data)
    x_train = data.drop(['quantity', 'vendor_code'], axis=1)
    y_train = data.get('quantity')
    model.fit(x_train, y_train.values)

    x_test = pd.DataFrame(test_data).drop(['quantity', 'vendor_code'], axis=1)
    y_test = pd.DataFrame(test_data).get('quantity')

    result = model.predict(x_test)

    calculate_metrics(y_test, result, 'CatBoostRegressor')

    # covert to list[dict[vendor_code, quantity]]
    predicts = []
    for idx, predict in enumerate(result):
        predicts.append({
            'vendor_code': test_data[idx]['vendor_code'],
            'predict': predict,
            'actual': y_test[idx]
        })

    # sum by vendor_code
    predicts = pd.DataFrame(predicts).groupby(['vendor_code']).sum().reset_index().to_dict('records')

    return model, predicts
