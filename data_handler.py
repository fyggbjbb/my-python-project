import pandas as pd
import numpy as np

class DataHandler:
    def __init__(self):
        pass

    def handle_data(self, file_path):
        data = self.read_csv_file(file_path)
        data = self.preprocess_data(data)
        return data

    def read_csv_file(self, file_path):
        try:
            data = pd.read_csv(file_path, encoding='gbk')
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"文件{file_path}不存在")

    def preprocess_data(self, data):
        features = ['年纪', '性别', '购买金额', '历史购买次数', '购买频率']  # 补充购买金额，包含性别
        if not all(col in data.columns for col in features):  # 检查所有特征列是否存在
            raise KeyError("数据缺失必要列：历史购买次数、性别、购买金额、年纪、购买频率")

        # 性别编码
        gender_mapping = {'男': 1, '女': 0}
        data['性别'] = data['性别'].map(gender_mapping)

        # 购买频率编码（假设原代码频率映射逻辑保留）
        frequency_mapping = {
            'Bi - Weekly': 1,
            'Fortnightly': 1,
            'Every 3 Months': 3,
            'Quarterly': 3,
            'Annually': 4
        }
        data['购买频率'] = data['购买频率'].map(frequency_mapping).fillna(0)

        data[features] = data[features].replace([np.inf, -np.inf], np.nan).dropna()

        # 生成目标变量
        data['RepeatPurchase'] = 0
        data.loc[(data['历史购买次数'] > 20) & (data['购买频率'] < 3), 'RepeatPurchase'] = 1

        X = data[features]
        y = data['RepeatPurchase']
        return X, y

