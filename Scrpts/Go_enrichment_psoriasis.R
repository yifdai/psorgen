# load required libraries
library(data.table)
library(org.Hs.eg.db)
library(clusterProfiler)
library(enrichplot)
library(ggplot2)
library(pheatmap)
library(tidyverse)
library(xlsx)

setwd("D:/rwork/alex/psorgen-old")

# read csv file
df <- read.xlsx("pso_gene.xlsx", sheetName = "Sheet1")

# extract gene names and remove duplicates
genes <- df$Gene.name

# map to EntrezID
genes <- bitr(genes, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)
genes <- na.omit(genes)

# perform GO enrichment analysis
ego <- enrichGO(gene = genes$ENTREZID, OrgDb = org.Hs.eg.db, keyType = "ENTREZID", ont="ALL", pAdjustMethod = "BH", pvalueCutoff = 0.05, qvalueCutoff = 0.05)

# plot gene-concept network
ego2 <- pairwise_termsim(ego)
emapplot(ego2, node_label_cex = 1.2, node_label_repel = TRUE)

ego_df <- as.data.frame(ego)

# plot dotplot of GO enrichment analysis
dotplot(ego, showCategory=10)

# plot barplot of GO enrichment analysis
barplot(ego, showCategory=10)

GO_BP<-enrichGO( genes$ENTREZID,#GO富集分析BP模块
                 OrgDb = org.Hs.eg.db,
                 keyType = "ENTREZID",
                 ont = "BP",
                 pvalueCutoff = 0.05,
                 pAdjustMethod = "BH",
                 qvalueCutoff = 0.05,
                 minGSSize = 10,
                 maxGSSize = 500,
                 readable = T)
plotGOgraph(GO_BP)#GO-BP功能网络图
GO_CC<-enrichGO( genes$ENTREZID,#GO富集分析CC模块
                 OrgDb = org.Hs.eg.db,
                 keyType = "ENTREZID",
                 ont = "CC",
                 pvalueCutoff = 0.05,
                 pAdjustMethod = "BH",
                 qvalueCutoff = 0.05,
                 minGSSize = 10,
                 maxGSSize = 500,
                 readable = T)
plotGOgraph(GO_CC)#GO-CC功能网络图
GO_MF<-enrichGO( genes$ENTREZID,#GO富集分析MF模块
                 OrgDb = org.Hs.eg.db,
                 keyType = "ENTREZID",
                 ont = "MF",
                 pvalueCutoff = 0.05,
                 pAdjustMethod = "BH",
                 qvalueCutoff = 0.05,
                 minGSSize = 10,
                 maxGSSize = 500,
                 readable = T)
plotGOgraph(GO_MF)#GO-MF功能网络图

# save emapplot
png("emapplot.png", width = 2160, height = 1480, res = 120)
emapplot(ego2, node_label_cex = 1.2, showCategory = 15, node_label_repel = TRUE, layout = "nicely")
dev.off()

# save dotplot
png("dotplot.png")
dotplot(ego, showCategory=10)
dev.off()

# save barplot
png("barplot.png")
barplot(ego, showCategory=10)
dev.off()

# save GO-BP plot
png("GO_BP_plot.png", width = 1580, height = 1480, res = 640)
plotGOgraph(GO_BP)
dev.off()

# save GO-CC plot
png("GO_CC_plot.png", width = 1580, height = 1480, res = 640)
plotGOgraph(GO_CC)
dev.off()

# save GO-MF plot
png("GO_MF_plot.png", width = 1580, height = 1480, res = 640)
plotGOgraph(GO_MF)
dev.off()

