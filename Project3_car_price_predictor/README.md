# File Descriptions

## data_cleaning.ipynb
Input: quikr_car.csv
Process: Data Cleaning
Output: cleaned_car.csv

## model.ipynb
regression model built
uses the clean csv file,
OHE as the encoder, ColumnTransformer and Pipeline
r2_score as the metrics,
checks which random state gives highest accuracy, uses numpy to extract it
extracts the model as a pickle file