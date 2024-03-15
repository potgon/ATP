import pandas as pd
import numpy as np

from src.app.evaluation_core.model_core import baseline, window_generator
from src.app.evaluation_core.model_trainers.lstm_trainer import LSTMTrainer

class LSTMModel:
    def __init__(self, units=50):
        self.LSTMTrainer = LSTMTrainer(window=self.window_init(), units=units)
        self.train_df, self.val_df, self.test_df = self.data_processing(self.data_init())
        self.trained_model = None
        
    def data_init(self) -> pd.DataFrame:
        df = pd.read_csv("data/datasets/SP500_data.csv")
        df.drop("Dividends", axis=1, inplace=True)
        df.drop("Stock Splits", axis=1, inplace=True)
        return df

    def feature_engineering(self, df) -> pd.DataFrame:
        date_time = pd.to_datetime(df.pop("Date"), utc=True)
        df["day_of_week"] = date_time.dt.dayofweek
        df["month_of_year"] = date_time.dt.month
        
        df["day_sin"] = np.sin(df["day_of_week"] * (2 * np.pi / 7))
        df["day_cos"] = np.cos(df["day_of_week"] * (2 * np.pi / 7))
        df["month_sin"] = np.sin((df["month_of_year"] - 1) * (2 * np.pi / 12))
        df["month_cos"] = np.cos((df["month_of_year"] - 1) * (2 * np.pi / 12))
         
        return df
    
    def data_split(self, df):
        n = len(df)
        train_df = df[0:int(n*0.7)]
        val_df = df[int(n*0.7):int(n*0.9)]
        test_df = df[int(n*0.9):]
        
        return train_df, val_df, test_df
    
    def data_normalization(self, df, train_df, val_df, test_df):
        train_mean = train_df.mean()
        train_std = train_df.std()
        
        train_df = (train_df - train_mean) / train_std
        val_df = (val_df - train_mean) / train_std
        test_df = (test_df - train_mean) / train_std

        df_std = (df - train_mean) / train_std
        df_std = df_std.melt(var_name="Column", value_name="Normalized")

        return train_df, val_df, test_df
    
    def data_processing(self, df):
        df = self.feature_engineering(df)
        train_df, val_df, test_df = self.data_split(df)
        train_df, val_df, test_df = self.data_normalization(train_df, val_df, test_df)
        
        return train_df, val_df, test_df
    
    def window_init(self):
        return  window_generator(input_width=30,
                              label_width=1,
                              shift=1,
                              train_df=self.train_df,
                              val_df=self.val_df,
                              test_df=self.test_df,
                              label_columns=["Close"])
        
    def train(self):
        self.trained_model = self.LSTMTrainer.train()
    
    def evaluate(self):
        # Look what does the inner-most evaluate do (print, plot...)
        #self.LSTMTrainer.evaluate()
        pass
    
    def predict(self):
        pass