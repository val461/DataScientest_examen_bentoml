import pandas as pd
from sklearn.model_selection import train_test_split

input_path='data/raw/admission.csv'

data = pd.read_csv(input_path)
data = data.drop(columns=['Serial No.'])

X = data.drop(columns=['Chance of Admit '])
y = data['Chance of Admit ']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

X_train.to_csv('data/processed/X_train.csv', index=False)
X_test.to_csv('data/processed/X_test.csv', index=False)
y_train.to_csv('data/processed/y_train.csv', index=False)
y_test.to_csv('data/processed/y_test.csv', index=False)
