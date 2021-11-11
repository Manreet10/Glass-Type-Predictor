# Importing the necessary Python modules.
import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from sklearn.metrics import precision_score, recall_score 

# ML classifier Python modules
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Loading the dataset.
@st.cache()
def load_data():
    file_path = "glass-types.csv"
    df = pd.read_csv(file_path, header = None)
    # Dropping the 0th column as it contains only the serial numbers.
    df.drop(columns = 0, inplace = True)
    column_headers = ['RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe', 'GlassType']
    columns_dict = {}
    # Renaming columns with suitable column headers.
    for i in df.columns:
        columns_dict[i] = column_headers[i - 1]
        # Rename the columns.
        df.rename(columns_dict, axis = 1, inplace = True)
    return df

glass_df = load_data() 

# Creating the features data-frame holding all the columns except the last column.
X = glass_df.iloc[:, :-1]

# Creating the target series that holds last column.
y = glass_df['GlassType']

# Spliting the data into training and testing sets.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

@st.cache()
def prediction(model,RI,Na,Mg,Al,Si,K,Ca,Ba,Fe):
  glass_type = model.predict([[RI,Na,Mg,Al,Si,K,Ca,Ba,Fe]])
  glass_type = glass_type[0]
  if glass_type == 1:
    return "building windows float processed".upper()

  elif glass_type == 2:
    return "building windows non float processed".upper()

  elif glass_type == 3:
    return "vehicle windows float processed".upper()

  elif glass_type == 4:
    return "vehicle windows non float processed".upper()

  elif glass_type == 5:
    return "containers".upper()

  elif glass_type == 6:
    return "tableware".upper()

  else:
    return "headlamp".upper()

# S4.1: Add title on the main page and in the sidebar.
st.title("Glass Type Predictor")
st.sidebar.title("Exploratory Data Analysis")

# S5.1: Using the 'if' statement, display raw data on the click of the checkbox.
if st.sidebar.checkbox("Show raw data"):
  st.subheader("Full Dataset")
  st.dataframe(glass_df)

# S6.1: Scatter Plot between the features and the target variable.
# Add a subheader in the sidebar with label "Scatter Plot".
st.sidebar.subheader("Scatter Plot")
# Choosing x-axis values for the scatter plot.
features_list = st.sidebar.multiselect("Select the x-axis values",('RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe'))

# Remove deprecation warning.
st.set_option('deprecation.showPyplotGlobalUse', False)
for i in features_list:
  st.subheader(f"Scatter plot between {i} and Glass Type")
  plt.figure(figsize=(20,8))
  sns.scatterplot(x = i, y = 'GlassType',data = glass_df)
  st.pyplot()

# Sidebar for histograms.
st.sidebar.subheader("Histogram")
# Choosing features for histograms.
hist_features  = st.sidebar.multiselect("Select features to create histogram",('RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe'))
# Create histograms.
for i in hist_features:
  st.subheader(f"Histogram for {i}")
  plt.figure(figsize=(20,8))
  plt.hist(glass_df[i], bins = 'sturges',edgecolor = 'red')
  st.pyplot()

# Sidebar for box plots.
st.sidebar.subheader("Boxplot")
# Choosing columns for box plots.
box_features  = st.sidebar.multiselect("Select columns to create boxplot",('RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe'))
# Create box plots.
for i in box_features:
  st.subheader(f"Boxplot for {i}")
  plt.figure(figsize=(20,8))
  sns.boxplot(glass_df[i])
  st.pyplot()

