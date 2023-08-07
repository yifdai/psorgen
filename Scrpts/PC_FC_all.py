import pandas as pd

# 加载VICTOR.sample_spc文件
victor_df = pd.read_csv("VICTOR.sample_spc", sep="\t")

# 定义四种突变类型
mutation_types = ['missense', 'nonsense', 'frameshift', 'splice_region_variant']

# 用于存放所有从四个csv文件中获取的样本ID
all_sample_ids = []

# 读取四个csv文件
for m_type in mutation_types:
    df = pd.read_csv(f"variants_individuals_{m_type}.csv")
    for ids in df["Individuals"]:
        all_sample_ids.extend(ids.split(','))

# 去重
unique_sample_ids = list(set(all_sample_ids))

# 创建新的DataFrame，只包含从四个csv文件中获取的样本ID的行
filtered_df = victor_df[victor_df["SeqID"].isin(unique_sample_ids)]

# 输出到新的csv文件
filtered_df.to_csv("filtered_VICTOR.sample_spc.csv", index=False)
