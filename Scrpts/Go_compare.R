# load required libraries
library(data.table)
library(org.Hs.eg.db)
library(clusterProfiler)
library(enrichplot)
library(ggplot2)
library(tidyverse)
library(xlsx)

setwd("D:/rwork/alex/psorgen-old")

# read csv file
df1 <- read.xlsx("pso_gene.xlsx", sheetName = "Sheet1")

# extract gene names and remove duplicates
genes_pso <- df1$Gene.name

# map to EntrezID
genes_pso <- bitr(genes_pso, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)
genes_pso <- na.omit(genes_pso)

# perform GO enrichment analysis
ego_pso <- enrichGO(gene = genes_pso$ENTREZID, OrgDb = org.Hs.eg.db, keyType = "ENTREZID", ont="ALL", pAdjustMethod = "BH", pvalueCutoff = 0.05, qvalueCutoff = 0.05)

# read csv file
df2 <- fread("merged_variants_individuals_disease_OMIM.csv")

# extract gene names and remove duplicates
genes_rare <- unique(sub(":.+$", "", df2$GeneEffects))

# map to EntrezID
genes_rare <- bitr(genes_rare, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)
genes_rare <- na.omit(genes_rare)

# perform GO enrichment analysis
ego_rare <- enrichGO(gene = genes_rare$ENTREZID, OrgDb = org.Hs.eg.db, keyType = "ENTREZID", ont="ALL", pAdjustMethod = "BH", pvalueCutoff = 0.05, qvalueCutoff = 0.05)


ego_compare <- compareCluster(list(rare = genes_rare$ENTREZID, pso = genes_pso$ENTREZID), fun = "enrichGO", OrgDb = org.Hs.eg.db, ont = "BP")

dotplot(ego_compare, showCategory = 50)


# get the enriched GO terms
pso_go_terms <- ego_pso$Description
rare_go_terms <- ego_rare$Description

# find the common terms
common_terms <- intersect(pso_go_terms, rare_go_terms)

ego_compare <- compareCluster(ego_list, fun = "enrichGO", OrgDb = org.Hs.eg.db)
print(ego_compare)
# Subset the results for common terms
ego_compare_common <- subset(ego_compare, Description %in% common_terms)

# Visualize with dotplot
dotplot(ego_compare_common, showCategory = 50)

# Get the GO term IDs from the comparison
go_ids <- ego_compare$ID

# Find the matching descriptions from the original enrichment results
pso_descriptions <- subset(ego_pso, ID %in% go_ids)$Description
rare_descriptions <- subset(ego_rare, ID %in% go_ids)$Description

# Get the common descriptions
common_descriptions <- intersect(pso_descriptions, rare_descriptions)

# Subset the comparison results for common descriptions
ego_compare_common <- ego_compare[ego_compare$ID %in% common_descriptions, ]

# Visualize with dotplot
dotplot(ego_compare_common, showCategory = 50)


