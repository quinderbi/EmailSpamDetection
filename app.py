import streamlit as st
from getEndPoint import call_endpoint
from getEndPoint import preprocess_data

st.title('Email Spam Detection App')

message = st.text_area('Enter a message')

if st.button('Submit'):
    message = preprocess_data(message)
    response = call_endpoint(message)
    if response:
        if response.decode('utf-8') == '["ham"]':
            st.write('The message is not spam')
        else:
            st.write('The message is spam')
    else:
        st.write('Something went wrong')
    