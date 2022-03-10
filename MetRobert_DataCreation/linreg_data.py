import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# we are a supermarket
# we are going to save how many products are sold each day
# we are also going to measure how many people there are each day

# x = amount of people in store
x = np.array([20, 30, 40, 50, 60, 70, 80, 85, 100])

# y = amount of products stored
acc = np.array([89.88, 90.23, 90.91, 91.73, 92.09, 92.37, 92.48, 92.80, 93.32])
f1 = np.array([67.24, 69.76, 71.22, 72.38, 74.21, 75.54, 76.37, 76.29, 79.22])

x = x.reshape(-1, 1)
#print(x)
#print(acc)
#print(f1)

acc_model = LinearRegression().fit(x, acc)
f1_model = LinearRegression().fit(x, acc)

# how good is our model?
r_sq_acc = acc_model.score(x, acc)
r_sq_f1 = f1_model.score(x, f1)

print("acc model score = " + str(r_sq_acc))
print("f1 model score = " + str(r_sq_f1))

# predict using our model 
y_pred_110 = acc_model.predict(np.array([110]).reshape(1, -1))
y_pred_120 = acc_model.predict(np.array([110]).reshape(1, -1))
y_pred_130 = acc_model.predict(np.array([110]).reshape(1, -1))
y_pred_140 = acc_model.predict(np.array([110]).reshape(1, -1))
y_pred_150 = acc_model.predict(np.array([110]).reshape(1, -1))

print(y_pred_110)
print(y_pred_120)
print(y_pred_130)
print(y_pred_140)
print(y_pred_150)
