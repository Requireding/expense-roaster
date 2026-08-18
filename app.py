import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import google.generativeai as genai
import os
import random
from dotenv import load_dotenv

load_dotenv()


#CONFIGURATION & SETUP

st.set_page_config(page_title="The Expense Roaster", page_icon="🔥", layout="wide")

# Initialize Session State Variables 
if "expense_data" not in st.session_state:
    st.session_state.expense_data = None
if "roast_result" not in st.session_state:
    st.session_state.roast_result = None

# Sidebar Setup
st.sidebar.title("🔥 The Expense Roaster")
st.sidebar.markdown("Upload your monthly expenses and let AI brutally audit your life choices.")

# PRIVATE API KEY: 
api_key = os.getenv("GEMINI_API_KEY")

@st.cache_resource
def init_gemini(key):
    genai.configure(api_key=key)
    return genai.GenerativeModel('gemini-2.5-flash')


# We inject custom CSS to style the Streamlit elements and add hover animations.
st.markdown("""
<style>
    /* Create a gradient text effect for the main title */
    .custom-title {
        background: -webkit-linear-gradient(45deg, #ff4b4b, #ff904f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0px;
        padding-bottom: 10px;
        cursor: pointer;
    }
    
    /* Glassmorphism styling for the KPI metric cards */
    [data-testid="stMetric"] {
        background: rgba(255, 75, 75, 0.05);
        border: 1px solid rgba(255, 75, 75, 0.2);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease-in-out;
    }
    
    /* Make the cards float up when the mouse hovers over them */
    [data-testid="stMetric"]:hover {
        transform: translateY(-8px);
        border: 1px solid rgba(255, 75, 75, 0.6);
        box-shadow: 0 8px 25px rgba(255, 75, 75, 0.2);
    }
    
    /* Style the submit button to look more aggressive */
    [data-testid="baseButton-secondaryFormSubmit"] {
        background-color: #ff4b4b;
        color: white;
        border: none;
        transition: 0.3s;
    }
    [data-testid="baseButton-secondaryFormSubmit"]:hover {
        background-color: #ff2b2b;
        transform: scale(1.02);
    }
</style>

<!-- Custom HTML Title with inline JavaScript -->
<div class="custom-title" onclick="alert('System Initialized: Prepare your wallet for a roasting.')">
    💸 The Expense Roaster Dashboard
</div>
<hr style="border: 1px solid rgba(255,75,75,0.2); margin-top: 0px;">
<script>
    // A little JavaScript running in the background console
    console.log("Expense Roaster Custom UI loaded successfully!");
</script>
""", unsafe_allow_html=True)



#DYNAMIC MOCK DATA PIPELINE

def generate_mock_data():
    """Generates a Pandas DataFrame with at least 12 randomized but highly specific spending habits."""
    
    food_merchants = ["Swiggy", "Zepto", "Zomato"]
    food_items = ["Late night biryani", "Late night ice cream & chips", "Pizza combo", "Red Bull & Maggi", "Late night momos"]
    
    skincare_merchants = ["Minimalist", "The Ordinary", "Chemist At Play", "The Derma Co", "DERMATOUCH"]
    skincare_items = ["Salicylic Acid 2%", "Glycolic Acid Toner", "Hyaluronic Acid Serum", "Daily Moisturizer"]
    
    travel_items = ["3A Train Ticket", "SL Train Ticket", "3E Train Ticket"]
    
    data = {"Date": [], "Time": [], "Category": [], "Merchant": [], "Description": [], "Amount (INR)": []}
    
    # Generate 14 random transactions to easily surpass the "at least 10" requirement
    for _ in range(14):
        # Generate a random date in August 2026
        random_day = random.randint(1, 20)
        random_date = f"2026-08-{random_day:02d}"
        
        # Weighted random choice:
        category = random.choices(
            ["Food Delivery", "Skincare", "Travel", "Tech/Appliances"], 
            weights=[7, 3, 2, 2], k=1
        )[0]
        
        if category == "Food Delivery":
            # Late night hours
            random_time = f"0{random.randint(0, 4)}:{random.randint(10, 59)}"
            merchant = random.choice(food_merchants)
            desc = random.choice(food_items)
            amt = random.randint(150, 850)
            
        elif category == "Skincare":
            # Normal daytime hours
            random_time = f"{random.randint(10, 22)}:{random.randint(10, 59)}"
            merchant = random.choice(skincare_merchants)
            desc = random.choice(skincare_items)
            amt = random.randint(399, 1499)
            
        elif category == "Travel":
            random_time = f"{random.randint(8, 20)}:{random.randint(10, 59)}"
            merchant = "IRCTC"
            desc = random.choice(travel_items)
            amt = random.randint(450, 2100)
            
        else: 
            # Tech or general splurges
            random_time = f"{random.randint(12, 18)}:{random.randint(10, 59)}"
            splurges = [
                ("Samsung Store", "Galaxy Watch7", 29999),
                ("Havells Store", "Avanza Air Fryer Oven", 6500),
                ("ASI", "Archaeological Survey e-Ticket", 50),
                ("Anytime Fitness", "Gym Pre-workout & Gear", 1200)
            ]
            merchant, desc, amt = random.choice(splurges)

        # Append to our data dictionary
        data["Date"].append(random_date)
        data["Time"].append(random_time)
        data["Category"].append(category)
        data["Merchant"].append(merchant)
        data["Description"].append(desc)
        data["Amount (INR)"].append(amt)
        
    
    df = pd.DataFrame(data)
    df = df.sort_values(by="Date").reset_index(drop=True)
    
    return df


# MAIN DASHBOARD & UI/UX

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Step 1: Load Data")
    uploaded_file = st.file_uploader("Upload Expense CSV", type=["csv"])
    
    if st.button("🎲 Generate Mock Expenses"):
        st.session_state.expense_data = generate_mock_data()
        st.success("Mock data loaded successfully!")
        
    if uploaded_file is not None:
        st.session_state.expense_data = pd.read_csv(uploaded_file)

with col2:
    st.markdown("### Step 2: Data Visualization")
    if st.session_state.expense_data is not None:
        df = st.session_state.expense_data
        
        # Dynamic API Cards
        total_spent = df["Amount (INR)"].sum()
        tech_spent = df[df["Category"] == "Tech/Appliances"]["Amount (INR)"].sum()
        food_spent = df[df["Category"] == "Food Delivery"]["Amount (INR)"].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Monthly Spend", f"₹{total_spent:,}")
        m2.metric("Tech Splurges", f"₹{tech_spent:,}", delta="Critical", delta_color="inverse")
        m3.metric("Late-Night Delivery", f"₹{food_spent:,}", delta="High", delta_color="inverse")
        
        # Interactive Data Editor & Chart
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df, x="Category", y="Amount (INR)", color="#ff4b4b")
    else:
        st.info("Awaiting data upload or generation...")



#AI INTEGRATION & THE ROAST

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("### Step 3: The Financial Audit")


with st.form("roast_form"):
    st.markdown("Are you ready to face the music?")
    submit_button = st.form_submit_button("🔥 Roast My Wallet")
    
    if submit_button:
        if not api_key:
            st.error("System Error: Gemini API Key is missing. Please ensure your .env file is configured correctly.")
        elif st.session_state.expense_data is None:
            st.error("Please load some expense data first.")
        else:
            try:
                model = init_gemini(api_key)
                df_csv = st.session_state.expense_data.to_csv(index=False)
                
                # Prompt
                system_prompt = f"""
                You are a ruthless, highly sarcastic financial advisor. I am providing you with a CSV of my monthly expenses.
                
                Your task:
                1. Analyze the data and BRUTALLY roast my discretionary spending. Call out specific habits (like ordering food between 12 AM and 5 AM, spending on premium skincare, or blowing money on gadgets and air fryers).
                2. Provide a strict, 3-step budget recovery plan to stop this financial bleeding.
                3. Format your response beautifully using Markdown headings, bullet points, and bold text.
                
                Here is the CSV data:
                {df_csv}
                """
                
                with st.spinner("Analyzing your terrible financial decisions..."):
                    response = model.generate_content(system_prompt)
                    st.session_state.roast_result = response.text
            except Exception as e:
                st.toast(f"API Error: {e}")
                st.error(f"The API request failed: {e}")

# Display the roast
if st.session_state.roast_result:
    with st.expander("🔥 Your Financial Audit Results", expanded=True):
        st.markdown(st.session_state.roast_result)