import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
data = pd.read_csv('./results.csv')

# Convert relevant columns to numeric, forcing errors to NaN
time_columns = [f"{method} - Time" for method in ['BFS(top-down)', 'BFS(down-top)', 'DD', 'HDD(down-top)', 'HDD(top-down)']]
function_columns = [f"{method} - Functions" for method in ['BFS(top-down)', 'BFS(down-top)', 'DD', 'HDD(down-top)', 'HDD(top-down)']]

data[time_columns] = data[time_columns].apply(pd.to_numeric, errors='coerce')
data[function_columns] = data[function_columns].apply(pd.to_numeric, errors='coerce')

# Determine the combined value of PERSES+CGMethod and the method with the least functions and least time if tie
combined_values = []
for index, row in data.iterrows():
    min_functions = row[function_columns].min()
    min_functions_methods = [method for method in function_columns if row[method] == min_functions]
    
    if len(min_functions_methods) > 1:
        min_time_method = min_functions_methods[0]
        for method in min_functions_methods:
            if row[method.replace('Functions', 'Time')] < row[min_time_method.replace('Functions', 'Time')]:
                min_time_method = method
    else:
        min_time_method = min_functions_methods[0]

    min_time_method = min_time_method.replace(' - Functions', '')
    min_time = row[f"{min_time_method} - Time"]
    
    combined_time = row['PERSES+CGMethod - Time'] + min_time
    
    combined_values.append(combined_time)

data['Combined Time'] = combined_values

# Calculate the additional combined time
data['Combined Time Extended'] = (
    data['PERSES + function + Contract Level - Time'] +
    data['DD Contract Level - time'] +
    data[time_columns].min(axis=1)
)

# Calculate the speedup: PERSES Time / (PERSES+CGMethod + Min Algorithm Time)
data['Speedup'] = data['PERSES - Time'] / data['Combined Time']

# Calculate the speedup for Combined Time Extended: PERSES Time / Combined Time Extended
data['Speedup Extended'] = data['PERSES - Time'] / data['Combined Time Extended']

# Calculate and print the average speedups
average_speedup = data['Speedup'].mean()
average_speedup_extended = data['Speedup Extended'].mean()

print(f"Average Speedup (PERSES Time / DD function level): {average_speedup}")
print(f"Average Speedup (PERSES Time / DD function level + DD contract level): {average_speedup_extended}")


# Plotting the comparison for time
plt.figure(figsize=(14, 8))
contracts = data['Contract']

plt.plot(contracts, data['PERSES - Time'], marker='o', label='PERSES Time')
plt.plot(contracts, data['Combined Time'], marker='o', label='PERSES+ DD Function Level')
plt.plot(contracts, data['Combined Time Extended'], marker='o', label='PERSES + DD Function Level + DD Contract Level')

plt.xlabel('Smart Contracts')
plt.ylabel('Time (s)')
plt.title('Comparison of Combined Algorithm Times with PERSES Time')
plt.legend(title='Time Categories')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Save the plot as an image file
plt.savefig('./comparison_plot_time_combined.png')

# Show the plot
plt.show()

# Plotting the speedup
plt.figure(figsize=(14, 8))

plt.plot(contracts, data['Speedup'], marker='o', label='Speedup (PERSES + DD Function Level)')
plt.plot(contracts, data['Speedup Extended'], marker='o', label='Speedup (PERSES + DD Function Level + DD Contract Level)')

plt.xlabel('Smart Contracts')
plt.ylabel('Speedup')
plt.title('Speedup of Combined Algorithm Time over PERSES Time')
plt.legend(title='Speedup Categories')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Save the plot as an image file
plt.savefig('./comparison_plot_speedup_combined.png')

# Show the plot
plt.show()

