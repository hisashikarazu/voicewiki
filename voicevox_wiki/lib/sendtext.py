import time


import pandas as pd


def to_csv(from_wiki):
    wday_list = from_wiki[0]
    url = from_wiki[1]
    wday_dict = {wday_list[0][:6]: wday_list[0][7:]}

    i=0
    for s in wday_list:
        wday_dict[i+1] = wday_list[i]
        if i == len(wday_list)-1:
            wday_dict['from:'] = url
        i=i+1
    
    dir = '../csv'
    csv_name = time.strftime('%m%d')
    csv_path = f'{dir}/{csv_name}.csv'

    pd.DataFrame([
        {"k":k, "v":v}
        for k,v in wday_dict.items()
    ]).to_csv(csv_path)

    print({row.k:row.v for idx,row in pd.read_csv(csv_path).iterrows()})