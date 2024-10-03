## End to End Flight Price Prediction Project

Project Steps:-
1) Creating a git repository and adding the license in it
2) Creating a new environment for the project by VS Code
3) Creating the README file on VS Code
4) Linking this git repository to the VS Code and perform the first commit
5) Adding gitignore file
    5.1 *.log - for ignoring all the log files
    5.2 artifacts/ - for ignoring the whole folder
6) Adding requirements.txt file (with -e . in the end so that requirements.txt will initialize the setup.py)
7) Adding setup.py file so that we can use local folder as a package itself
8) Adding Source folder and init file in it
9) Adding sub folder to the source folder
    9.1 Components
        9.1.1 Data Ingestion
        9.1.2 Data Transformation
        9.1.3 Model Trainer
    9.2 Pipelines
        9.2.1 Training Pipeline
        9.2.2 Prediction Pipeline
    9.3 Logging
    9.4 Exception
    9.5 Utils
10) Writing the code for custom exception
11) Writing the code for logging
12) Expolatory Data Analysis(EDA) done on jupyter notebook
    12.1 Dealing with missing value
    12.2 Correlation between features
    12.3 Column conversion into meaningfull insight
    12.4 Graph plotting for Univariate, Bivariate and Multivariate
    12.5 Train test split
    12.6 Categorical variable encoding
    12.7 Model selection
    12.8 Training the model
    12.9 Prediction from model
13) Data Ingestion
14) Data Cleaning
15) Data Transformation
16) Model Training
    16.1 Model selection
    16.2 Hyper parameter tunning
    16.3 Saving the Model
17) Creating app.py for API
18) Writing Model Prediction Pipeline and linking with app.py
19) Deployment with AWS by using gitHub action