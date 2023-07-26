import pandas as pd
import os


def formatting_data(file_name):
    '''
    將Cmoney的資料整理成程式可用之格式。
    '''
    path = 'raw_data/{}'.format(file_name)
    # encoding的類別有點特別
    data = pd.read_csv(path, encoding='cp950', low_memory=False)
    # 此row含有日期，指定為columns name
    data.columns = data.iloc[0, ]
    # 把不必要的row刪除(cmoney下載資料過程產生的欄位)
    data.drop(index=[0, 1, 2, 3], inplace=True)
    # 此column含有股票代碼，指定為index
    data.index = data.iloc[:, 0].values
    # 把不必要的columns刪掉
    data.drop(columns=['基準日:最近一日', '資料日期/'], inplace=True)
    # 更改路徑，把資料存到指定資料夾
    os.chdir('data')
    data.to_csv(file_name.split('.csv')[0]+'_已格式化'+'.csv')
    print('資料： 「{}」已初始化並儲存！'.format(file_name))
    print('最新資料日期為: {}'.format(data.columns[-1]))
    # 回到上層資料夾，否則會讀不到資料
    os.chdir('..')