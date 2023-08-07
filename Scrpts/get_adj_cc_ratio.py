import csv

adjustment_factor = 0.9452830188679245

def process_file(filename):
    output_filename = filename.replace(".csv", "_adjusted.csv")
    
    with open(filename, 'r') as infile, open(output_filename, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['case/control ratio adjusted']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            ratio = float(row['case/control ratio'])
            adjusted_ratio = ratio / adjustment_factor
            row['case/control ratio adjusted'] = adjusted_ratio
            writer.writerow(row)

    print(f"Processed {filename} -> {output_filename}")

# Process the two files
process_file("variants_individuals_disease_OMIM_case_control_frameshift.csv")
process_file("variants_individuals_disease_OMIM_case_control_missense.csv")
