import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import datetime


def get_prediction(model, df):
       data = df[['Close']]
       weekly_mean = data.Close.rolling(7).mean()
       monthly_mean = data.Close.rolling(30).mean()
       quarterly_mean = data.Close.rolling(90).mean()
       yearly_mean = data.Close.rolling(365).mean()

       data['weekly_mean'] = weekly_mean / data.Close
       data['monthly_mean'] = monthly_mean / data.Close
       data['quarterly_mean'] = quarterly_mean / data.Close
       data['yearly_mean'] = yearly_mean / data.Close

       data['yearly_weekly_mean'] = data.yearly_mean / data.weekly_mean
       data['yearly_monthly_mean'] = data.yearly_mean / data.monthly_mean
       data['yearly_quarterly_mean'] = data.yearly_mean / data.quarterly_mean

       data = data.dropna()

       scaler = StandardScaler()

       features = data.drop(['Close'], axis=True)
       features = scaler.fit_transform(features)

       data['predicted_rate'] = model.predict(features)
       data['signal'] = np.where(data.predicted_rate.shift(1) < data.predicted_rate,"Buy","No Position")

       prediction = data.tail(1)[['signal','predicted_rate']].T
       st.write('Current Rate')
       st.dataframe(data.Close.tail(1))
       st.write('Next Day Predicted Rate')
       st.dataframe(prediction)

