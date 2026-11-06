#-----------------------------------------------------------------------
# Project Name : Ad Click Prediction System
# Description : Predicts whether a user will click on an online advertisement.
# Author : Samruddhi Mandage
# Date : 05/11/2026
#-----------------------------------------------------------------------

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
from sklearn.ensemble import RandomForestClassifier

Border = "-"*70

#-----------------------------------------------------------------------
# function name : LoadData
# Description : Load the dataset from CSV file
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
# Description : Clean the data and prepare features
# Input : DataFrame
# Output : Updated DataFrame
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def PreprocessData(df):

    df = df.drop(columns=["Ad Topic Line","City","Country","Timestamp"],errors="ignore")

    df = df.dropna(subset=["Clicked on Ad"])

    print("Data preprocessing completed")
    print(df.head())

    return df

#-----------------------------------------------------------------------
# function name : SplitData
# Description : Split data into training and testing subsets
# Input : DataFrame
# Output : X_train, X_test, Y_train, Y_test
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def SplitData(df):

    X = df.drop("Clicked on Ad",axis=1)
    Y = df["Clicked on Ad"]

    X = pd.get_dummies(X,drop_first=True,dtype=int)

    X = X.fillna(X.median())

    X_train,X_test,Y_train,Y_test = train_test_split(
        X,Y,test_size=0.2,random_state=42,stratify=Y
    )

    print("Dataset splitting completed successfully")
    return X_train,X_test,Y_train,Y_test

#-----------------------------------------------------------------------
# function name : TrainModel
# Description : Train Random Forest classification model
# Input : Training features and labels
# Output : Trained model
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def TrainModel(X_train,Y_train):

    Model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    Model = Model.fit(X_train,Y_train)

    print("Model trained successfully")
    return Model

#-----------------------------------------------------------------------
# function name : EvaluateModel
# Description : Evaluate the trained model
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

    DataPath = "advertising.csv"

    df = LoadData(DataPath)
    df = PreprocessData(df)

    X_train,X_test,Y_train,Y_test = SplitData(df)

    Model = TrainModel(X_train,Y_train)

    EvaluateModel(Model,X_test,Y_test)

if __name__=="__main__":
    main()

#---------------------------- End of Program ---------------------------
