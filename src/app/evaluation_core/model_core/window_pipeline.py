import pandas as pd
from src.app.evaluation_core.model_core.window_generator import WindowGenerator

def data_init(filepath: str, columns_dropped: list[str] | None) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df.drop(columns=columns_dropped, inplace=True)
    return df

def data_split(df):
    n = len(df)
    train_df = df[0 : int(n * 0.7)]
    val_df = df[int(n * 0.7) : int(n * 0.9)]
    test_df = df[int(n * 0.9) :]

    return train_df, val_df, test_df

def data_normalization(train_df, val_df, test_df):
    train_mean = train_df.mean()
    train_std = train_df.std()

    train_df = (train_df - train_mean) / train_std
    val_df = (val_df - train_mean) / train_std
    test_df = (test_df - train_mean) / train_std

    return train_df, val_df, test_df

def data_processing(df):
    train_df, val_df, test_df = data_split(df)
    train_df, val_df, test_df = data_normalization(train_df, val_df, test_df)
    
    return WindowGenerator(input_width=30,
                            label_width=1,
                            shift=1,
                            train_df=train_df,
                            val_df=val_df,
                            test_df=test_df,
                            label_columns=["Close"])
