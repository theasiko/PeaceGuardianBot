import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
df = pd.read_csv("violence_database_with_bias_v9_large_multi_entries.csv")

# Feature Engineering
# Encode categorical features using Label Encoding
le_country = LabelEncoder()
le_type_of_measures = LabelEncoder()
le_form_of_violence = LabelEncoder()

df['Country'] = le_country.fit_transform(df['Country'])
df['Type of Measures'] = le_type_of_measures.fit_transform(df['Type of Measures'])
df['Form of Violence'] = le_form_of_violence.fit_transform(df['Form of Violence'])

# Group by country and find the most popular type of violence
most_popular_per_country = df.groupby('Country')['Form of Violence'].agg(lambda x: x.mode().iat[0]).reset_index()

# Split the data into training and testing sets
train_data, test_data = train_test_split(most_popular_per_country, test_size=0.2, random_state=42)

# Define features (X) and target variable (y)
X_train = train_data[['Country']]
X_test = test_data[['Country']]
y_train = train_data['Form of Violence']
y_test = test_data['Form of Violence']

# Train a random forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model and Label Encoders to a file
model_filename = 'violence_prediction_model.joblib'
saved_data = {
    'model': model,
    'le_country': le_country,
    'le_form_of_violence': le_form_of_violence,
    'le_type_of_measures': le_type_of_measures
}
joblib.dump(saved_data, model_filename)

# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy: {accuracy}")
print(f"Trained model and Label Encoders saved to {model_filename}")
