import pandas as pd
import numpy as np

def parse_ratio(ratio_str):
    ratios = ratio_str.split('/')
    affected = 0
    unaffected = 0
    for ratio in ratios:
        if 'Affected' in ratio:
            affected = int(ratio.split(':')[1])
        if 'Unaffected' in ratio:
            unaffected = int(ratio.split(':')[1])
    if unaffected == 0:
        return np.nan
    else:
        return affected / unaffected

# 定义四种突变类型
mutation_types = ['missense', 'nonsense', 'frameshift', 'splice_region_variant']

# 对于每种突变类型
for m_type in mutation_types:
    # 加载当前突变类型的csv文件
    variants_df = pd.read_csv(f"variants_individuals_disease_OMIM_{m_type}.csv")

    # 计算case/control ratio
    variants_df['case/control ratio'] = variants_df['AFT'].apply(parse_ratio)

    # 将新的dataframe保存到新的csv文件
    variants_df.to_csv(f"variants_individuals_disease_OMIM_case_control_{m_type}.csv", index=False)
