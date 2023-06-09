import streamlit as st
from currencyConverter import currency_converter
from model import predict


def main():
    st.sidebar.header('Currency Converter and Predictor App')
    op = st.sidebar.selectbox('Select an option', ['convert', 'predict'])
    if op == 'convert':
        currency_converter()
    else:
        predict()






if __name__ == '__main__':
    main()
