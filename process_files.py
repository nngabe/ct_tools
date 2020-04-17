## 04/2020 Nicholas A. Gabriel

import os
import pandas as pd


def process_files(in_dir, out_dir):
  """Take raw files from crowdtangle and process them for text analysis

    Args:
    in_dir (str)
    out_dir (str)

    Out:
    out_files in format uid_endDate.csv
  """
  start_dir = os.getcwd()
  # expand ~ into user directory
  in_dir = os.path.expanduser(in_dir)
  out_dir = os.path.expanduser(out_dir)
  # go to directory with raw files
  os.chdir(in_dir)
  files = os.listdir('.')
  # can choose whatever columns are wanted here
  cols = ['Created', 'Type', 'Likes', 'Comments', 'Shares', 'Post Views', 'Total Views', 'text']
  for f in files:
    try:
      df = pd.read_csv(f)
      date = ''.join(f.split('-')[0:3])
      uid = str(df.loc[0,'Facebook Id'])
      out_file = uid + '_' + date + '.csv'
      df['text'] = df.loc[:,'Message'].fillna(' ') + df.loc[:,'Description'].fillna(' ') + df.loc[:,'Link Text'].fillna(' ')
      doc = df.loc[:,cols]
      doc.to_csv(out_dir + out_file)
    except Exception as e:
      print(e)

  os.chdir(start_dir)

if __name__ == '__main__':

  in_dir = '~/ctfiles/'
  out_dir = '~/post_data/'
  process_files(in_dir, out_dir)
