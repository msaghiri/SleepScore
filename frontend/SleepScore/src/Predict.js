export const IDEAL_HOURS_OF_SLEEP = 8.5 
const WEIGHT_SLEEP_DEFICIT = -0.4699773730911285
const BIAS_SLEEP_DEFICIT = 8.588984016359197

const WEIGHT_STRESS_LEVEL = -0.6062274064157418
const BIAS_STRESS_LEVEL = 10 



export function predictSleepScore(row) {

    const stress_component = WEIGHT_STRESS_LEVEL * row.stress_level + BIAS_STRESS_LEVEL;


    const deficit = row.sleep_deficit;
    const deficit_component = WEIGHT_SLEEP_DEFICIT * (deficit ** 2) + BIAS_SLEEP_DEFICIT; 


    const step_boost = row.daily_steps >= 4000 ? 0.5 : 0;


    const age_boost = row.age >= 35 ? 0.6 : 0;


    let bmi_penalty = 0;
    if (row.bmi_category === 1) {
        bmi_penalty = -0.3;
    } else if (row.bmi_category === 2) {
        bmi_penalty = -0.6;
    }


    let predicted_score = ((stress_component + deficit_component) / 2) + step_boost + age_boost + bmi_penalty;


    return Math.max(1, Math.min(10, predicted_score));
}




