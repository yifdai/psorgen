filename = "VICTOR.sample_spc"

affected_count = 0
unaffected_count = 0

with open(filename, 'r') as f:
    headers = f.readline().strip().split("\t")  # Read headers
    aff_index = headers.index('Aff')  # Find the index of the 'Aff' column
    
    for line in f:
        data = line.strip().split("\t")
        if data[aff_index] == "Affected":
            affected_count += 1
        elif data[aff_index] == "Unaffected":
            unaffected_count += 1

print(f"Affected: {affected_count}")
print(f"Unaffected: {unaffected_count}")
print(f"Case / Control Ratio: {affected_count / unaffected_count}")
