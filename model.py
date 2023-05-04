import streamlit as st
import numpy as np
import datetime
import yfinance as yf
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from currency import get_prediction
import warnings

warnings.filterwarnings('ignore')

def predict():
    base = st.sidebar.selectbox('Choose currency pair', ['USD', 'GBP', 'EUR'])
    target = st.sidebar.selectbox('Choose another currency pair', ['EUR', 'GBP', 'USD'])
    if base == target:
        st.error('Application Error!')
        return None
    symbol= f'{base}{target}=X'
    if st.sidebar.button('Accept'):
        data = download_data(symbol)
        st.sidebar.success('Data Downloaded!')
        model_engine(data, symbol)

@st.cache_resource
def download_data(symbol):
    df = yf.download(symbol, start='2008-01-01', end=datetime.date.today(), progress=False)
    return df




def model_engine(df, symbol):
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

    data['next_day_price'] = data.Close.shift(-1)
    data = data.dropna()

    scaler = StandardScaler()

    features = data.drop(['Close', 'next_day_price'], axis=True)
    target = data['next_day_price']
    features = scaler.fit_transform(features)

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=.2, random_state=0)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    score = r2_score(y_test, preds) * 100
    st.header('Currency Rate Prediction')
    st.write(f'Model Accuracy: {round(score)}%')
    get_prediction(model, df)
