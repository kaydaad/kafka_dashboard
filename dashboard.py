import streamlit as st
from confluent_kafka import Consumer
import pandas as pd
import json
from collections import Counter
import time

# Load secrets from Streamlit's Secrets Manager
conf = {
    'bootstrap.servers': st.secrets["BOOTSTRAP_SERVERS"],
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': st.secrets["SASL_USERNAME"],
    'sasl.password': st.secrets["SASL_PASSWORD"],
    'group.id': 'streamlit-consumer',
    'auto.offset.reset': 'latest'
}

topic = st.secrets["TOPIC"]
consumer = Consumer(conf)
consumer.subscribe([topic])

st.set_page_config(page_title="Customer Support Dashboard", layout="wide")
st.title("📊 Customer Support Events Dashboard")

# Session state to persist data across reruns
if "data" not in st.session_state:
    st.session_state.data = []
if "sentiment_counter" not in st.session_state:
    st.session_state.sentiment_counter = Counter()

# Try polling a new message
msg = consumer.poll(timeout=1.0)
if msg is not None and not msg.error():
    try:
        record = json.loads(msg.value().decode("utf-8"))
        st.session_state.data.append(record)
        sentiment = record.get("sentiment", "unknown")
        st.session_state.sentiment_counter[sentiment] += 1
    except Exception as e:
        st.error(f"Error decoding message: {e}")

# Display dashboard
df = pd.DataFrame(st.session_state.data)
st.subheader("Latest 10 Messages")
st.write(df.tail(10))

st.subheader("Sentiment Distribution")
st.bar_chart(pd.Series(st.session_state.sentiment_counter))

# Add refresh control
if st.button("🔄 Refresh"):
    st.session_state.refreshed = True  # Just a placeholder to trigger rerun

# Gracefully close Kafka consumer
consumer.close()

