# Install gspread to import data from Google Sheets
!pip install --upgrade -q gspread



from google.colab import drive

drive.mount('/content/gdrive')



import os, json
import pandas as pd

root_path = '/content/gdrive/My Drive/Kering Datasets/'

json_resp = []
all_everything = { "types": [], "scores": [], "im_urls": []}
im_names = []

for root, dirs, files in os.walk(root_path):
  for file in files:
    with open(os.path.join(root, file), 'r') as f:
      json_arr = json.load(f)
      for obj in json_arr:
        user_agent = obj['jsonPayload']['user_agent'].strip('\'\'\'')
        if 'LUCE' in user_agent:
          im_url = obj['jsonPayload']['im_url'].strip('\'\'\'')
          json_resp = obj['jsonPayload']['response']
          json_resp = json.loads(json_resp.strip('\'\'\''))

          if 'objects' in json_resp:
            for resp_type in json_resp['objects']:
              all_everything['types'].append(resp_type['type'])
              all_everything['scores'].append(resp_type['score'])
              all_everything['im_urls'].append(im_url)
              count = 0
              for results in resp_type['result']:
                im_name = results['im_name']
                if (".jpg" not in im_name):
                  im_names.append(im_name)
                  count = count + 1
                  if (count == 4):
                    break
              break
    
df = pd.DataFrame.from_dict(all_everything)
df.to_csv(index=False, path_or_buf="./searches.csv")
# print(df.head(10))


# Plot the count of primary products being searched
df_types = df
df_types = df_types[df.types != 'other']
df_types = df_types[df.types != '']
types_plot = df_types['types'].value_counts()
print(types_plot.plot.bar())


# Plot the average scores of each category
df_scores = df
df_scores = df_scores[df.types != 'other']
df_scores = df_scores[df.types != '']
scores_plot = df_scores.groupby('types')['scores'].mean()
print(scores_plot.sort_values(ascending=False).plot.bar())



# Plot most recommended products
df_im_names = pd.DataFrame(im_names)
df_im_names[0].value_counts()
# im_names_plot = df_im_names[0].value_counts()
# print(im_names_plot.plot.bar())