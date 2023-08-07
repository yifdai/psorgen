import pandas as pd

# 定义四种突变类型
mutation_types = ['missense', 'frameshift']

# 创建一个空的DataFrame，用于存放所有的结果
result_df = pd.DataFrame()

# 对于每种突变类型
for m_type in mutation_types:
    # 加载当前突变类型的csv文件
    df = pd.read_csv(f"variants_individuals_disease_OMIM_case_control_{m_type}.csv")

    # 拆分SEX和AFT列，提取出Affected、Unaffected、Male、Female的数值
    df['Affected'] = df['AFT'].apply(lambda x: sum(int(i.split(':')[1]) for i in x.split('/') if 'Affected' in i))
    df['Unaffected'] = df['AFT'].apply(lambda x: sum(int(i.split(':')[1]) for i in x.split('/') if 'Unaffected' in i))
    df['Male'] = df['SEX'].apply(lambda x: sum(int(i.split(':')[1]) for i in x.split('/') if 'Male' in i))
    df['Female'] = df['SEX'].apply(lambda x: sum(int(i.split(':')[1]) for i in x.split('/') if 'Female' in i))

    # 删除原来的SEX、AFT和case/control ratio列
    df.drop(columns=['SEX', 'AFT', 'case/control ratio', 'NumberOfIEIGenes', 'NumberOfIndividuals'], inplace=True)

    # 按照GeneEffects列分组，并对Affected、Unaffected、Male、Female四列求和，同时将VariantID列的值合并到一起
    grouped_df = df.groupby('GeneEffects').agg({
        'Affected': 'sum',
        'Unaffected': 'sum',
        'Male': 'sum',
        'Female': 'sum',
        'VariantID': lambda x: ','.join(x)
    })

    # 计算新的case/control ratio
    grouped_df['case/control ratio'] = grouped_df['Affected'] / grouped_df['Unaffected']

    # 计算NumberOfVariant
    grouped_df['NumberOfVariant'] = grouped_df['VariantID'].apply(lambda x: len(x.split(',')))

    # 将处理后的结果添加到result_df中
    result_df = pd.concat([result_df, grouped_df])

# 将结果保存到新的csv文件
result_df.to_csv("merged_variants_individuals_disease_OMIM.csv")

