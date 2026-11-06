#-----------------------------------------------------------------------
# Project Name : Head Brain Analysis Case Study
# Description : Uses linear regression to study the relationship between head size and brain weight.
# Author : Samruddhi Mandage
# Date : 05/11/2026
#-----------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score

Border = "-"*70

#-----------------------------------------------------------------------
# function name : LoadData
# Description : Load Head Brain dataset
# Input : CSV file path
# Output : DataFrame
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def LoadData(DataPath):

    df = pd.read_csv(DataPath)

    print("Dataset loaded successfully")
    print(df.head())

    return df

#-----------------------------------------------------------------------
# function name : AnalyseData
# Description : Perform basic data analysis
# Input : DataFrame
# Output : None
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def AnalyseData(df):

    print(Border)
    print("Shape of dataset :",df.shape)
    print(Border)

    print("Missing values :")
    print(df.isnull().sum())

    print(Border)
    print("Statistical report :")
    print(df.describe())

#-----------------------------------------------------------------------
# function name : SplitData
# Description : Separate features and target
# Input : DataFrame
# Output : Training and testing data
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def SplitData(df):

    df = df.dropna()

    X = df[["Head Size(cm^3)"]]
    Y = df["Brain Weight(grams)"]

    X_train,X_test,Y_train,Y_test = train_test_split(
        X,Y,test_size=0.2,random_state=42
    )

    print("Dataset splitting completed")
    return X_train,X_test,Y_train,Y_test

#-----------------------------------------------------------------------
# function name : TrainModel
# Description : Train Linear Regression model
# Input : Training data
# Output : Trained model
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def TrainModel(X_train,Y_train):

    Model = LinearRegression()

    Model = Model.fit(X_train,Y_train)

    print("Model trained successfully")
    return Model

#-----------------------------------------------------------------------
# function name : EvaluateModel
# Description : Evaluate regression model
# Input : Model and testing data
# Output : MSE and R2 score
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def EvaluateModel(Model,X_test,Y_test):

    Y_pred = Model.predict(X_test)

    print("Mean Squared Error :",mean_squared_error(Y_test,Y_pred))
    print("R2 Score :",r2_score(Y_test,Y_pred))

    return Y_pred

#-----------------------------------------------------------------------
# function name : VisualizeData
# Description : Plot actual values and regression line
# Input : Testing data and predicted values
# Output : Scatter plot
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def VisualizeData(X_test,Y_test,Y_pred):

    plt.scatter(X_test,Y_test,label="Actual data")
    plt.plot(X_test,Y_pred,label="Regression line")

    plt.title("Head Size vs Brain Weight")
    plt.xlabel("Head Size (cm^3)")
    plt.ylabel("Brain Weight (grams)")

    plt.legend()
    plt.grid()
    plt.show()

#-----------------------------------------------------------------------
# Entry point function
#-----------------------------------------------------------------------

def main():

    DataPath = "headbrain.csv"

    df = LoadData(DataPath)

    AnalyseData(df)

    X_train,X_test,Y_train,Y_test = SplitData(df)

    Model = TrainModel(X_train,Y_train)

    Y_pred = EvaluateModel(Model,X_test,Y_test)

    VisualizeData(X_test,Y_test,Y_pred)

if __name__=="__main__":
    main()

#---------------------------- End of Program ---------------------------
