import streamlit as st
import pandas as pd
import joblib

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Flight Fare Prediction",
    page_icon="✈️",
    layout="wide"
)

# --------------------------------------------------
# Load Model
# --------------------------------------------------
model = joblib.load("flight_fare_model.pkl")
# --------------------------------------------------
# Prediction History
# --------------------------------------------------

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    color: #aeb4c0;
    margin-bottom: 35px;
}

.input-card {
    background: #f8f9fa;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #e5e5e5;
}

.result-card {
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    background: #eef7ff;
    border: 1px solid #cfe8ff;
    margin-top: 25px;
}

.result-label {
    font-size: 17px;
    color: #374151;
}

.result-price {
    font-size: 36px;
    font-weight: 700;
    margin-top: 8px;
    color: #1f2937;
}
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    font-weight: 600;
    font-size: 15px;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] > div > div {
    border-radius: 10px;
}

div[data-testid="stSelectbox"] > div > div:focus-within,
div[data-testid="stNumberInput"] > div > div:focus-within {
    border-color: #6c8cff;
    box-shadow: 0 0 0 1px #6c8cff;
}
/* Predict Button */
div.stButton > button[kind="primary"] {
    background: #4f7cff;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-size: 17px;
    font-weight: 600;
    transition: 0.2s;
}

div.stButton > button[kind="primary"]:hover {
    background: #3b68e8;
    color: white;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">✈️ Flight Fare Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Predict the estimated flight fare using machine learning</div>',
    unsafe_allow_html=True
)
def reset_inputs():
    st.session_state["airline"] = "AirAsia"
    st.session_state["source_city"] = "Bangalore"
    st.session_state["departure_time"] = "Early_Morning"
    st.session_state["stops"] = "zero"
    st.session_state["arrival_time"] = "Early_Morning"
    st.session_state["destination_city"] = "Bangalore"
    st.session_state["flight_class"] = "Economy"
    st.session_state["duration"] = 2.0
    st.session_state["days_left"] = 10
    st.session_state.prediction_history = []

# --------------------------------------------------
# Input Section
# --------------------------------------------------

st.markdown("### 🛫 Enter Flight Details")

col1, col2 = st.columns(2)

with col1:

    airline = st.selectbox(
        "Airline",
        ["AirAsia", "Air_India", "GO_FIRST", "Indigo", "SpiceJet", "Vistara"],
        key="airline"
    )

    source_city = st.selectbox(
        "Source City",
        ["Bangalore", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"],
        key="source_city"
    )

    departure_time = st.selectbox(
        "Departure Time",
        ["Early_Morning", "Morning", "Afternoon",
         "Evening", "Night", "Late_Night"],
        key="departure_time"
    )

    stops = st.selectbox(
        "Stops",
        ["zero", "one", "two_or_more"],
        key="stops"
    )

    duration = st.number_input(
    "Duration (hours)",
    min_value=0.5,
    max_value=50.0,
    step=0.1,
    key="duration"
)

with col2:

    arrival_time = st.selectbox(
        "Arrival Time",
        ["Early_Morning", "Morning", "Afternoon",
         "Evening", "Night", "Late_Night"],
        key="arrival_time"
    )

    destination_city = st.selectbox(
        "Destination City",
        ["Bangalore", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"],
        key="destination_city"
    )

    flight_class = st.selectbox(
        "Class",
        ["Economy", "Business"],
        key="flight_class"
    )

    days_left = st.number_input(
        "Days Left",
        min_value=1,
        max_value=49,
        value=10,
        step=1,
        key="days_left"
    )

# --------------------------------------------------
# Prediction
# --------------------------------------------------

st.markdown("---")

predict_col1, predict_col2, predict_col3 = st.columns([1, 2, 1])

with predict_col2:

    predict_button = st.button(
    "✈️ Predict Flight Fare",
    use_container_width=True,
    type="primary"
)
    reset_button = st.button(
        "🔄 Reset",
        use_container_width=True,
        on_click=reset_inputs
    )

if predict_button:

    input_data = pd.DataFrame([{
        "airline": airline,
        "source_city": source_city,
        "departure_time": departure_time,
        "stops": stops,
        "arrival_time": arrival_time,
        "destination_city": destination_city,
        "class": flight_class,
        "duration": duration,
        "days_left": days_left
    }])

    prediction = model.predict(input_data)[0]
    st.session_state.prediction_history.append({
    "Airline": airline,
    "From": source_city,
    "To": destination_city,
    "Class": flight_class,
    "Duration": duration,
    "Days Left": days_left,
    "Predicted Fare": f"₹{prediction:,.2f}"
})

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">
                Estimated Flight Fare
            </div>
            <div class="result-price">
                ₹{prediction:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# Prediction History
# --------------------------------------------------

if st.session_state.prediction_history:

    st.markdown("---")
    st.markdown("### 📋 Prediction History")

    history_df = pd.DataFrame(st.session_state.prediction_history)

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.prediction_history = []
        st.rerun()

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#9ca3af; padding:15px 0 5px 0;">
        <div style="font-size:15px; font-weight:600;">
            ✈️ Flight Fare Prediction
        </div>
        <div style="font-size:13px; margin-top:5px;">
            Machine Learning Project | Random Forest Regression
        </div>
        <div style="font-size:12px; margin-top:8px;">
            Predict estimated flight fares based on travel details
        </div>
    </div>
    """,
    unsafe_allow_html=True
)