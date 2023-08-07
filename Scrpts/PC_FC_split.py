import pandas as pd

# 加载VICTOR.sample_spc文件
victor_df = pd.read_csv("VICTOR.sample_spc", sep="\t")

# 定义四种突变类型
mutation_types = ['missense', 'nonsense', 'frameshift', 'splice_region_variant']

# 读取四个csv文件
for m_type in mutation_types:
    # 加载当前突变类型的csv文件
    df = pd.read_csv(f"variants_individuals_{m_type}.csv")

    # 从当前csv文件中获取所有样本ID
    sample_ids = []
    for ids in df["Individuals"]:
        sample_ids.extend(ids.split(','))

    # 去重
    unique_sample_ids = list(set(sample_ids))

    # 创建新的DataFrame，只包含当前csv文件中获取的样本ID的行
    filtered_df = victor_df[victor_df["SeqID"].isin(unique_sample_ids)]

    # 输出到新的csv文件，文件名对应当前突变类型
    filtered_df.to_csv(f"filtered_VICTOR.sample_spc_{m_type}.csv", index=False)

