import pandas as pd
import os


file_path = '/Users/travisclarke/Documents/Masters/MaFIA EtOH Images/New Mafia/results'
csv_path = os.path.join(file_path, 'results.csv')
data = pd.read_csv(csv_path)
print('done')