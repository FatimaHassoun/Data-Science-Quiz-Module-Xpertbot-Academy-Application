import streamlit as st
import pandas as pd
import plotly.express as px
import csv
import os

# Constants
DATA_FILE = "output.csv"

# Session State Keys
OPTIONS_KEY = "options"
EDIT_MODE_KEY = "edit_mode"
EDIT_INDEX_KEY = "edit_index"

def init_session_state():
    if OPTIONS_KEY not in st.session_state:
        st.session_state[OPTIONS_KEY] = {f"opt{i}": "" for i in range(1,5)}
    if EDIT_MODE_KEY not in st.session_state:
        st.session_state[EDIT_MODE_KEY] = False
    if EDIT_INDEX_KEY not in st.session_state:
        st.session_state[EDIT_INDEX_KEY] = -1

@st.cache_data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, quoting=csv.QUOTE_ALL)
    return pd.DataFrame(columns=["track","question","option1","option2","option3",
                                   "option4","correctAnswer","mark","time(seconds)"])

def save_data(df: pd.DataFrame):
    df.to_csv(DATA_FILE, index=False, quoting=csv.QUOTE_ALL)
    st.cache_data.clear()

def search_and_edit(df: pd.DataFrame):
    st.header("🔍 Search & Edit Questions")
    term = st.text_input("Search questions by keyword:")
    if term and not df.empty:
        matches = df[df.question.str.contains(term, case=False, na=False)]
        if not matches.empty:
            pick = st.selectbox("Select question:", matches.question)
            if st.button("Edit Selected Question"):
                idx = df.index[df.question == pick][0]
                st.session_state[EDIT_INDEX_KEY] = idx
                st.session_state[EDIT_MODE_KEY] = True
                row = df.loc[idx]
                # prefill options
                for i in range(1,5):
                    st.session_state[OPTIONS_KEY][f"opt{i}"] = row.get(f"option{i}", "")
        else:
            st.warning("No matching questions found.")

def question_form(df: pd.DataFrame):
    mode = st.session_state[EDIT_MODE_KEY]
    idx = st.session_state[EDIT_INDEX_KEY]
    title = "✏️ Edit Question" if mode else "➕ Add New Question"
    with st.sidebar:
        st.header(title)
        with st.form("q_form", clear_on_submit=True):
            tracks = df.track.unique().tolist() or ["General"]
            track = st.selectbox("Track:", tracks, key="track_input")

            default_q = df.at[idx, 'question'] if mode else ""
            question = st.text_input("Question*:", value=default_q, key="q_input")

            cols = st.columns(4)
            opts = []
            for i, col in enumerate(cols, start=1):
                with col:
                    default_val = st.session_state[OPTIONS_KEY].get(f"opt{i}", "")
                    val = st.text_input(f"Option {i}{'*' if i<3 else ''}", value=default_val, key=f"opt_input_{i}")
                    opts.append(val)
            for i, val in enumerate(opts, start=1):
                st.session_state[OPTIONS_KEY][f"opt{i}"] = val

            choices = [o for o in opts if o]
            if mode:
                default_ans = df.at[idx, 'correctAnswer']
                default_index = choices.index(default_ans) if default_ans in choices else 0
            else:
                default_index = 0
            correct = st.selectbox(
                "Correct Answer*:",
                choices,
                index=default_index,
                disabled=not choices,
                key="correct_input"
            )

            default_mark = float(df.at[idx, 'mark']) if mode else 1.0
            mark = st.number_input("Mark*:", min_value=0.0, value=default_mark, key="mark_input")
            default_time = int(df.at[idx, 'time(seconds)']) if mode else 30
            time_sec = st.number_input("Time (seconds)*:", min_value=1, value=default_time, key="time_input")

            submitted = st.form_submit_button("Save" if mode else "Add")
            if submitted:
                if not question or len(choices) < 2:
                    st.error("Fill in question and at least two options.")
                else:
                    entry = {
                        'track': track,
                        'question': question,
                        'option1': opts[0],
                        'option2': opts[1],
                        'option3': opts[2] if len(opts)>2 else "",
                        'option4': opts[3] if len(opts)>3 else "",
                        'correctAnswer': correct,
                        'mark': mark,
                        'time(seconds)': time_sec
                    }
                    if mode:
                        df.loc[idx] = entry
                        st.success("Question updated!")
                    else:
                        df.loc[len(df)] = entry
                        st.success("Question added!")
                    save_data(df)
                    # reset state
                    st.session_state[EDIT_MODE_KEY] = False
                    st.session_state[EDIT_INDEX_KEY] = -1
                    st.session_state[OPTIONS_KEY] = {f"opt{i}":"" for i in range(1,5)}

def display_questions(df: pd.DataFrame):
    if df.empty:
        return
    st.header("📋 Current Questions")
    st.dataframe(df[['track','question','correctAnswer','mark']])

    st.subheader("📈 Questions by Track")
    counts = df.track.value_counts().reset_index()
    counts.columns = ['track','count']
    fig = px.bar(counts, x='track', y='count', color='track')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("⏱️ Marks vs Time")
    fig2 = px.scatter(df, x='time(seconds)', y='mark', color='track', hover_data=['question'])
    st.plotly_chart(fig2, use_container_width=True)

def main():
    st.title("📚 MCQ Quiz Admin Dashboard")
    init_session_state()
    df = load_data()
    search_and_edit(df)
    question_form(df)
    display_questions(df)

if __name__ == "__main__":
    main()
