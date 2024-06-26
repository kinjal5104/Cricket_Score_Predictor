import streamlit as st
import pickle
import pandas as pd

# Load the pre-trained model
model_path = 'pipe.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Define lists for dropdowns
teams = [
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa', 
    'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka'
]

cities = [
    'Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 
    'Cape Town', 'London', 'Pallekele', 'Barbados', 'Sydney', 
    'Melbourne', 'Durban', 'St Lucia', 'Wellington', 'Lauderhill', 
    'Hamilton', 'Centurion', 'Manchester', 'Abu Dhabi', 'Mumbai', 
    'Nottingham', 'Southampton', 'Mount Maunganui', 'Chittagong', 
    'Kolkata', 'Lahore', 'Delhi', 'Nagpur', 'Chandigarh', 'Adelaide', 
    'Bangalore', 'St Kitts', 'Cardiff', 'Christchurch', 'Trinidad'
]

# Streamlit UI components
st.title('Cricket Score Predictor')

# Input fields for teams and city
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Select batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select bowling team', sorted(teams))

city = st.selectbox('Select city', sorted(cities))

# Input fields for current match status
col3, col4, col5, col6 = st.columns(4)
with col3:
    current_score = st.number_input('Current Score')
with col4:
    overs = st.number_input('Overs done (works for over > 5)', min_value=0.0, step=0.1)
with col5:
    wickets = st.number_input('Wickets out', min_value=0, max_value=10, step=1)
with col6:
    last_five = st.number_input('Runs scored in last 5 overs')

# Prediction button
if st.button('Predict Score'):
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = current_score / overs if overs > 0 else 0  # Avoid division by zero
    
    # Create input DataFrame for prediction
    input_data = {
        'batting_team': [batting_team], 
        'bowling_team': [bowling_team], 
        'city': [city], 
        'current_score': [current_score],
        'balls_left': [balls_left], 
        'wickets_left': [wickets_left], 
        'crr': [crr], 
        'last_five': [last_five]
    }
    input_df = pd.DataFrame(input_data)
    
    # Make prediction
    try:
        result = model.predict(input_df)
        st.success("Predicted Score: " + str(int(result[0])))
    except Exception as e:
        st.error("Prediction failed. Error: {}".format(e))
