import pandas as pd
import csv
import os
import gzip
import re

os.chdir('/mnt/d/rwork/alex')

vcf_file = "rare_raw.vcf.gz"  # 你的VCF文件
iei_file = "2022_updated_IEIs.xlsx"  # 你的IEI文件

# 从IEI文件中读取基因列表
iei_df = pd.read_excel(iei_file)
iei_genes = set(iei_df["Genetic defect"].str.strip())  # 去除空格并转换为集合以便之后的比较

mutation_types = ['missense', 'nonsense', 'frameshift', 'splice_region_variant']  # 根据你的VCF文件修改这个列表
individuals_dict = {mutation_type: dict() for mutation_type in mutation_types}
individuals = []

with gzip.open(vcf_file, "rt") as vcf:  # 注意这里使用了gzip.open，并且模式为"rt"，意为读取文本
    for line in vcf:
        if line.startswith("##"):  # 跳过注释行
            continue
        if line.startswith("#"):  # 获取个体名字
            individuals = line.strip().split("\t")[9:]
            continue
        fields = line.strip().split("\t")
        variant_id = fields[2]
        genotype_data = fields[9:]
        info_fields = dict(x.split("=", 1) for x in fields[7].split(";") if "=" in x)
        if "vAnnGeneAll" in info_fields:
            gene_effects = info_fields["vAnnGeneAll"].split(",")
            variant_individuals = [individuals[i] for i, data in enumerate(genotype_data) if data.split(":")[0] != "0/0"]  # 检查基因型是否为非野生型
            if variant_individuals:
                for i in range(0, len(gene_effects), 3):
                    gene = gene_effects[i]
                    mutation_type = gene_effects[i + 1].lower()
                    if gene in iei_genes:
                        for m_type in mutation_types:
                            if m_type in mutation_type:
                                gene_effect = gene + ":" + mutation_type
                                if variant_id not in individuals_dict[m_type]:
                                    individuals_dict[m_type][variant_id] = [[], []]
                                if gene_effect not in individuals_dict[m_type][variant_id][0]:
                                    individuals_dict[m_type][variant_id][0].append(gene_effect)
                                individuals_dict[m_type][variant_id][1].extend(variant_individuals)

# 将结果写入到CSV文件
for m_type in mutation_types:
    with open(f"variants_individuals_{m_type}.csv", "w") as out:  # 生成的文件名将包含突变类型
        writer = csv.writer(out)
        writer.writerow(["VariantID", "GeneEffects", "NumberOfIEIGenes", "NumberOfIndividuals", "Individuals"])
        for variant_id, (gene_effects, variant_individuals) in individuals_dict[m_type].items():
            writer.writerow([variant_id, ",".join(gene_effects), len(set(gene.split(':')[0] for gene in gene_effects)), len(set(variant_individuals)), ",".join(set(variant_individuals))])

