from setuptools import setup, find_packages

setup(
    name="poverty_prediction",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-cors",
        "waitress",
        "scikit-learn",
        "pandas",
        "numpy",
        "python-dotenv",
    ],
)