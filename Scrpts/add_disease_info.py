import pandas as pd

# 加载2022_updated_IEIs.xlsx文件
ieis_df = pd.read_excel("2022_updated_IEIs.xlsx")

# 提取我们需要的列
ieis_df = ieis_df[['Genetic defect', 'Disease ', 'OMIM']]

# 对于Genetic defect列，我们需要把它转化为小写以便和其他文件一致
ieis_df['Genetic defect'] = ieis_df['Genetic defect'].str.lower()

# 定义四种突变类型
mutation_types = ['missense', 'nonsense', 'frameshift', 'splice_region_variant']

# 对于每种突变类型
for m_type in mutation_types:
    # 加载当前突变类型的csv文件
    variants_df = pd.read_csv(f"variants_individuals_{m_type}.csv")

    # 我们需要先抽取出gene名称，注意这里GeneEffects的格式是'GENE:effect'，如果不是，需要适当调整
    variants_df['gene'] = variants_df['GeneEffects'].apply(lambda x: x.split(':')[0].lower())

    # 将两个dataframe合并，根据gene列合并，使用left join保留所有variants_df中的行，对于ieis_df中没有的gene，disease和OMIM列会被填充为NaN
    merged_df = pd.merge(variants_df, ieis_df, left_on='gene', right_on='Genetic defect', how='left')

    # 删除临时的gene列
    merged_df.drop(columns=['gene'], inplace=True)

    # 将合并后的dataframe保存到新的csv文件
    merged_df.to_csv(f"variants_individuals_disease_OMIM_{m_type}.csv", index=False)

