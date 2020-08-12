import csv
import json
import pandas as pd

sourceDataViews = "Views.csv"
destDataViews = "LogViews.json"

csvfilepd = pd.read_csv(sourceDataViews).sort_values(by='timestamp', ascending=False)
csvfilepd.to_json(destDataViews, orient = 'records')
