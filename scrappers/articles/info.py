import pandas as pd

fox_george = pd.read_json('./george-floyd-url-fox.json')
cnn_george = pd.read_json('./george-floyd-url-cnn.json')
print(fox_george.columns)
print(cnn_george.columns)