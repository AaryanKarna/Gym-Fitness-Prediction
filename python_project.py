# -*- coding: utf-8 -*-
"""Python Project

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QpkBpj4wR6L1_EDYTeP1GfQ-1FrR_qDI

**Without Function** - Aaryan Karn
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler

url="https://raw.githubusercontent.com/sayande01/Kaggle_Notebooks/refs/heads/main/gym_members_exercise_tracking.csv"
dataset=pd.read_csv(url)

dataset.head()

dataset.shape

dataset.isnull().sum()

y = dataset['Calories_Burned']
X = dataset.drop(['Calories_Burned', 'Workout_Type', 'Gender'], axis=1)

X.head()

X.shape

from sklearn.model_selection import train_test_split
scaler=StandardScaler()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 2509)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32)

class RegressionModel(nn.Module):
  def __init__(self):
    super(RegressionModel, self).__init__()
    self.layer1=nn.Linear(12,1)

  def forward(self,x):
    x=self.layer1(x)
    return x

model:RegressionModel=RegressionModel()

loss = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.003)

train_loss=[]
test_loss=[]
train_accuracy=[]
train_loss=[]

num_epochs = 5000
train_losses = []  # Initialize the list for storing training losses
test_losses = []  # Initialize the list for storing test losses

for ep in range(num_epochs):
    # Training mode
    model.train()

    # Forward pass
    predicted_y = model(X_train_tensor).squeeze()
    y_train = y_train_tensor.squeeze()
    losses = loss(predicted_y, y_train_tensor)

    # Backward pass and optimization
    optimizer.zero_grad()  # Zero the gradients before the backward pass
    losses.backward()  # Backpropagation
    optimizer.step()  # Update the model parameters

    # Print training loss every 100 epochs
    if ep % 100 == 0:
        print(f"Epoch [{ep}/{num_epochs}], Training Loss: {losses.item()}")

    # Append the training loss to the list
    train_losses.append(losses.item())

    # Evaluate on test set
    model.eval()  # Set model to evaluation mode

    with torch.no_grad():  # No gradients needed for evaluation
        predicted_y_test = model(X_test_tensor).squeeze()
        y_test=y_test_tensor.squeeze()
        test_loss = loss(predicted_y_test, y_test_tensor)

    # Append the test loss to the list
    test_losses.append(test_loss.item())

    # Print test loss every 100 epochs
    if ep % 100 == 0:
        print(f"Epoch [{ep}/{num_epochs}], Test Loss: {test_loss.item()}")

predicted_y_test = predicted_y_test.numpy()  # Convert PyTorch tensor to numpy
y_test = y_test_tensor.numpy()  # Convert PyTorch tensor to numpy

# Create a dictionary with the two arrays
d = {'y_pred': predicted_y_test.flatten(), 'y_test': y_test.flatten()}

# Create a DataFrame
df = pd.DataFrame(d)

# Print the DataFrame
print(df)

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

mse = mean_squared_error(y_test, predicted_y_test)
mae = mean_absolute_error(y_test, predicted_y_test)
r2 = r2_score(y_test, predicted_y_test)

print(f"Mean Squared Error (MSE): {mse}")
print(f"Mean Absolute Error (MAE): {mae}")
print(f"R-squared (R²): {r2}")

import matplotlib.pyplot as plt

plt.scatter(y_test, predicted_y_test)
plt.xlabel("True values (y_test)")
plt.ylabel("Predicted values (y_pred)")
plt.title("True vs Predicted values")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='r', linestyle='--')
plt.show()

"""**With Function** - Aaryan Karn"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset=pd.read_csv("https://raw.githubusercontent.com/sayande01/Kaggle_Notebooks/refs/heads/main/gym_members_exercise_tracking.csv")

dataset.isna().sum()

dataset.info()

y = dataset['Calories_Burned']
X = dataset.drop(['Calories_Burned', 'Workout_Type', 'Gender'], axis=1)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 2509)

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

regressor.score(X_test,y_test)

y_pred = regressor.predict(X_test)

d = {'y_pred': y_pred, 'y_test': y_test}

pd.DataFrame(d)

