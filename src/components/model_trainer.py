import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass

from sklearn.linear_model import LinearRegression,Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error , r2_score, accuracy_score, confusion_matrix
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

from catboost import CatBoostRegressor
from xgboost import XGBRegressor


from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class ModelTrainerConfig:
    model_path = os.path.join("artifacts","model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def intiate_model_training(self,train_arr,test_arr):
        try:
            logging.info("Model Training is Started")
            models ={
                "Linear Regression": LinearRegression(),
                "Ridge Regression": Ridge(),
                "Lasso Regression": Lasso(),
                "Decision Tree Regressor": DecisionTreeRegressor(),
                "Random Forest Regressor": RandomForestRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
                "GradientBoosting Regressor": GradientBoostingRegressor(),
                "KNeighbors Regressor": KNeighborsRegressor(),
                "CatBoost Regressor": CatBoostRegressor(verbose=False),
                "XGB Regressor": XGBRegressor()
            }

            X_train = train_arr[:,:-1]
            X_test = test_arr[:,:-1]

            y_train = train_arr[:,-1]
            y_test = test_arr[:,-1]
            logging.info("Training and Testing array is divided into X-train,test and Y-train,test")

            report = {}

            for i in range(len(models)):

                model = list(models.values())[i]

                model.fit(X_train,y_train)

                y_test_pred = model.predict(X_test)

                score = r2_score(y_test,y_test_pred)

                # print("=============================================")
                # print(f"The Model name is: {list(models.keys())[i]}")

                # print(f"Mean absolute error: {mean_absolute_error(y_test,y_test_pred)}")
                # print(f"Mean squared error: {mean_squared_error(y_test,y_test_pred)}")
                # print(f"Root Mean squared error: {np.sqrt(mean_squared_error(y_test,y_test_pred))}")
                # print("\n")
                # print(f"The R2 Score for Model is: {score}")
                # print("=============================================")
                # print("\n")
                report[list(models.keys())[i]]=score
            logging.info("Fit and Predict Performed on each Model")
            

            report_sort = {k: v for k, v in sorted(report.items(), key=lambda x: x[1],reverse=True)}

            best_model_name = list(report_sort.keys())[0]
            best_model_r2 = list(report_sort.values())[0]
            best_model = models[best_model_name]

            logging.info("Best Model and its R2_Scorer found")


            # print(pd.DataFrame(report_sort,index=[0]).T)
            print(f"The Best Model name is: {best_model_name} with R2_Score: {best_model_r2}")
            print(f"Best model is: {best_model}")
            
            logging.info("Model training is completed")
            # From the above Fit and Predict, We got to know that Catboost Model is having highest r2_score so now we are applying hyper tunning on the CatBoost Regressor

            logging.info("Hyperparameter tunning is statred")
            loss_function=['RMSE']
            iterations = [int(x) for x in np.linspace(start=100,stop=2000,num=20)]
            learning_rate = [0.01,0.05,0.1,0.25,0.5,0.8,0.9]
            depth = [1,3,5,6,7,8]
            l2_leaf_reg = [2,5,10,15,20,30]
            random_state= 42

            params = {
                "loss_function": loss_function,
                "iterations": iterations,
                "learning_rate": learning_rate,
                "depth": depth,
                "l2_leaf_reg": l2_leaf_reg,
                # "random_state": random_state
            }

            logging.info("First Randomnized CV is used to find best hyper parameter")
            Random_cv = RandomizedSearchCV(estimator=best_model,param_distributions=params,cv=3,n_iter=100,n_jobs=-1,verbose=1,random_state=42)

            Random_cv.fit(X_train,y_train)

            best_random_grid = Random_cv.best_estimator_

            print(Random_cv.best_params_)

            y_pred = best_random_grid.predict(X_test)

            print(f"R2 Score for Random CV: {r2_score(y_test,y_pred)}")
            logging.info("Randomnized CV is Completed")


            param_grid = {
                "loss_function": [Random_cv.best_params_["loss_function"]],
                "iterations": [Random_cv.best_params_['iterations']-100,Random_cv.best_params_['iterations'],Random_cv.best_params_['iterations']+100],
                "learning_rate": [Random_cv.best_params_['learning_rate']-0.09, Random_cv.best_params_['learning_rate']-0.05, Random_cv.best_params_['learning_rate'], Random_cv.best_params_['learning_rate']+0.05,Random_cv.best_params_['learning_rate']+0.1],
                "depth": [ Random_cv.best_params_['depth']-1, Random_cv.best_params_['depth'], Random_cv.best_params_['depth']+1],
                "l2_leaf_reg": [ Random_cv.best_params_['l2_leaf_reg']-5, Random_cv.best_params_['l2_leaf_reg'], Random_cv.best_params_['l2_leaf_reg']+5,]
            }

            logging.info("GridSearch CV is loaded")
            Grid_cv = GridSearchCV(estimator=best_model,param_grid=param_grid,cv=3,n_jobs=-1,verbose=1)

            Grid_cv.fit(X_train,y_train)

            print(Grid_cv.best_estimator_)
            best_grid = Grid_cv.best_estimator_

            y_pred_grid = best_grid.predict(X_test)

            print(f"R2 Score for GridSearch: {r2_score(y_test,y_pred_grid)}")

            logging.info("GridSearchCV is Complete")

            logging.info("Hyperparameter tunning is ended")

            save_object(
                self.model_trainer_config.model_path,
                best_model
            )

            return best_model_r2,best_model_name

        except Exception as e:
            raise CustomException(e,sys)


