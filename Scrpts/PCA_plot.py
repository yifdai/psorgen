import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('filtered_VICTOR.sample_spc_missense.csv')

# Combine the 'Sex' and 'Aff' columns into a new 'Category' column
df['Category'] = df['Sex'] + '-' + df['Aff']

# Create a palette dictionary to specify colors for each category
palette = {
    "Female-Affected": "red",
    "Male-Affected": "blue",
    "Female-Unaffected": "green",
    "Male-Unaffected": "purple",
    "Female-UnknAff": "yellow",  
    "Male-UnknAff": "cyan"  
}

# Create the scatter plot
plt.figure(figsize=(10, 8))
sns.scatterplot(x='victorPC1', y='victorPC2', hue='Category', palette=palette, data=df)

# Set title and labels
plt.title('PCA clustering based on Sex and Affection status')
plt.xlabel('PC1')
plt.ylabel('PC2')

plt.savefig("PCA_plot.png", dpi=300)

# Show the plot
plt.show()

