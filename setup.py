from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="algo_verite_medical",
    version="1.0.0",
    description="Système de recherche sanitaire et prédiction de rétablissement basé sur l'analyse pyramidale",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    python_requires=">=3.8",
)