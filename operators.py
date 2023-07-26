import numpy as np
np.warnings.filterwarnings('ignore')


def lag(series, periods=1):
    '''
    將序列值落後一期。
    '''
    series = np.roll(series, shift=periods)
    # np.roll會把最後的值捕到最前面，因此要把前面值變成nan
    series[: periods] = np.nan
    return series


def rolling_window(series, windows):
    '''
    模仿pandas.rolling用法，但底層是由numpy形成。
    (運作邏輯可參考以下網址)
    '''
    # 參考https://stackoverflow.com/questions/6811183/rolling-window-for-1d-arrays-in-numpy
    shape = series.shape[:-1] + (series.shape[-1] - windows + 1, windows)
    strides = series.strides + (series.strides[-1],)
    
    # 在上述方法下，將只會算出移動後的情況，例如：series的len為5，移動窗格為3
    # series為[1, 2, 3, 4, 5]，經由上面做法會產出
    # [
    #  [1, 2, 3],
    #  [2, 3, 4],
    #  [3, 4, 5]
    # ]
    # 但實際序列有5個值因此以下在前面設定nan
    # [
    #  [nan, nan, nan],
    #  [nan, nan, nan]
    # ]
    # 以下依據上述邏輯，產生兩個array後再疊一起
    # nan的shape size為(windows-1, windows)
    # 其中x為windows-1，因為第windows個時便可以開始運算，所以只有windows-1
    # Y由於給定窗格為大小為windiws，因此為windiws
    na_array = np.empty(shape=(windows-1, windows))
    na_array[:] = np.nan
    
    rolled_array = np.lib.stride_tricks.as_strided(
        series, shape=shape, strides=strides
    )
    
    result = np.vstack((na_array, rolled_array))
    
    return result