#-----------------------------------------------------------------------
# Project Name : Loan Approval Prediction System
# Description : Predicts loan approval status from applicant and loan information.
# Author : Samruddhi Mandage
# Date : 05/11/2026
#-----------------------------------------------------------------------

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

Border = "-"*70

#-----------------------------------------------------------------------
# function name : LoadData
# Description : Load loan prediction dataset
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
# Description : Handle missing values and categorical columns
# Input : DataFrame
# Output : Updated DataFrame
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def PreprocessData(df):

    df = df.drop(columns=["Loan_ID"],errors="ignore")

    for Col in df.columns:
        if df[Col].dtype == "object":
            df[Col] = df[Col].fillna(df[Col].mode()[0])
        else:
            df[Col] = df[Col].fillna(df[Col].median())

    df = pd.get_dummies(df,drop_first=True,dtype=int)

    print("Data preprocessing completed")
    return df

#-----------------------------------------------------------------------
# function name : SplitData
# Description : Split features and target column
# Input : DataFrame
# Output : Training and testing data
# Author : Samruddhi Mandage
#-----------------------------------------------------------------------

def SplitData(df):

    X = df.drop("Loan_Status_Y",axis=1)
    Y = df["Loan_Status_Y"]

    X_train,X_test,Y_train,Y_test = train_test_split(
        X,Y,test_size=0.2,random_state=42,stratify=Y
    )

    print("Dataset splitting completed")
    return X_train,X_test,Y_train,Y_test

#-----------------------------------------------------------------------
# function name : TrainModel
# Description : Train Random Forest classifier
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
# Description : Evaluate loan approval predictions
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

    DataPath = "train.csv"

    df = LoadData(DataPath)
    df = PreprocessData(df)

    X_train,X_test,Y_train,Y_test = SplitData(df)

    Model = TrainModel(X_train,Y_train)

    EvaluateModel(Model,X_test,Y_test)

if __name__=="__main__":
    main()

#---------------------------- End of Program ---------------------------
