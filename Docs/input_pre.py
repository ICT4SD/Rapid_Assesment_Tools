import pandas as pd
path = '/Users/Maxwell/PycharmProjects/Github/Rapid_Assessment_Tools/SharedFiles/Fordham/RIA Bhutan/Docs Reviewed/Bhutan_Input.txt'

with open(path, 'r') as f:
    text = f.read()


df = pd.DataFrame([context.strip().split(' ', 1) for context in text.split(sep='*****')], columns=['sector', 'text'])

df.to_csv('bhutan_input.csv')

