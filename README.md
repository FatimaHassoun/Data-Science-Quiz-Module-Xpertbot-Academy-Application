# Internship Project Summary - Quiz Module - XpertBot Academy Application
**Role: Data Scientist**
---

**Project: Quiz Module- XpertBot Academy Application**
---
A quiz management system built with Streamlit. This application provides both administrative and user dashboard interfaces for managing and monitoring multiple-choice quiz data across various tracks.

## 🚀 Features

### Admin Dashboard (`quiz-dashboard.py`)

- **Question Management**: Add, edit, and search quiz questions
- **Multi-track Support**: Organize questions by different educational tracks
- **Visual Analytics**: Interactive charts showing question distribution and performance metrics
- **Data Persistence**: CSV-based storage for questions and answers
- **Real-time Search**: Find and edit questions by keyword

### User Dashboard (`user-dashboard.py`)

- **Live User Monitoring**: Track online users and their performance
- **Performance Analytics**: View average scores by track
- **User Statistics**: Monitor user engagement across different tracks
- **Data Visualization**: Interactive charts for user metrics

## 📊 Data Structure

The system manages quiz data with the following structure:

- **Track**: Educational category (Cybersecurity, Data Science, Mobile Development)
- **Question**: The quiz question text
- **Options**: Up to 4 multiple-choice options
- **Correct Answer**: The correct option
- **Mark**: Point value for the question
- **Time**: Time limit in seconds

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd quiz-module-xpertbot-academy-data-science
   ```

2. **Install required dependencies**:

   ```bash
   pip install streamlit pandas plotly numpy
   ```

3. **Run the Admin Dashboard**:

   ```bash
   streamlit run quiz-dashboard.py
   ```

4. **Run the User Dashboard** (in a separate terminal):
   ```bash
   streamlit run user-dashboard.py
   ```

## 🎯 Usage

### Admin Dashboard

1. **Adding Questions**: Use the sidebar form to add new quiz questions
2. **Editing Questions**: Search for existing questions and click "Edit Selected Question"
3. **Viewing Analytics**: Monitor question distribution and performance metrics
4. **Data Management**: All changes are automatically saved to `output.csv`

### User Dashboard

1. **Monitor Online Users**: View real-time count of active users
2. **Track Performance**: Analyze average scores by educational track
3. **User Analytics**: Review user engagement patterns
4. **Data Overview**: Browse user data samples

## 🔧 Configuration

### Customizing Tracks

Edit the `TRACKS` list in `user-dashboard.py` to modify available educational tracks:

```python
TRACKS = ["Web Development", "Data Science", "Mobile Development", "Project Management", "Cybersecurity", "Quality Assurance"]
```

## 📋 Requirements

- Python 3.7+
- Streamlit
- Pandas
- Plotly Express
- NumPy

## 🎨 Features in Detail

### Data Visualization

- **Bar Charts**: Question distribution by track
- **Scatter Plots**: Marks vs. time analysis
- **Interactive Charts**: Hover data and filtering
