## developed by soraya remaili
import pandas as pd

megaCSV = pd.read_csv("./csv_clean/megaCSV.csv")
megaCSV['xt_ocean'] = megaCSV['xt_ocean'] -360
megaFilter = megaCSV.groupby(['xt_ocean', 'yt_ocean'], as_index=False).agg({'st_ocean': 'max'})
megaFilter.to_csv('./csv_clean/megaFilter.csv', index=False, float_format='%.10f')
