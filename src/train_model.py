import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import bentoml

X_train = pd.read_csv('data/processed/X_train.csv')
y_train = pd.read_csv('data/processed/y_train.csv')

model = LinearRegression()
model.fit(X_train, y_train)

X_test = pd.read_csv('data/processed/X_test.csv')
y_test = pd.read_csv('data/processed/y_test.csv')

y_pred = model.predict(X_test)

rmse = mean_squared_error(y_test, y_pred)**.5
r2 = r2_score(y_test, y_pred)

print(f"RMSE on test set: {rmse}")
print(f"R2 on test set: {r2}")

if rmse < 0.1 and r2 > 0.7:
    print("saving")
    bentoml.sklearn.save_model("admission_model", model)
    # bentoml models list
else:
    print("not saving")
