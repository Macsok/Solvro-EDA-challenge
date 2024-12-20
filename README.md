# Exploratory Data Analysis
An attempt to solve an exploratory data analysis challenge proposed by Solvro. This repository contains all files and scripts used in the analysis. The entire work is documented in the `Exploratory_Data_Analysis_report.pdf` file. Nonetheless, I strongly recommend reviewing the script files and following the data mining pattern. The project took over 30 hours to complete.

## Report description
The Exploratory Data Analysis (EDA) presented in this report investigates a dataset of 134 cocktails, aiming to uncover key characteristics, relationships between ingredients, and groupings of similar drinks. The analysis emphasizes the importance of understanding the data through visualization and descriptive statistics, while also addressing issues like missing values and ingredient consistency. Using clustering techniques, the report categorizes cocktails based on ingredient similarities, providing insights that can enhance cocktail recommendations. Overall, this EDA serves as a foundational step for further research and development in the realm of cocktail analysis and recommendations.

# Download the repository
Clone the repository:
```sh
git clone https://github.com/Macsok/Exploratory-Data-Analysis
cd Exploratory-Data-Analysis
```

# Using Virtualenv
Use virtualenv to isolate project dependencies, ensuring no conflicts between different projects.
First, install Virtualenv if you haven't already:
```sh
pip install virtualenv
```
Navigate to main project directory and create a new virtual environment:
```sh
virtualenv venv
```
Activate the Virtual Environment:
```sh
source myenv/bin/activate
```
When activated, your shell will show the virtual environment’s name in the prompt.

Now that the environment is active, you can install packages:
```sh
pip install -r dependencies/requirements.txt
```
Once you have finished working on your project, it’s a good habit to deactivate its venv. By deactivating, you leave the virtual environment.
```sh
deactivate
```
Delete the Virtual Environment (if your virtual environment is in a directory called 'venv':):
```sh
rm -r venv
```

You can learn more about virtual environments at: https://python.land/virtual-environments/virtualenv

## Prerequisites
- Python 3.x
    
## Required Libraries
- `pandas`
- `matplotlib`
- `numpy`
- `seaborn`
- `scikit-learn`
- `typing`

<!--
# An approach to the problem
<div align="center">
<img src="/assets/idea.png" alt="mindmap" title="mindmap" height="500"/>
</div>
-->

# Process of learning - date stamps of the exploration
  - 10.10.2024    first look at the problem, revision of pandas, 1h
  - 11.10.2024    unpacking data from every row (solving problems with datatypes), over 2h
  - 12.10.2024    developing an approach, data preprocessing, EDA, over 6h 
  - 13.10.2024    unpacking and extracting indexes, 1.5h
  - 14.10.2024    answered for a couple of questions about the dataset, wrote script that extracts ingredients from list of cocktails, 3.5h
  - 17.10.2024    preprocessing data script, started scikit-learn analysis, 0.5h
  - 18.10.2024    ingredients reference to list, 1h
  - 19.10.2024    list of ingredients to list of names function, K-means, 1.5h
  - 21.10.2024    cleaned up scikit-learn analysis, clusterization and prediction scripts, 2h
  - 22.10.2024    clustered visualization, brief documentation, 2h
  - 23.10.2024    report preparation, 1.5h
  - 24.10.2024    reporting cocktail only analyse, 2h
  - 25.10.2024    reporting ingredients analyse, 2h
  - 26.10.2024    reporting whole dataset analysis, script correction, 2h
  - 27.10.2024    reporting clusterisation, 1h
  - 28.10.2024    report summary, repository description, 3.5h
