#-----------------------------------------------------------------------
# Project Name : Diabetes Detection System
# Description : Uses patient measurements to classify diabetes outcome for educational analysis.
# Author : Samruddhi Mandage
# Date : 05/11/2026
#-----------------------------------------------------------------------

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

Border = "-"*70

#-----------------------------------------------------------------------
# function name : LoadData
# Description : Load the diabetes dataset
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
# function name : PreprocessData
# Description : Handle invalid zero values
# Input : DataFrame
# Output : Updated DataFrame
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def PreprocessData(df):

    Columns = ["Glucose","BloodPressure","SkinThickness","Insulin","BMI"]

    for Col in Columns:
        if Col in df.columns:
            df[Col] = df[Col].replace(0,pd.NA)
            df[Col] = df[Col].fillna(df[Col].median())

    print("Missing values handled successfully")
    return df

#-----------------------------------------------------------------------
# function name : SplitData
# Description : Separate independent and dependent variables
# Input : DataFrame
# Output : Training and testing data
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def SplitData(df):

    X = df.drop("Outcome",axis=1)
    Y = df["Outcome"]

    X_train,X_test,Y_train,Y_test = train_test_split(
        X,Y,test_size=0.2,random_state=42,stratify=Y
    )

    print("Dataset splitting completed")
    return X_train,X_test,Y_train,Y_test

#-----------------------------------------------------------------------
# function name : FeatureScaling
# Description : Scale the independent variables
# Input : Training and testing features
# Output : Scaled features and scaler
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def FeatureScaling(X_train,X_test):

    Scaler = StandardScaler()

    X_train = Scaler.fit_transform(X_train)
    X_test = Scaler.transform(X_test)

    print("Feature scaling completed")
    return X_train,X_test

#-----------------------------------------------------------------------
# function name : TrainModel
# Description : Train Logistic Regression model
# Input : Training data
# Output : Trained model
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def TrainModel(X_train,Y_train):

    Model = LogisticRegression(max_iter=1000)

    Model = Model.fit(X_train,Y_train)

    print("Model trained successfully")
    return Model

#-----------------------------------------------------------------------
# function name : EvaluateModel
# Description : Evaluate model performance
# Input : Model and testing data
# Output : Accuracy and confusion matrix
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def EvaluateModel(Model,X_test,Y_test):

    Y_pred = Model.predict(X_test)

    print("Accuracy :",accuracy_score(Y_test,Y_pred))
    print("Confusion Matrix :")
    print(confusion_matrix(Y_test,Y_pred))
    print("Classification Report :")
    print(classification_report(Y_test,Y_pred))

#-----------------------------------------------------------------------
# Entry point function
#-----------------------------------------------------------------------

def main():

    DataPath = "diabetes.csv"

    df = LoadData(DataPath)
    df = PreprocessData(df)

    X_train,X_test,Y_train,Y_test = SplitData(df)
    X_train,X_test = FeatureScaling(X_train,X_test)

    Model = TrainModel(X_train,Y_train)

    EvaluateModel(Model,X_test,Y_test)

if __name__=="__main__":
    main()

#---------------------------- End of Program ---------------------------
