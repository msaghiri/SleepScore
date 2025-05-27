import { predictSleepScore, IDEAL_HOURS_OF_SLEEP } from '../Predict.js';

function PredictionForm({ onScoreCalculated }) {
    function predict(e) {
        e.preventDefault();

        const stressLevel = parseFloat(document.getElementById("stress_level").value);
        const sleep = parseFloat(document.getElementById("actual_sleep_hours").value);
        const sleepDeficit = IDEAL_HOURS_OF_SLEEP - sleep;
        const dailySteps = parseInt(document.getElementById("daily_steps").value);
        const age = parseInt(document.getElementById("age").value);
        const bmiCategory = document.getElementById("bmi_category").value;

        const bmiMap = {
            normal: 0,
            overweight: 1,
            obese: 2
        };

        const finalRow = {
            stress_level: stressLevel,
            sleep_deficit: sleepDeficit,
            daily_steps: dailySteps,
            age,
            bmi_category: bmiMap[bmiCategory]
        };

        const finalSleepScore = Math.round(predictSleepScore(finalRow) * 10) / 10;
        onScoreCalculated(finalSleepScore); 
    }

    return (
        <div className="prediction-div">
            <h1>Sleep Score</h1>
            <form className="prediction-form">
                <label htmlFor="stress_level">Stress Level (0–10):</label>
                <input type="number" id="stress_level" name="stress_level" min="0" max="10" required />

                <label htmlFor="actual_sleep_hours">Actual Sleep Hours:</label>
                <input type="number" id="actual_sleep_hours" name="actual_sleep_hours" step="0.1" max="14" required />

                <label htmlFor="daily_steps">Daily Steps:</label>
                <input type="number" id="daily_steps" name="daily_steps" required />

                <label htmlFor="age">Age:</label>
                <input type="number" id="age" name="age" required />

                <label htmlFor="bmi_category">BMI Category:</label>
                <select id="bmi_category" name="bmi_category" required>
                    <option value="">Select</option>
                    <option value="normal">Normal</option>
                    <option value="overweight">Overweight</option>
                    <option value="obese">Obese</option>
                </select>

                <button type="submit" onClick={predict}>Predict</button>
            </form>
        </div>
    );
}

export default PredictionForm;
