```text
      .-------------.__   Requireding@GITHUB
     /             / |    --------------------
    /             /  |    Project: .... The Expense Roaster (Capstone)
   /____________ /   |    Uptime: ..... 21 years, 0 months
   | ___________ |   |    Kernel: ..... MirAI summer internship | IBM SkillBuild Mentee
   | |         | |   |    Location: ... Greater Noida, Uttar Pradesh, India
   | | >_      | |   |    Tech Stack: . Streamlit, Pandas, Gemini 2.5 API
   | |_________| |  /     Focus: ...... FinTech, Data Pipelines, AI Prompting
   |_____________| /      Live App: ... https://expense-roaster-a.streamlit.app/

💸 The Expense Roaster (Capstone Project)
This repository contains the source code for my final AI Builder Track Capstone Project. It is a highly interactive dashboard that allows users to upload a CSV of their monthly expenses. The app visualizes the data using pandas and st.bar_chart, and then pipes the CSV string to the Gemini API using advanced system prompts to brutally roast the user's discretionary spending habits.

🚀 Live Deployment
You can access the live application here: https://expense-roaster-a.streamlit.app/

🏗️ Architecture & Technical Implementation
Memory Management: Utilizes st.session_state to prevent API data loss upon UI re-renders.

API Optimization: Employs st.form to batch user inputs and prevent unnecessary calls to the Gemini LLM.

Data Processing: Leverages native pandas DataFrames to structure mock CSV inputs and generate dynamic KPI delta metrics via st.metric.

Custom UI/UX: Injects native HTML, CSS (Glassmorphism), and a background JavaScript clock engine via streamlit.components.v1 to bypass standard frontend limitations.

⚙️ Local Setup Instructions
Clone the repository:

Bash
git clone [https://github.com/Requireding/expense-roaster.git](https://github.com/Requireding/expense-roaster.git)
Install the dependencies:

Bash
pip install -r requirements.txt
Secure your API Key:

Create a .env file in the root directory.

Add your key: GEMINI_API_KEY="your_actual_key_here"

Run the server:

Bash
streamlit run app.py
