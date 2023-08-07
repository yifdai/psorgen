import pandas as pd

def sum_colon_data(series):
    data_dict = {}
    for data in series:
        # Splitting by space gives all key:value pairs
        data_items = data.split()
        for item in data_items:
            # Check if the current item contains multiple key:value pairs separated by '/'
            if '/' in item:
                subitems = item.split('/')
                for subitem in subitems:
                    key, value = subitem.split(":")
                    if key not in data_dict:
                        data_dict[key] = 0
                    data_dict[key] += int(value)
            else:
                key, value = item.split(":")
                if key not in data_dict:
                    data_dict[key] = 0
                data_dict[key] += int(value)
    return ' '.join([f"{k}:{v}" for k, v in data_dict.items()])

def extract_int_from_string(x, position):
    try:
        return int(x.split('/')[position].split(':')[-1])
    except ValueError:
        print(f"Error extracting integer from: {x}")
        return 0  # or some default value

def process_csv(input_csv):
    df = pd.read_csv(input_csv)

    # 对数据进行分组并汇总
    grouped = df.groupby('GeneEffects').agg({
        'VariantID': 'count',
        'Individuals': lambda x: ','.join(x),
        'SEX': sum_colon_data,
        'AFT': sum_colon_data,
        'VICPOP': sum_colon_data,
        'Disease ': 'first',  # 只取第一个Disease的值
        'OMIM': 'first'       # 只取第一个OMIM的值
    }).reset_index()

    # Replace the lambda with a call to this function
    grouped['case/control ratio'] = grouped['AFT'].apply(lambda x: extract_int_from_string(x, 0) / extract_int_from_string(x, 1))

    # 保存到新的csv文件
    grouped.to_csv(input_csv.replace('.csv', '_processed.csv'), index=False)
    print(f"Processed data saved to {input_csv.replace('.csv', '_processed.csv')}")

# 处理两个csv文件
process_csv('variants_individuals_disease_OMIM_case_control_frameshift_adjusted.csv')
process_csv('variants_individuals_disease_OMIM_case_control_missense_adjusted.csv')
