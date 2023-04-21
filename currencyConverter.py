import streamlit as st
import requests


def currency_converter():
    st.header('Currency Converter')
    key = st.text_input('Enter your API key')
    return get_country_code(key)





def get_country_code(key):
    url = f'https://v6.exchangerate-api.com/v6/{key}/codes'
    res = requests.get(url).json()
    country = res['supported_codes']

    code = []
    for i in country:
        code.append(i[0])

    base = st.selectbox('Enter the base currency', code)
    target = st.selectbox('Enter the target currency', code)
    amount = st.number_input('Enter the amount')
    if st.button('Convert'):
        converter(base, target, amount, key)



def converter(base, target, amount, key):
    url = f'https://v6.exchangerate-api.com/v6/{key}/pair/{base}/{target}/{amount}'
    res = requests.get(url).json()
    base_code = res['base_code']
    target_code = res['target_code']
    rate = res['conversion_rate']
    result = res['conversion_result']
    st.text(f'Base_currency: {base_code} \
     \nTarget Currency: {target_code} \
     \nConversion Rate: {rate} \
     \nConversion Amount: {result}')
