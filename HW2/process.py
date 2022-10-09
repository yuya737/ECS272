import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv('pitches.csv')
    data = data.assign(xmid = (data['x0'] + data['px']) / 2 - data['pfx_x'] / 12)
    data = data.assign(zmid = (data['z0'] + data['pz']) / 2 - data['pfx_z'] / 12)
    data = data[['x0', 'xmid', 'z0', 'zmid', 'px', 'pz', 'pitch_type']]
    data.to_csv('temp.csv')

