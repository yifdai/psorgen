import pandas as pd
import csv
import os
import gzip

os.chdir('/mnt/d/rwork/alex')

vcf_file = "rare_raw.vcf.gz"  # 你的VCF文件
iei_file = "2022_updated_IEIs.xlsx"  # 你的IEI文件
output_file = "intersect_IEIs.csv"  # 输出的CSV文件

# 从IEI文件中读取基因列表
iei_df = pd.read_excel(iei_file)
iei_genes = {gene.strip(): iei_df[iei_df["Genetic defect"].str.strip() == gene.strip()].iloc[0].tolist() for gene in iei_df["Genetic defect"].str.strip()}  # 创建一个字典，键为基因名，值为IEI文件中的行

# 从VCF文件中读取基因列表
vcf_genes = dict()
info_dict = dict()
with gzip.open(vcf_file, "rt") as vcf:  # 注意这里使用了gzip.open，并且模式为"rt"，意为读取文本
    for line in vcf:
        if line.startswith("#"):  # 跳过注释行
            continue
        fields = line.strip().split("\t")
        info_fields = dict(x.split("=", 1) for x in fields[7].split(";") if "=" in x)
        if "vAnnGeneAll" in info_fields:
            gene_effects = info_fields["vAnnGeneAll"].split(",")
            for i in range(0, len(gene_effects), 3):
                gene = gene_effects[i]
                mutation_type = gene_effects[i + 1]
                variant_id = fields[2]
                if gene in iei_genes:
                    id_with_mutation = f"{variant_id}##{mutation_type}"
                    if gene not in vcf_genes:
                        vcf_genes[gene] = [id_with_mutation]
                    else:
                        vcf_genes[gene].append(id_with_mutation)
                    # Collect info for each variant
                    id_with_info = f"{variant_id}##{fields[7]}"
                    if gene not in info_dict:
                        info_dict[gene] = [id_with_info]
                    else:
                        info_dict[gene].append(id_with_info)

# 找出同时出现在两个文件中的基因
common_genes = set(iei_genes.keys()).intersection(set(vcf_genes.keys()))

# 将结果写入到CSV文件
with open(output_file, "w") as out:
    writer = csv.writer(out)
    # 首先获取IEI文件的列名，然后添加VCF文件中的信息列名
    header = list(iei_df.columns) + ["Mutation_with_VariantID_VCF", "INFO_VCF"]
    writer.writerow(header)
    for gene in common_genes:
        # 将带有变异类型和variant id的列表转换为字符串
        id_with_mutation_str = "; ".join(vcf_genes[gene])
        id_with_info_str = "; ".join(info_dict[gene])
        row = iei_genes[gene] + [id_with_mutation_str, id_with_info_str]
        writer.writerow(row)

