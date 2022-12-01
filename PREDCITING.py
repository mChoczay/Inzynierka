import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import load_model
from tensorflow import keras
import pandas as pd
import random as rd

csv_path = "data\DataBaseForML.csv"
df = pd.read_csv(csv_path)


feature_keys = [
    "date_time",
    "time (s)",
    "int",
    "temp (degC)",
    "rh (%)",
    "lumen1 (nm)",
    "lumen2 (nm)",

]

date_time_key = "Date Time"

split_fraction = 0.75
train_split = int(split_fraction * int(df.shape[0]))

def normalize(data, train_split):
    global data_mean
    global data_std
    data_mean = data[:train_split].mean(axis=0)
    data_std = data[:train_split].std(axis=0)
    return (data - data_mean) / data_std

def create_data(loaded_data,feature_keys=feature_keys,split_fraction=split_fraction,train_split=train_split,df=df):
    date_time_key = "Date Time"
    split_fraction = 0.75
    train_split = int(split_fraction * int(df.shape[0]))
    step = 10
    past = 600
    future = 6
    batch_size = 128



    selected_features = [feature_keys[i] for i in [3, 4, 5, 6]]
    features = df[selected_features]
    a,b,c = float(rd.randint(19,21)),float(rd.randint(38,42)),float(rd.randint(400,500))
    df2 = pd.DataFrame([[a,b,loaded_data,c]], columns=['temp (degC)','rh (%)','lumen1 (nm)','lumen2 (nm)'])
    df = pd.concat([df2, df])
    features = df[selected_features]

    features.index = df[date_time_key]
    features.head()

    features = normalize(features.values, train_split)
    features = pd.DataFrame(features)
    features.head()

    train_data = features.loc[0 : train_split - 1]
    val_data = features.loc[train_split:]

    start = past + future
    end = start + train_split

    x_train = train_data[[i for i in range(4)]].values
    y_train = features.iloc[start:end][[1]]

    sequence_length = int(past / step)

    dataset_train = keras.preprocessing.timeseries_dataset_from_array(
        x_train,
        y_train,
        sequence_length=sequence_length,
        sampling_rate=step,
        batch_size=batch_size,
    )

    x_end = len(val_data) - past - future

    label_start = train_split + past + future

    x_val = val_data.iloc[:x_end][[i for i in range(4)]].values
    y_val = features.iloc[label_start:][[1]]

    dataset_val = keras.preprocessing.timeseries_dataset_from_array(
        x_val,
        y_val,
        sequence_length=sequence_length,
        sampling_rate=step,
        batch_size=batch_size,
    )
    pred = prediction(dataset_val)
    return pred[2]


def prediction(dataset_val):
    model = load_model('data/Best_model.h5')
    for x, y in dataset_val.take(1):
        out = model.predict(x)[2]
        denorm = out*data_std + data_mean
    return(denorm)

