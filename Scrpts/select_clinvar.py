import csv

gene_list_file = "gene_list.txt"
clinvar_file = "clinvar_result.txt"
output_file = "clinvar_gene_select.csv"

with open(gene_list_file, 'r') as f:
    genes = [line.strip() for line in f.readlines()]

with open(clinvar_file, 'r') as f, open(output_file, 'w', newline='') as out_f:
    reader = csv.reader(f, delimiter="\t")
    writer = csv.writer(out_f, delimiter=",")
    
    headers = next(reader) 
    headers.append("Matched_Gene")
    writer.writerow(headers)
    
    for row in reader:
        # Skip rows with 'Benign' in "Clinical significance (Last reviewed)" column
        if "Benign" in row[4] and not row[4].startswith("Likely benign"):
            continue
        
        for gene in genes:
            if gene in row[1]:
                print(f"Matched gene {gene} in clinvar_result.txt") 
                row.append(gene)
                writer.writerow(row)
                break

print("Filtered genes written to clinvar_gene_select.csv.")
