import pandas as pd
import os

os.chdir('/mnt/d/rwork/alex')

# 加载VICTOR.sample_spc文件
victor_df = pd.read_csv("VICTOR.sample_spc", sep="\t")

# 为每个CSV文件添加新列
mutation_types = ['missense', 'nonsense', 'frameshift', 'splice_region_variant'] # 定义四种突变类型
for m_type in mutation_types:
    df = pd.read_csv(f"variants_individuals_{m_type}.csv")

    # 创建新的列，初始化为空字符串
    df["SEX"] = ""
    df["AFT"] = ""
    df["VICPOP"] = ""

    # 更新每一行的SEX, AFT, VICPOP列
    for index, row in df.iterrows():
        individuals = row["Individuals"].split(",")
        sex_counts = victor_df.loc[victor_df["SeqID"].isin(individuals), "Sex"].value_counts()
        aft_counts = victor_df.loc[victor_df["SeqID"].isin(individuals), "Aff"].value_counts()
        vicpop_counts = victor_df.loc[victor_df["SeqID"].isin(individuals), "victorPop"].value_counts()

        df.at[index, "SEX"] = "/".join([f"{k}:{v}" for k, v in sex_counts.items()])
        df.at[index, "AFT"] = "/".join([f"{k}:{v}" for k, v in aft_counts.items()])
        df.at[index, "VICPOP"] = "/".join([f"{k}:{v}" for k, v in vicpop_counts.items()])

    # 保存修改后的DataFrame到CSV
    df.to_csv(f"variants_individuals_{m_type}.csv", index=False)

