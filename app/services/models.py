from typing import List

import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import tensorflow as tf

from app.models.payloads import (StockPredictionPayload,
                                             payload_to_list)
from app.models.predictions import StockPredictionResult


class StockPredictionModel(object):

    def __init__(self, path):
        self.path = path
        self._load_local_model()

        # hyper params
        self._input_data_column_cnt = 6   # columns of input data
        self._output_data_column_cnt = 1  # columns of output data

        self._seq_length = 28             # length of sequence
        self._rnn_cell_hidden_dim = 20    # hidden dimensions of cell 
        self._forget_bias = 1.0           # forget bias 
        self._num_stacked_layers = 1      # stacked LSTM layers
        self._keep_prob = 1.0             # dropout ratio

        self._epoch_num = 1000            # epochs
        self._learning_rate = 0.01        # learning rate

    def _load_local_model(self):
        self.model = joblib.load(self.path)

    def _data_standardize(self, x):
        x_np = np.asarray(x)
        return (x_np - x_np.mean()) / x_np.std()
 
    def _min_max_scale(self, x):
        x_np = np.asarray(x)
        return (x_np - x_np.min()) / (x_np.max() - x_np.min() + 1e-7) # 1e-7은 0으로 나누는 오류 예방차원
    
    def _reverse_min_max_scale(self, org_x, x):
        org_x_np = np.asarray(org_x)
        x_np = np.asarray(x)
        return (x_np * (org_x_np.max() - org_x_np.min() + 1e-7)) + org_x_np.min()

    def _data_load(self, ):
        stock_fn = "blah.csv"
        encoding = "euc-kr"
        names = ['Date','Open','High','Low','Close','Adj Close','Volume']

        raw_data_frame = pd.read_csv(stock_fn, names = names, encoding = encoding)

        raw_data_frame.drop("Date", axis = 1, inplace = True)   # drop date column

        stock_info = raw_data_frame.values[1:].astype(np.float) # convert price, volume to float

        price = stock_info[:, :-1]
        norm_price = self._min_max_scale(price)

        # 거래량형태 데이터를 정규화한다
        # ['Open','High','Low','Close','Adj Close','Volume']에서 마지막 'Volume'만 취함
        # [:,-1]이 아닌 [:,-1:]이므로 주의하자! 스칼라가아닌 벡터값 산출해야만 쉽게 병합 가능
        volume = stock_info[:, -1:]
        norm_volue = self._min_max_scale(volume)

        x = np.concatenate((norm_price, norm_volume), axis = 1)  # axis  = 1, 세로로 concatenate

        y = x[:, [-2]] # target: close

        dataX = [] # 입력으로 사용할 Sequence data
        dataY = [] # 출력으로 사용 (target)
        

        return data

    def _preprocess(self, payload: StockPredictionPayload) -> List:
        logger.debug("Pre-processing payload.")



        result = np.asarray(payload_to_list(payload)).reshape(1, -1)
        return result

    def _postprocess(self, prediction: np.ndarray) -> StockPredictionResult:
        logger.debug("Post-processing prediction.")
        result = prediction.tolist()
        human_readable_unit = result[0] * self.RESULT_UNIT_FACTOR
        hpp = StockPredictionResult(median_house_value=human_readable_unit)
        return hpp

    def train():
        return ""

    def _predict(self, features: List) -> np.ndarray:
        logger.debug("Predicting.")
        prediction_result = self.model.predict(features)
        return prediction_result

    def predict(self, payload: StockPredictionPayloads):
        if payload is None:
            raise ValueError(NO_VALID_PAYLOAD.format(payload))

        pre_processed_payload = self._pre_process(payload)
        prediction = self._predict(pre_processed_payload)
        logger.info(prediction)
        post_processed_result = self._post_process(prediction)

        return post_processed_result