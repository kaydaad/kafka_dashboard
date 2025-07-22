Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import streamlit as st
... from confluent_kafka import Consumer
... import pandas as pd
... import json
... from collections import Counter
... import time
... 
... # Kafka Config
... conf = {
...     'bootstrap.servers': 'pkc-rgm37.us-west-2.aws.confluent.cloud:9092',
...     'security.protocol': 'SASL_SSL',
...     'sasl.mechanisms': 'PLAIN',
...     'sasl.username': 'G4PUVCL67RQ6FYIP',
...     'sasl.password': 'VaVJ1RVPIcWiUUQW/T6uBWq5f6tdLzn6hMBgsxXiZzC7VmLkcwIh1buO9QfbAVa9',
...     'group.id': 'streamlit-dashboard',
...     'auto.offset.reset': 'earliest'
... }
... 
... topic = 'customer-support-events'
... 
... st.set_page_config(page_title="Customer Support Dashboard", layout="wide")
... st.title("📊 Customer Support Events Dashboard")
... 
... placeholder = st.empty()
... 
... sentiment_counter = Counter()
... consumer = Consumer(conf)
... consumer.subscribe([topic])
... 
... data = []
... 
... while True:
...     msg = consumer.poll(1.0)
...     if msg is None:
...         continue
...     if msg.error():
...         st.error(f"Error: {msg.error()}")
...         continue
... 
...     record = json.loads(msg.value().decode('utf-8'))
...     data.append(record)
...     sentiment = record.get("sentiment", "unknown")
...     sentiment_counter[sentiment] += 1
... 
...     df = pd.DataFrame(data)
... 
...     with placeholder.container():
...         st.subheader("Latest 10 Messages")
...         st.write(df.tail(10))
... 
...         st.subheader("Sentiment Distribution")
        st.bar_chart(pd.Series(sentiment_counter))

    time.sleep(1)

consumer.close()
