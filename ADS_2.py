import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def process_world_bank_data(population_data):
    
    """
    Process World Bank population data from a CSV file.

    Parameters:
        
    Path to the CSV file containing World Bank population data.

    Returns:
   
    Transposed and cleaned DataFrame for further analysis.
    
    """
    world_bank_data = pd.read_csv(population_data).iloc[: -5]
    world_bank_data.drop(columns=['Country Code', 'Series Code', '2001 [YR2001]', '2002 [YR2002]', '2003 [YR2003]', '2004 [YR2004]', '2005 [YR2005]', '2006 [YR2006]', '2007 [YR2007]','2008 [YR2008]','2009 [YR2009]','2010 [YR2010]','2011 [YR2011]','2012 [YR2012]'], inplace=True) 
    world_bank_data.columns = [col.split(' ')[0] for col in world_bank_data.columns]
    transpose = world_bank_data.T
    transpose.columns = transpose.iloc[0]
    transpose = transpose.iloc[1:]
    transpose = transpose[transpose.index.str.isnumeric()]
    transpose.index = pd.to_numeric(transpose.index)
    transpose['Years'] = transpose.index
    
    return world_bank_data, transpose

# Read the World Bank data from the specified CSV file path.
population_data_path = r"/Users/user1/Downloads/P_Data_Extract_From_World_Development_Indicators-3 2/fa0aaa74-f486-420b-a339-7cf1e29bfbe4_Data.csv"
world_bank_data, transpose = process_world_bank_data(population_data_path)

print(world_bank_data.head())
print(transpose.head())

# Summary Statistics
indicators = ['Population density (people per sq. km of land area)', 'Rural population', 'Urban population (% of total population)', 'Urban population growth (annual %)','Population in the largest city (% of urban population)']
selected_data = world_bank_data[world_bank_data['Series'].isin(indicators)]
summary_statistics = selected_data.groupby('Series').describe()

# Correlation Analysis
selected_years = ['2013']
indicator_corr = selected_data.pivot_table(index='Country', columns='Series', values=selected_years)
correlation_matrix = indicator_corr.corr()

# Plotting the Correlation Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap between Indicators for 2013')
plt.xlabel('Series')
plt.ylabel('Series')
plt.show()

def barplot_urban_growth_data(world_bank_data):
    
    """
    Create a bar plot for urban population growth data for the years 2015-2019.

    Parameters:
        
    Transposed and cleaned World Bank data.

    """
    urban_growth_data = world_bank_data[world_bank_data['Series'] == 'Urban population growth (annual %)']

    # Bar Plot for Urban Population Growth
    plt.figure(figsize=(12, 8))
    urban_growth_data_melted = pd.melt(urban_growth_data, id_vars=['Country'], value_vars=['2015', '2016', '2017', '2018', '2019'],
                                       var_name='Year', value_name='Urban Population Growth (Annual %)')

    urban_growth_data_melted['Urban Population Growth (Annual %)'] = urban_growth_data_melted['Urban Population Growth (Annual %)'].astype(float)
    urban_growth_data_melted['Year'] = urban_growth_data_melted['Year'].astype(int)

    sns.barplot(x='Country', y='Urban Population Growth (Annual %)', hue='Year', data=urban_growth_data_melted,
                palette='magma', dodge=True)

    plt.title('Urban Population Growth (Annual %) in 2015 - 2019')
    plt.xlabel('Country')
    plt.ylabel('Urban Population Growth (Annual %)')
    plt.xticks(rotation=90)
    plt.legend(title='Year', loc=2)
    plt.show()

barplot_urban_growth_data(world_bank_data)

def lineplot_urban_growth_data(world_bank_data):
    
    """
    Create a line plot for urban population growth data over the years 2015-2019.

    Parameters:
    
    Transposed and cleaned World Bank data.

    """
    urban_growth_data = world_bank_data[world_bank_data['Series'] == 'Urban population growth (annual %)']

    # Line Plot for Urban Population Growth
    plt.figure(figsize=(12, 8))
    urban_growth_data_melted = pd.melt(urban_growth_data, id_vars=['Country'], value_vars=['2015', '2016', '2017', '2018', '2019'],
                                       var_name='Year', value_name='Urban Population Growth (Annual %)')

    urban_growth_data_melted['Urban Population Growth (Annual %)'] = urban_growth_data_melted['Urban Population Growth (Annual %)'].astype(float)
    urban_growth_data_melted['Year'] = urban_growth_data_melted['Year'].astype(int)

    sns.lineplot(x='Year', y='Urban Population Growth (Annual %)', hue='Country', data=urban_growth_data_melted, marker='o', markersize=8, linewidth=2)

    plt.title('Urban Population Growth (Annual %) Over the Years')
    plt.xlabel('Year')
    plt.xticks(range(2015, 2020, 1))
    plt.ylabel('Urban Population Growth (Annual %)')
    plt.legend(title='Country',  loc=3)
    plt.show()

lineplot_urban_growth_data(world_bank_data)

def pie_chart_largest_city_population(world_bank_data):
    
    """
    Create a pie chart for the population in the largest city (% of urban population) for the year 2019.

    Parameters:
    
    Transposed and cleaned World Bank data.

    """
    largest_city_data = world_bank_data[world_bank_data['Series'] == 'Population in the largest city (% of urban population)']

    year = '2019'
    
    largest_city_data = largest_city_data.dropna(subset=[year])
    largest_city_data[year] = largest_city_data[year].astype(float)
    largest_city_data = largest_city_data.sort_values(by=year, ascending=False)

    top_countries = largest_city_data.head(6)

    # Plot the pie chart
    plt.figure(figsize=(10, 8))
    explode=[0.03,0.03,0.03,0.03,0.03,0.03]
    plt.pie(top_countries[year], labels=top_countries['Country'], explode=explode, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set3"))
    plt.title(f'Population in the Largest City (% of Urban Population) ({year})')
    plt.show()

pie_chart_largest_city_population(world_bank_data)

def histogram_rural_population(world_bank_data):
    
    """
    Create a histogram for rural population for the years 2015-2019.

    Parameters:
    
    Transposed and cleaned World Bank data.

    """
    # Filter data for rural population
    rural_population_data = world_bank_data[world_bank_data['Series'] == 'Rural population']
    rural_population_data_melted = pd.melt(rural_population_data, id_vars=['Country'], value_vars=['2015', '2016', '2017', '2018', '2019'],
                                       var_name='Year', value_name='Rural Population')
    
    rural_population_data_melted['Rural Population'] = rural_population_data_melted['Rural Population'].astype(float)
    rural_population_data_melted['Year'] = rural_population_data_melted['Year'].astype(int)

    # Histogram for Rural Population
    plt.figure(figsize=(12, 8))
    sns.histplot(data=rural_population_data_melted, x='Rural Population', bins=20, color='skyblue')
    plt.title('Histogram for Rural Population (2015-2019)')
    plt.xlabel('Rural Population')
    plt.ylabel('Frequency')
    plt.show()

# Call the function to generate the histogram for rural population
histogram_rural_population(world_bank_data) 

