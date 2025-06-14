# -*- coding: utf-8 -*-
"""Cancer_Patient_Prediction_ML

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZRVMoMM7WD9J3TvhWmDFsAeF0Ej8asbj
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import r2_score, accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

import warnings
warnings.filterwarnings("ignore")

cancer = pd.read_excel('/content/sample_data/cancer_patient_data_sets.xlsx')

"""**Data Pre Processing**"""

cancer.head()

# Finding Number of Rows And Columns

cancer.shape
print(f"The Number Of Rows : {cancer.shape[0]}")
print(f"The Number Of Columns is : {cancer.shape[1]}")

# Gathering some information about data
# All The Data is int except (Patient Id, Level) are object

cancer.info()

# Getting Descreptive information about data

cancer.describe()

# Showing Null Values

cancer.isnull().sum()

# Showing Duplicates

duplicated_values = cancer[cancer.duplicated()]
duplicated_values

cancer.nunique()

cancer['Level'].value_counts()

# Dropping unnecessary columns for our preduction and analysis

cancer = cancer.drop(['Patient Id'], axis=1)
cancer.head()

"""**Applying Label Encoder**"""

encoder = LabelEncoder()
encoded_level = encoder.fit_transform(cancer['Level'])
encoded_level

#Generating Data Frame out of encoded data

encoded_level_df = pd.DataFrame(encoded_level)

# The Column named 'Level' is now renamed to '0'

cancer = cancer.drop('Level', axis=1)
cancer = pd.concat([cancer,encoded_level_df], axis=1)
cancer.columns

# Rename the column 'Level' with it's original name

cancer.columns=[                     'Age',                   'Gender',
                  'Air Pollution',              'Alcohol use',
                   'Dust Allergy',     'OccuPational Hazards',
                   'Genetic Risk',     'chronic Lung Disease',
                  'Balanced Diet',                  'Obesity',
                        'Smoking',           'Passive Smoker',
                     'Chest Pain',        'Coughing of Blood',
                        'Fatigue',              'Weight Loss',
            'Shortness of Breath',                 'Wheezing',
          'Swallowing Difficulty', 'Clubbing of Finger Nails',
                  'Frequent Cold',                'Dry Cough',
                        'Snoring',                          'Level']

#checking if our experiment is working good
cancer.head()

"""**Exploratory Data Analysis and Data Visualization**"""

#Age Distribution by Risk Visualization in Histogram
#Createing "Bins" and set an appropriate bin size (e.g., 5 or 10 years)

sns.distplot(cancer['Age'], bins=10)

"""**Regression analysis** is a set of statistical methods used for the estimation of relationships between a dependent variable and one or more independent variables. It can be utilized to assess the strength of the **relationship between variables and for modeling** the future relationship between them."""

# Trying to find the relationship between 'Age' in X -axis vs. 'Chest Pain' in Y -axis by Regression Analysis

sns.jointplot(x='Age', y='Chest Pain', data=cancer, kind='reg')

#visualizing the correlation between different variables in dataset using a heatmap.

plt.figure(figsize=(15,8))
sns.set_context('paper', font_scale=0.8)

cancer_mx = cancer.corr()
sns.heatmap(cancer_mx, annot=True, cmap='Blues')

# prompt: create another dataset with Fatigue, Chest Pain, Coughing of Blood, Passive Smoker, Smoking, Obesity, Balanced Diet, Chronic Lung Disease, Genetic Risk, Alcohol use, Air Pollution

# Select the specified columns to create a new dataset
selected_columns = ['Air Pollution', 'Alcohol use', 'Genetic Risk', 'chronic Lung Disease', 'Balanced Diet',
                    'Obesity', 'Smoking', 'Passive Smoker', 'Coughing of Blood', 'Chest Pain', 'Fatigue', 'Level']

# Check if the selected columns exist in the original DataFrame
existing_columns = [col for col in selected_columns if col in cancer.columns]

if len(existing_columns) == len(selected_columns):
    new_dataset = cancer[existing_columns].copy()
    print("New dataset created with the specified columns:")
    print(new_dataset.head())
else:
    print("Warning: Some specified columns were not found in the original DataFrame.")
    print("Columns found:", existing_columns)
    print("Columns not found:", list(set(selected_columns) - set(existing_columns)))
    # Create a dataset with the existing columns if some were not found
    if existing_columns:
        new_dataset = cancer[existing_columns].copy()
        print("New dataset created with the existing specified columns:")
        print(new_dataset.head())
    else:
        print("No specified columns were found in the original DataFrame.")
        new_dataset = pd.DataFrame() # Create an empty DataFrame

new_dataset.head()

# Generating a scatter plot with a regression line using the seaborn library. It
# visualizes the relationship between 'Smoking' and 'Chest Pain', with different
# colors representing 'Age'.

plt.figure(figsize=(15,8))
sns.set_context('paper', font_scale=1.1)
sns.lmplot(x='Smoking', y='Chest Pain', hue='Age', data=cancer, scatter_kws={'s':100, 'linewidths': 0.5, 'edgecolor':'w'})

# visualizeing the relationship between 'Smoking' and 'Chest Pain', with
# different colors representing 'Gender'.

sns.lmplot(x='Smoking', y='Chest Pain', hue='Gender', data=cancer, scatter_kws={'s':100, 'linewidths': 0.5, 'edgecolor':'w'})

"""The code bellow generates a grid of plots. Each plot within the grid shows the relationship between 'chronic Lung Disease' and 'Shortness of Breath'. The grid is structured such that plots in the same column represent the same gender, and plots in the same row represent the same smoking status. This allows for a visual comparison of the relationship between 'chronic Lung Disease' and 'Shortness of Breath' across different combinations of gender and smoking habits."""

sns.lmplot(x='chronic Lung Disease', y='Shortness of Breath', col='Gender', row='Smoking', data=cancer, height=8, aspect=0.6)

"""**Cancer Patient Prediction Machine Learning**"""

#Dividing Data into featurs and target

#x = cancer.iloc[:, :-1]
#y = cancer.iloc[:, -1]

#Dividing Data into featurs and target on new_dataset

x = new_dataset.iloc[:, :-1]
y = new_dataset.iloc[:, -1]

#Splitting the data for training and testing

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.25, random_state=42, stratify=y)
# stratify=y ensures that the proportion of classes in y_train and y_test is the
# same as in the original dataset.

print(f"\nTraining set size: {len(x_train)} samples")
print(f"Testing set size: {len(x_test)} samples")

"""**Logistic Regression**"""

# Logistic regression is a supervised machine learning algorithm widely used for
# binary classification tasks

model_lr = LogisticRegression()
model_lr.fit(x_train, y_train)

LogisticRegression()

predict_lr = model_lr.predict(x_test)
accuracy_lr = accuracy_score(y_test, predict_lr)
print(f"Accuracy of Logistic Regression Model : {accuracy_lr}")

cm_lr = confusion_matrix(predict_lr, y_test)
cm_lr

# Classification Report

print(classification_report(y_test, predict_lr))

sns.heatmap(cm_lr, annot=True, cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""**Support Vector Machine (SVM)**"""

# SVM is a supervised machine learning algorithm that classifies data by finding
# an optimal line or hyperplane that maximizes the distance between each class
# in an N-dimensional space.

model_svm = SVC(C=1, gamma=0.01, kernel='rbf')
model_svm.fit(x_train, y_train)

SVC(C=1, gamma=0.01)

predict_svm = model_svm.predict(x_test)
accuracy_svm = accuracy_score(predict_svm, y_test)
print(f"Accuracy of Support Vector Machine Model : {accuracy_svm}")

cm_svm = confusion_matrix(predict_svm, y_test)
cm_svm

# Classification Report

print(classification_report(y_test, predict_svm))

sns.heatmap(cm_svm, annot=True, cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""**Decision Tree Model**"""

# --- Train the Decision Tree Model --- Initialize the Decision Tree Classifier
# You can tune parameters like max_depth, min_samples_leaf, criterion='entropy'
# For a first run, we'll keep it simple or set a max_depth to avoid extreme
# overfitting.
dt_classifier = DecisionTreeClassifier(random_state=42, max_depth=5) # max_depth limits tree growth for interpretability

# Train the model
dt_classifier.fit(x_train, y_train)

print("\nDecision Tree Classifier trained successfully!")

# Make predictions on the test set
y_pred_dt = dt_classifier.predict(x_test)

# Calculate Accuracy
accuracy_dt = accuracy_score(y_test, y_pred_dt)
print(f"\nAccuracy of the Decision Tree Classifier: {accuracy_dt:.4f}")

# Display Classification Report
# This shows precision, recall, f1-score for each class
print("\nClassification Report:")
print(classification_report(y_test, y_pred_dt, target_names=encoder.classes_))

# Display Confusion Matrix
# Helps to see where the model made mistakes (e.g., predicted Medium when it was High)
cm_dt = confusion_matrix(y_test, y_pred_dt)
print("\nConfusion Matrix:")
print(cm_dt)

# Visualize Confusion Matrix using Seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Blues',
            xticklabels=encoder.classes_, yticklabels=encoder.classes_)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# --- Visualize the Decision Tree (Optional) ---
# This helps in understanding how the tree makes decisions.
# Requires graphviz if you want more interactive/exportable plots, but plot_tree is built-in.

plt.figure(figsize=(25, 15))
plot_tree(dt_classifier,
          feature_names=x.columns.tolist(),
          class_names=encoder.classes_.tolist(),
          filled=True,
          rounded=True,
          fontsize=10)
plt.title("Decision Tree Visualization", fontsize=20)
plt.show()

# Optional: Feature Importance
# See which features the tree considered most important for making predictions
feature_importances = pd.DataFrame({
    'Feature': x.columns,
    'Importance': dt_classifier.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\nFeature Importances:")
print(feature_importances)

# Optional: Visualize Feature Importances
plt.figure(figsize=(12, 8))
sns.barplot(x='Importance', y='Feature', data=feature_importances)
plt.title('Feature Importances from Decision Tree')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.show()

"""**Random Forest Classifier**"""

# --- Random Forest Classifier ---
#Implement and Train the Random Forest Model ---
# Initialize the Random Forest Classifier
# You can tune parameters like n_estimators (number of trees), max_depth, min_samples_leaf, etc.
# For a start, a reasonable number of estimators is good.
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)

# Train the model
rf_classifier.fit(x_train, y_train)

print("\nRandom Forest Classifier trained successfully!")

# --- Evaluate the Model ---

# Make predictions on the test set
y_pred_rf = rf_classifier.predict(x_test)

# Calculate Accuracy
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f"\nAccuracy of the Random Forest Classifier: {accuracy_rf:.4f}")

# Display Classification Report
# This shows precision, recall, f1-score for each class
print("\nClassification Report:")
print(classification_report(y_test, y_pred_rf, target_names=encoder.classes_))

# Display Confusion Matrix
# Helps to see where the model made mistakes (e.g., predicted Medium when it was High)
cm_rf = confusion_matrix(y_test, y_pred_rf)
print("\nConfusion Matrix:")
print(cm_rf)

#Visualize Confusion Matrix using Seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues',
            xticklabels=encoder.classes_, yticklabels=encoder.classes_)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# --- Feature Importance (Specific to Ensemble Models) ---
# See which features the Random Forest model considered most important for making predictions
feature_importances = pd.DataFrame({
    'Feature': x.columns,
    'Importance': rf_classifier.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\nFeature Importances from Random Forest:")
print(feature_importances)

# Visualize Feature Importances
plt.figure(figsize=(12, 8))
sns.barplot(x='Importance', y='Feature', data=feature_importances.head(15)) # Show top 15 features
plt.title('Top Feature Importances from Random Forest')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.tight_layout() # Adjust layout to prevent labels from overlapping
plt.show()

"""**K-Nearest Neighbors (KNN)**"""

# --- Feature Scaling (CRUCIAL for KNN) ---
# KNN calculates distances between data points, so features with larger ranges
# can disproportionately influence the distance. Scaling ensures all features
# contribute equally. StandardScaler makes the mean 0 and standard deviation 1.

scaler = StandardScaler()

# Fit the scaler on the training data and transform both training and testing data
X_train_scaled = scaler.fit_transform(x_train)
X_test_scaled = scaler.transform(x_test)

print("\nFeatures scaled successfully using StandardScaler.")
print("First 10 rows of scaled training features (X_train_scaled):")
print(X_train_scaled[:10])

# --- Implement and Train the K-Nearest Neighbors (KNN) Model ---
# Initialize the KNN Classifier
# The 'n_neighbors' parameter (k) is critical. A common starting point is 5.
# Eexperimenting with different values of k.
knn_classifier = KNeighborsClassifier(n_neighbors=7, weights="distance", metric='minkowski', p=2)

# Train the model
knn_classifier.fit(X_train_scaled, y_train) # Train on scaled data
#knn_classifier.fit(x_train, y_train) # Train on new_dataset non scaled data

print(f"\nK-Nearest Neighbors Classifier trained successfully with n_neighbors = {knn_classifier.n_neighbors}!")

# --- Evaluate the Model ---

# Make predictions on the scaled test set
y_pred_knn = knn_classifier.predict(X_test_scaled) # Predict on scaled data

# Calculate Accuracy
accuracy_knn = accuracy_score(y_test, y_pred_knn)
print(f"\nAccuracy of the KNN Classifier: {accuracy_knn:.4f}")

# Display Classification Report
# This shows precision, recall, f1-score for each class
print("\nClassification Report:")
print(classification_report(y_test, y_pred_knn, target_names=encoder.classes_))

# Display Confusion Matrix
# Helps to see where the model made mistakes (e.g., predicted Medium when it was High)
cm_knn = confusion_matrix(y_test, y_pred_knn)
print("\nConfusion Matrix:")
print(cm_knn)

# Visualize Confusion Matrix using Seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(cm_knn, annot=True, fmt='d', cmap='Blues',
            xticklabels=encoder.classes_, yticklabels=encoder.classes_)
plt.title('Confusion Matrix for KNN')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# --- Finding Optimal 'k' using a simple loop ---
# It's good practice to try a range of 'k' values to find the best one.
# This simple loop plots accuracy vs. k.

print("\n--- Finding Optimal 'k' ---")
accuracies = []
k_range = range(1, 21) # Test k from 1 to 20

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_scaled, y_train)
    y_pred_k = knn.predict(X_test_scaled)
    accuracies.append(accuracy_score(y_test, y_pred_k))

plt.figure(figsize=(10, 6))
plt.plot(k_range, accuracies, marker='o', linestyle='--')
plt.title('KNN Accuracy vs. Number of Neighbors (k)')
plt.xlabel('Number of Neighbors (k)')
plt.ylabel('Accuracy')
plt.xticks(k_range)
plt.grid(True)
plt.show()

optimal_k = k_range[accuracies.index(max(accuracies))]
print(f"Optimal 'k' found (based on this range): {optimal_k} with accuracy {max(accuracies):.4f}")