export async function getPrediction(population, averageIncome, unemploymentRate) {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        population,
        average_income: averageIncome,
        unemployment_rate: unemploymentRate
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Prediction API failed');
    }

    const data = await response.json();
    return data; // { prediction: number, risk_level: string }
  } catch (err) {
    console.error("Prediction error:", err);
    return { prediction: null, risk_level: "Error" };
  }
}
