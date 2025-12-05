import requests

import requests

test_cases = [
    # Format: {'population': value, 'average_income': value, 'unemployment_rate': value}
    {'population': 100000, 'average_income': 10000, 'unemployment_rate': 30.0},  # Should be high risk
    {'population': 50000, 'average_income': 15000, 'unemployment_rate': 15.0},   # Moderate risk
    {'population': 20000, 'average_income': 30000, 'unemployment_rate': 8.0},    # Low risk
    {'population': 10000, 'average_income': 50000, 'unemployment_rate': 5.0},    # Very low risk
]

print("Testing API with different scenarios:\n" + "="*50)

for i, test_case in enumerate(test_cases, 1):
    response = requests.post(
        'http://localhost:5001/predict',
        json=test_case
    )
    result = response.json()
    print(f"\nTest Case {i}:")
    print(f"Input: {test_case}")
    print(f"Status Code: {response.status_code}")
    print(f"Predicted Poverty Rate: {result.get('prediction', 'N/A'):.2f}%")
    print(f"Risk Level: {result.get('risk_level', 'N/A')}")
    print("-" * 50)