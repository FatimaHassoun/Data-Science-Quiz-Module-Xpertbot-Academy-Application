import streamlit as st
import pandas as pd
import numpy as np
import os

DATA_FILE = "user_data.csv"
TRACKS = ["Web Development", "Data Science", "Mobile Development", "Project Management", "Cybersecurity", "Quality Assurance"]
NUM_USERS = 200
def simulate_data(num_users=NUM_USERS, tracks=TRACKS):
    np.random.seed(42)
    user_ids = [f"user_{i:03d}" for i in range(1, num_users+1)]
    track_choices = np.random.choice(tracks, size=num_users, p=[1/6,1/6,1/6,1/6, 1/6, 1/6])
    scores = np.round(np.random.normal(loc=70, scale=15, size=num_users).clip(0,100), 1)
    online = np.random.choice([True, False], size=num_users, p=[0.3,0.7])
    df = pd.DataFrame({
        "user_id": user_ids,
        "track": track_choices,
        "score": scores,
        "online": online
    })
    df.to_csv(DATA_FILE, index=False)
    return df

if not os.path.exists(DATA_FILE):
    df = simulate_data()
else:
    df = pd.read_csv(DATA_FILE)

st.title("📊 Live User Dashboard")
total_online = df.online.sum()
st.metric(label="Users Online", value=int(total_online))

users_per_track = df.groupby('track')['user_id'].count().reset_index()
users_per_track.columns = ['Track', 'User Count']
st.subheader("👥 Users per Track")
st.bar_chart(data=users_per_track.set_index('Track'))

avg_score = df.groupby('track')['score'].mean().reset_index()
avg_score.columns = ['Track', 'Avg Score']
st.subheader("🏆 Average Score per Track")
st.bar_chart(data=avg_score.set_index('Track'))

st.subheader("📄 User Data Sample")
st.dataframe(df.head(50))
