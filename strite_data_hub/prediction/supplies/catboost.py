from catboost import CatBoostRegressor
import pandas as pd


class SuppliesCatBoost:

    def __init__(self, data: list):
        self.model = CatBoostRegressor()
        self.data = pd.DataFrame(data)
        print(self.data)

    def train(self):
        # remove key log_sales_total in data
        x_train = self.data.drop(['log_sales_total', 'vendor_code', 'warehouse'], axis=1)
        y_train = self.data.get('log_sales_total')
        self.model.fit(x_train, y_train.values)

    def predict(self, data: list):
        return self.model.predict(pd.DataFrame(data).drop(['vendor_code'], axis=1))

    def save(self, path: str):
        self.model.save_model(path)

    def load(self, path: str):
        self.model.load_model(path)


def get_prediction(data: list, predict: list, path: str = None) -> list:
    model = SuppliesCatBoost(data)
    if path is None:
        model.train()
        model.save('model.cbm')
    else:
        model.load(path)
    return model.predict(predict)