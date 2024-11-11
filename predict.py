# Import necessary modules
import streamlit as st

# Import necessary functions from web_functions
from random_forest import predict


def app(X, y):
    """This function create the prediction page"""

    # Add title to the page
    st.title("Cardiovascular Disease Risk Prediction")

    # Add a brief description
    st.markdown(
        "<h4 style='margin-bottom: 0px;'>Part 1: Predict the Presence of Cardiovascular Disease Risk</h4>",
        unsafe_allow_html=True)

    st.markdown(
        "<h5 style='margin-bottom: 0px;'>Please enter your personal information below: </h5>",
        unsafe_allow_html=True)

    # Take input of features from the user.
    age = st.number_input('Age', min_value=0, max_value=100, value=0)
    gender = st.selectbox('Gender', options=['Male', 'Female'])
    height = st.number_input('Height (cm)', min_value=0, max_value=300, value=0)
    weight = st.number_input('Weight (kg)', min_value=0, max_value=500, value=0)
    systolic_bp = st.number_input('Systolic Blood Pressure (mmHg)', min_value=0, max_value=300, value=0)
    diastolic_bp = st.number_input('Diastolic Blood Pressure (mmHg)', min_value=0, max_value=300, value=0)
    cholesterol = st.selectbox('Cholesterol Level', options=['Normal', 'Above Normal', 'Well Above Normal'])
    glucose = st.selectbox('Glucose Level', options=['Normal', 'Above Normal', 'Well Above Normal'])
    smoke = st.selectbox('Do you smoke?', options=['Yes', 'No'])
    alcohol = st.radio("Do you like to drink alcohol?", ("Yes", "No"))
    active = st.radio("Are you a active person?", ("Yes", "No"))

    # Check the value of 'active' to determine the select box behavior
    if active == "Yes":
        activity_level = st.selectbox("Physical activity level",
                                      options=["Sedentary (little or no exercise)",
                                               "Lightly Active (light exercise/sports 1-3 days/week)",
                                               "Moderately Active (moderate exercise/sports 3-5 days/week)",
                                               "Very Active (hard exercise/sports 6-7 days a week)",
                                               "Extra Active (very hard exercise/sports & a physical job)"])
    else:
        # Disable the select box and set the default option to "Sedentary (little or no exercise)"
        activity_level = st.selectbox("Physical activity level", options=["Sedentary (little or no exercise)"], index=0,
                                      key="activity_level_disabled", disabled=True)

    # Create dictionaries to map categorical variables
    gender_dict = {'Male': 1, 'Female': 2}
    cholesterol_dict = {'Normal': 1, 'Above Normal': 2, 'Well Above Normal': 3}
    glucose_dict = {'Normal': 1, 'Above Normal': 2, 'Well Above Normal': 3}
    smoke_dict = {'Yes': 1, 'No': 0}
    alcohol_dict = {'Yes': 1, 'No': 0}
    active_dict = {'Yes': 1, 'No': 0}

    # Map categorical variables to numerical values
    gender_num = gender_dict[gender]
    cholesterol_num = cholesterol_dict[cholesterol]
    glucose_num = glucose_dict[glucose]
    smoke_num = smoke_dict[smoke]
    alcohol_num = alcohol_dict[alcohol]
    active_num = active_dict[active]

    # Create a list to store all the features
    features = [age, gender_num, height, weight, systolic_bp, diastolic_bp, cholesterol_num, glucose_num, smoke_num,
                alcohol_num, active_num]

    # Create a button to predict
    if st.button("Predict"):
        # Get prediction and model score
        prediction = predict(X, y, features)
        st.success("Predicted Sucessfully")

        # Print the output according to the prediction
        if prediction == 1:
            st.info('You are at high risk of developing a cardiovascular disease.')
            st.warning("You should consume low saturated fats, controlling calories, and limiting cholesterol "
                       "intake.")
        else:
            st.info('You are at low risk of developing a cardiovascular disease.')
            st.info("You should maintain a balanced diet and a moderate intake of calories while limiting added "
                    "sugars and cholesterol-rich foods.")
