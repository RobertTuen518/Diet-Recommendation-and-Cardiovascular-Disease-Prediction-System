import joblib
import pandas as pd
import streamlit as st
import PIL
import mysql.connector
from sklearn.preprocessing import StandardScaler
from random_forest_2nd import load_data
from random_forest_2nd import train_model
from random_forest_2nd import predict

# Create a MySQL database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="drs_cvd_system"
)

# Create a cursor object to interact with the database
cursor = db_connection.cursor()

# Load the dataset
data = pd.read_csv("C:/Users/User/PycharmProjects/Python_Tutorial/USDA_KM_V3.csv")

# Load the model and scaler
kmeans = joblib.load('C:/Users/User/PycharmProjects/Python_Tutorial/kmeans_v3.joblib')

# Create a feature matrix
scaled_data = data[
    ['Calories (kcal)', 'Total Fat (g)', 'Cholesterol (mg)', 'Carbohydrate (g)', 'Sugar (g)', 'Protein (g)']]

# Scale the data to improve model performance
scaler = StandardScaler()
scaler.fit_transform(scaled_data)

kmeans.fit(scaled_data)


# Define the diet_recommendation function
def diet_recommendation(calories):
    # Calculate the recommended intake of macronutrients
    Protein = calories * 0.15 / 4
    TotalFat = calories * 0.3 / 9
    Carbohydrate = calories * 0.4 / 4
    Sugar = calories * 0.1 / 4
    Cholesterol = calories * 0.05 / 4  # Adjust the coefficient as needed

    # Select foods from the same cluster as the target calorie intake
    diet_features = ['Food Description', 'Calories (kcal)', 'Total Fat (g)', 'Cholesterol (mg)', 'Carbohydrate (g)',
                     'Sugar (g)', 'Protein (g)']
    data_with_features = data[diet_features]
    target = [calories, TotalFat, Carbohydrate, Sugar, Protein, Cholesterol]
    filtered_data = data_with_features[data['cluster'] == kmeans.predict(scaler.transform([target]))[0]]

    # Set the values to three decimal places
    filtered_data = filtered_data.round(3)

    return filtered_data.head(10)


tab1, tab2, tab3 = st.tabs(["Page 1", "Page 2", "Diet Recommendation"])

with tab1:
    # Page 1
    image = PIL.Image.open('C:/Users/User/PycharmProjects/Python_Tutorial/OIP.jpg')
    st.image(image, width=600, use_column_width="always")

    st.header("Diet Recommendation and Cardiovascular Disease Risk Prediction")
    # st.subheader("Please enter your personal information below:")
    st.markdown(
        "<h4 style='margin-bottom: 0px;'>Part 1: Predict the Presence of Cardiovascular Disease Risk</h4>",
        unsafe_allow_html=True)
    st.markdown(
        "<h5 style='margin-bottom: 0px;'>Please enter your personal information below: </h5>",
        unsafe_allow_html=True)

    # Create text input for name
    name = st.text_input("Name")

    # Create numeric input for age
    age = st.slider("Age", 0, 120, 10)

    # Create a select widget for gender
    gender = st.selectbox("Gender", options=["Male", "Female"])

    # Create numeric input for height
    height = st.number_input("Height (cm)", min_value=0.0, max_value=300.0, step=0.1)

    # Create numeric input for weight
    weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, step=0.1)

    # Create slider for Systolic Blood Pressure
    systolic_bp = st.slider("Systolic Blood Pressure (mmHg)", 70, 190, 120)

    # Create slider for Diastolic Blood Pressure
    diastolic_bp = st.slider("Diastolic Blood Pressure (mmHg)", 40, 100, 80)

    # Create a select widget for cholesterol
    cholesterol = st.selectbox('Cholesterol Level', options=['Normal', 'Above Normal', 'Well Above Normal'])

    # Create a select widget for glucose
    glucose = st.selectbox('Glucose Level', options=['Normal', 'Above Normal', 'Well Above Normal'])

    # Create a select widget for smoke
    smoke = st.selectbox('Do you smoke?', options=['Yes', 'No'])

    # Create a radio button for alcohol
    alcohol = st.radio("Do you like to drink alcohol?", ("Yes", "No"))

    # Create a radio button for active
    active = st.radio("Are you an active person?", ("Yes", "No"))

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

        # Validate that name is provided
        if not name:
            st.warning("Please provide required information before predicting.")
        else:
            # Loading the dataset
            df, X, y = load_data()

            # Train the model
            model = train_model(X, y)

            # Get the prediction
            prediction = predict(X, y, features)

            score = model.score(X, y)

            st.success(f"Model Trained Successfully. Accuracy: {score:.2%}")

            # st.success("Predicted Sucessfully")

            # Insert the prediction into the database
            if prediction == 1:
                prediction_label = "high risk"
            else:
                prediction_label = "low risk"

            # SQL query to insert the values into the database
            insert_query = """
                                                INSERT INTO health_records (name, gender, height, weight, systolic_bp, 
                                                                            diastolic_bp, cholesterol_level, 
                                                                            glucose_level, smoke, alcohol, active,
                                                                            physical_activity_level, health_status)
                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                                """

            values = (name, gender, height, weight, systolic_bp, diastolic_bp,
                      cholesterol, glucose, smoke, alcohol, active, activity_level, prediction_label)

            cursor.execute(insert_query, values)

            st.success("User data has been successfully inserted into the database")

            # Commit the changes to the database
            db_connection.commit()

            # Print the output according to the prediction
            if prediction == 1:
                st.info('You are at high risk of developing a cardiovascular disease.')
                st.warning("You should consume low saturated fats, controlling calories,"
                           " and limiting cholesterol intake.")
                st.session_state.submit_disabled = False  # Enable the "Submit" button
            else:
                st.info('You are at low risk of developing a cardiovascular disease.')
                st.info(
                    "You should maintain a balanced diet and a moderate intake of calories while "
                    "limiting added sugars and cholesterol-rich foods.")
                st.session_state.submit_disabled = True  # Disable the "Submit" button


    # Display the existing data in a Streamlit table
    def fetch_data():
        query = "SELECT * FROM health_records"
        cursor.execute(query)
        health_data = cursor.fetchall()
        return health_data


    db_data = fetch_data()

    # Get column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Define a dictionary to rename columns (modify this as needed)
    column_name_mapping = {
        "current_column_name_1": "desired_column_name_1",
        "current_column_name_2": "desired_column_name_2",
        "current_column_name_3": "desired_column_name_3",
        "current_column_name_4": "desired_column_name_4",
        "current_column_name_5": "desired_column_name_5",
        "current_column_name_6": "desired_column_name_6",
        "current_column_name_7": "desired_column_name_7",
        "current_column_name_8": "desired_column_name_8",
        "current_column_name_9": "desired_column_name_9",
        "current_column_name_10": "desired_column_name_10",
        "current_column_name_11": "desired_column_name_11",
        "current_column_name_12": "desired_column_name_12",
        "current_column_name_13": "desired_column_name_13",
        "current_column_name_14": "desired_column_name_14",
        # Add more mappings as needed
    }

    # Rename columns based on the dictionary
    renamed_data = []
    for row in db_data:
        renamed_row = {column_name_mapping.get(column, column): value for column, value in zip(column_names, row)}
        renamed_data.append(renamed_row)

    # Create a button to toggle data visibility
    if st.button("View Data"):

        # Display the data in a Streamlit table with renamed columns
        st.table(renamed_data)

        # Add a button to close or cancel the table
        if st.button("Close"):
            st.write("Table closed. Toggle the 'View Data' button to display again.")

    # Initialize a session state variable to control the button's state
    if 'submit_disabled' not in st.session_state:
        st.session_state.submit_disabled = True

    # Create button to navigate to Page 2
    if st.button("Submit", disabled=st.session_state.submit_disabled):
        with tab2:
            # Page 2
            st.title("Results")
            # st.subheader("Based on the information you provided, your results are as follows:")
            st.markdown(
                "<h4 style='margin-bottom: 0px;'>Based on the information you provided, "
                "your results are as follows:</h4>",
                unsafe_allow_html=True)

            # Calculate BMI
            if height != 0:
                bmi = weight / ((height / 100) ** 2)
                bmi_status = ""
                if bmi < 18.5:
                    bmi_status = "Underweight"
                elif 18.5 <= bmi < 25:
                    bmi_status = "Normal weight"
                elif 25 <= bmi < 30:
                    bmi_status = "Overweight"
                else:
                    bmi_status = "Obese"
            else:
                bmi = 0
                bmi_status = "Invalid input: height cannot be zero"

            age = float(age)
            weight = float(weight)
            height = float(height)

            # Create a dictionary for each physical activity level
            activity_level_dict = {
                "Sedentary": 1.2,
                "Lightly Active": 1.375,
                "Moderately Active": 1.55,
                "Very Active": 1.725,
                "Extra Active": 1.9
            }

            # Calculate total daily energy expenditure based on Harris-Benedict Equation
            activity_level_value = activity_level_dict.get(activity_level, 1.2)

            if gender == "Male":
                bmr = 66.5 + (13.75 * weight) + (5.003 * height) - (6.75 * age)
            else:
                bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)

            # Total Daily Energy Expenditure (tdee) in calories multiply Basal Metabolic Rate (bmr) by the
            # appropriate activity factor
            tdee = bmr * activity_level_value

            st.session_state.tdee = round(tdee, 2)

            # Display results in table form
            results = [
                ("Name", name),
                ("Age", int(age)),
                ("Gender", gender),
                ("BMI", round(bmi, 2)),
                ("BMI Status", bmi_status),
                ("Total Daily Energy Expenditure in calories", st.session_state.tdee)
            ]

            col1, col2 = st.columns(2)
            for i, r in enumerate(results):
                with col1:
                    st.write(f"{r[0]}:")
                with col2:
                    st.write(r[1])

            # Create button to navigate back to Page 1
            if st.button("Reset"):
                st.session_state = tab1
                # with tab1:
                # st.experimental_rerun()

with tab3:
    # Page 3
    # Retrieve the value of tdee from st.session_state
    tdee = st.session_state.get("tdee")

    st.markdown(
        "<h4 style='margin-bottom: 0px;'>Part 2: Personalized Top 10 Recommended Foods</h4>",
        unsafe_allow_html=True)

    # Create recommend diet button on Page 2
    # Create a button that triggers the diet_recommendation function based on user input
    if st.button("Recommend Diet", disabled=st.session_state.submit_disabled):

        # Display the recommendations in a table
        st.info("Top 10 recommended foods:")

        # Call the diet_recommendation function
        recommendations = diet_recommendation(tdee)
        recommendations = recommendations.reset_index(drop=True)
        recommendations.index = recommendations.index + 1  # Start numbering from 1

        # Set the values to three decimal places
        recommendations = recommendations.round(3)

        st.write(recommendations)

        recommendations_text = ''

        for i in range(len(recommendations)):
            recommendations_text += str(i + 1) + '. ' + recommendations.iloc[i]['Food Description'] + '\n'

        st.write(recommendations_text)

# Close the database connection
db_connection.close()
