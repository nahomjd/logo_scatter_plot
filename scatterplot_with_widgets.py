import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os.path
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import glob
from rembg import remove 
from PIL import Image
from matplotlib.widgets import RadioButtons
import matplotlib.gridspec as gridspec

def getImage(path):
    
    return OffsetImage(plt.imread(path), zoom=0.015, alpha = 1)

ann_remove = []
def set_visible(label):
    print(ann_remove)
    for i in ann_remove:
        i.remove()
    ann_remove.clear()
    option_index = labels.index(label)
    print(option_index)
    print('length: ', len(views))
    for index, val in enumerate(views):
        print(index)
        if index == option_index:
            views[index].set_visible(True)
            for idx, row in df_list[index].iterrows():
                ab = AnnotationBbox(getImage(row['path']), (row['SOS'], row['Pace']), frameon=False)
                ann_remove.append(ab)
                ax.add_artist(ab)
            print('True')
            #print(index)
        else:
            views[index].set_visible(False)
        plt.draw()

df = pd.read_csv('CBB_2022_2023_season.csv')

df['Tournament'] = df['School'].map(lambda x: 1 if 'NCAA' in x else 0)
df['School_new'] = df['School'].str.replace('[^a-zA-Z0-9 -]', '', regex=True).str.replace(' ','-')\
.str.replace('NCAA', '').str.strip().str.lower().str.replace('--','-')

df['path'] = 'logos\\' + df['School_new'] + '.png'

def getImage(path):
    
    return OffsetImage(plt.imread(path), zoom=0.015, alpha = 1)
    
fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
#ax.scatter(df['SOS'], df['Pace'])#, color='white')

plt.subplots_adjust(bottom=0.2)


df_tournament = df.query('Tournament == 1')
df_no = df.query('Tournament == 0')


v0 = ax.scatter(df['SOS'], df['Pace'], color='white')
v1 = ax.scatter(df_tournament['SOS'],df_tournament['Pace'], color='white')
v2 = ax.scatter(df_no['SOS'],df_no['Pace'], color='white')

views = (v0,v1,v2)
df_list = (df, df_tournament, df_no)
#ax.set_xticks(df['SOS'])

ax_radio = plt.axes([0.25,0.01,0.28,0.16])
labels = ('All Teams', 'NCAA Teams', 'Non-NCAA Teams')
vis = (True, False, False)

print(ax_radio)
options = RadioButtons(ax_radio, labels)
options.on_clicked(set_visible)

for index, obj in enumerate(views):
    obj.set_visible(vis[index])

plt.show()
