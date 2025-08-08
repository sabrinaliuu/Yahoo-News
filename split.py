import pandas as pd
import re

data = pd.read_csv("./output.csv")
output ={
            "id_key": [],
            "title": [],
            "time": [],
            "para": []
        }

for r in range(len(data)):
    url = data['url'].iloc[r]
    id = data['id'].iloc[r]
    post = data['post'].iloc[r]
    title = data['title'].iloc[r]
    time = data['time'].iloc[r]
    
    
    if url.find('images')==-1:

        text = post.replace('\u3000','').replace('\r\n','\n\n')
        text = re.split(r'\n\n', text)
        text = [item for item in text if item.strip()]
        #print(text)
      
        for j in range(len(text)):
            output['id_key'].append(id+'-'+str(j+1))
            output['title'].append(title)
            output['time'].append(time)
            output['para'].append(text[j])
## Save the data ##
import csv

## save csv file ##
with open('./output_split.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['id_key','title','time','para'])
    
    for i in range(len(output['id_key'])):
        output_row = [output['id_key'][i], output['title'][i], output['time'][i], output['para'][i]]
        writer.writerow(output_row)

## or save json file ##
import json
pd.DataFrame(output).to_json("output_split.json", orient="records", force_ascii=False, indent=4)
        
            

