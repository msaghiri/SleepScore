import numpy as np
import matplotlib.pyplot as plot
import pandas as pd

class Training:

    IDEAL_HOURS_OF_SLEEP = 8.5 #This number was derived from the csv, 8-8.5 hours is virtually the same and it is the most efficient in terms of correlation to sleep quality 


    #Values from training
    WEIGHT_SLEEP_DEFICIT = -0.4699773730911285
    BIAS_SLEEP_DEFICIT = 8.588984016359197

    WEIGHT_STRESS_LEVEL = -0.6062274064157418
    BIAS_STRESS_LEVEL = 10 #Our prediction gets closer to 10 when the individual is not stressed

    def load_data(self, filename):
        self.data_set = pd.read_csv(filename)

        self.data_set = self.data_set.rename(columns = {
            "Gender": "gender",
            "Age": "age",
            "Sleep Duration": "time_slept",
            "Quality of Sleep": "sleep_score",
            "Stress Level": "stress_level",
            "BMI Category": "bmi_category",
            "Heart Rate": "heart_rate",
            "Daily Steps": "daily_steps"
        })

        columns_to_drop = ['Physical Activity Level', 'Occupation', 'Blood Pressure', 'Sleep Disorder', 'Person ID'] 
        self.data_set = self.data_set.drop(columns=columns_to_drop)
        self.data_set['gender'] = self.data_set['gender'].map({
            "Male": 1,
            "Female": 0
        })

        self.data_set['bmi_category'] = self.data_set['bmi_category'].replace({
            'Normal Weight': 'Normal'
        })

        self.data_set['bmi_category'] = self.data_set['bmi_category'].map({
            "Normal": 0,
            "Overweight": 1,
            "Obese": 2
        })

        self.data_set['sleep_deficit'] = self.data_set['time_slept'] - self.IDEAL_HOURS_OF_SLEEP
    
    ##Generate the equation for the implication of sleep deficit on sleep quality
    def regress_sleep_deficit(self):
        X = self.data_set['sleep_deficit'].to_numpy()
        X_squared = X**2
        y = self.data_set['sleep_score'].to_numpy()
        y_hat = 0

        learning_rate = 0.01

        weight_1 = 0
        bias = 0

        iterations = 50000


        m = len(y)

        for i in range(iterations):
            y_hat = weight_1 * X_squared + bias

            error = y_hat - y

            gradient_weight_1 = (1/m) * np.dot(error, X_squared)
            gradient_bias = (1/m) * np.sum(error)

            weight_1 -= learning_rate * gradient_weight_1
            bias -= learning_rate * gradient_bias
        
        bias += 0.1
        y_hat = weight_1 * (X_squared) + bias
        mse = np.mean((y_hat - y)**2)
        print("MSE:", mse) #MSE: 0.354820493268653
    

        return weight_1, bias #-0.4699773730911285, 8.588984016359197


    def regress_sleep_stress(self):
        X = self.data_set['stress_level']
        y = self.data_set['sleep_score']
        y_hat = 0
        weight_1 = 0
        bias = 0 
        m = len(y)
        iterations = 50000
        learning_rate = 0.01

        for i in range(iterations):
            y_hat = weight_1 * X + bias
            error = y_hat - y

            gradient_weight_1 = (1/m) * np.dot(error, X)
            gradient_bias = (1/m) * np.sum(error)

            weight_1 -= learning_rate * gradient_weight_1
            bias -= learning_rate * gradient_bias
        
        ##Quickly calculate the MSE to get a gauge of how well the model did 
        y_hat = weight_1 * X + bias
        mse = np.mean((y_hat - y)**2)

        print(f'MSE: {mse}') #MSE: 0.27469333057142503

        return weight_1, bias #-0.6062274064157418, 10
    
    #Predict the sleep score for a given row
    def predict_sleep_score(self, row, w_deficit, b_deficit, w_stress, b_stress):

        #Predicting stress and deficit components based purely on the regressive models
        stress_component = w_stress * row['stress_level'] + b_stress


        deficit = row['sleep_deficit'] 
        deficit_component = w_deficit * (deficit ** 2) + b_deficit

        #Age and step showed much higher sleep quality for people over the age of 35 and for people who took more than 4000 steps in a given day
        step_boost = 0.5 if row['daily_steps'] >= 4000 else 0


        age_boost = 0.6 if row['age'] >= 35 else 0

        #The data showed worse mean sleep qualities for overweight and obese people, but not a concrete correlation. This addition did lower the MSE of the model
        bmi_penalty = 0
        if row['bmi_category'] == 1:
            bmi_penalty = -0.3
        elif row['bmi_category'] == 2:
            bmi_penalty = -0.6


        predicted_score = (((stress_component) + (deficit_component)) / 2) + step_boost + age_boost + bmi_penalty
        
        # NOTE:
        # While including gender reduced MSE from 0.5 to 0.31, the target variable (sleep quality) is subjective.
        # The observed correlation may reflect self-reporting bias rather than a difference in objective sleep quality, so the feature was excluded for generalizability.

        #if row['gender'] == 1: 
        #    predicted_score -= 0.5 

        return max(1, min(10, predicted_score)) 
    

    def predict(self, stress_level, actual_sleep_hours, daily_steps, age, bmi_category, gender):
        sleep_deficit = actual_sleep_hours - self.IDEAL_HOURS_OF_SLEEP

        new_data = pd.DataFrame({
            'stress_level': [stress_level],
            'sleep_deficit': [sleep_deficit],
            'daily_steps': [daily_steps],
            'age': [age],
            'bmi_category': [bmi_category],
            'gender': [gender]
        })

        row = new_data.iloc[0]

        return self.predict_sleep_score(
            row,
            self.WEIGHT_SLEEP_DEFICIT,
            self.BIAS_SLEEP_DEFICIT,
            self.WEIGHT_STRESS_LEVEL,
            self.BIAS_STRESS_LEVEL
        )
    
    def check_mse(self):
        predictions = self.data_set.apply(lambda row: self.predict_sleep_score(row, self.WEIGHT_SLEEP_DEFICIT, self.BIAS_SLEEP_DEFICIT, self.WEIGHT_STRESS_LEVEL, self.BIAS_STRESS_LEVEL), axis=1)
        mse = np.mean((predictions - self.data_set['sleep_score']) ** 2)
        print(f'Final MSE: {mse:.3f}')

        return predictions.to_numpy()
    
    def test_model(self):

        example_data = pd.DataFrame({ #Perfect conditions, predicts 10 as expected
            'stress_level': [0],
            'sleep_deficit': [0],
            'daily_steps': [4500],
            'age': [35],
            'bmi_category': [0],
            'gender': [0]
        })
        

        score = self.predict_sleep_score(example_data.iloc[0], self.WEIGHT_SLEEP_DEFICIT, self.BIAS_SLEEP_DEFICIT, self.WEIGHT_STRESS_LEVEL, self.BIAS_STRESS_LEVEL)
        print(score)

        return score




###FOR EXPERIMENTATION PURPOSES
trainer = Training()
trainer.load_data('training_set.csv')
#example_score = trainer.predict(stress_level=3, actual_sleep_hours=7.5, daily_steps=5000, age=40, bmi_category=0, gender=1)
#print(example_score)

trainer.check_mse()
