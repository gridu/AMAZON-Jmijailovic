import csv
import json
import pandas as pd

sourceDataReviews = "Reviews.csv"
destDataReviews = "LogReviews.json"

csvfilepd = pd.read_csv(sourceDataReviews).sort_values(by='timestamp', ascending=False)
csvfilepd.to_json(destDataReviews, orient = 'records')
