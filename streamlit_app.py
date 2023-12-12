#!/usr/bin/env python
# coding: utf-8

# # DATA VISUALISATION

# In[1]:


#pip install geopandas


# Importing Relevant Libraries

# In[2]:


import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd


#  Loading Dataset

# In[3]:



Data = pd.read_csv(r"1. WHO-COVID-19-global-table-data.csv")
Data_1 = pd.read_csv(r"2. vaccination-data.csv")


# In[4]:


Data.tail()


# In[5]:


Data_1.head()


# Import World map dataset

# In[6]:


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


# Merge the World Data With Our vaccination Dataset

# In[7]:


world = world.merge(Data_1, how='left', left_on='name', right_on='COUNTRY')


# In[25]:


st.title('DATA VISUALISATION')

st.write('HEAT MAP TO DEPICIT VACCINATION')


# Creating a Dropdown

# In[9]:


selected_metric = st.sidebar.selectbox('World Vaccination Status', ['PERSONS_FULLY_VACCINATED_PER100','TOTAL_VACCINATIONS', 'PERSONS_VACCINATED_1PLUS_DOSE', 'TOTAL_VACCINATIONS_PER100', 'PERSONS_VACCINATED_1PLUS_DOSE_PER100', 'PERSONS_FULLY_VACCINATED'], index=0)


# # Plotting The HeatMap Question 1

# In[10]:


fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.boundary.plot(ax=ax)
world.plot(column=selected_metric, cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
plt.title(f'World Vaccination Heat Map - {selected_metric}',y=1.05)
plt.axis('off')

# Display the map in Streamlit
st.pyplot(fig)


# Creating a Dataframe by grouping the data to WHO Region

# In[11]:


columns_to_sum = [
    'Cases - cumulative total',
    'Cases - cumulative total per 100000 population',
    'Cases - newly reported in last 7 days',
    'Cases - newly reported in last 7 days per 100000 population',
    'Cases - newly reported in last 24 hours',
    'Deaths - cumulative total',
    'Deaths - cumulative total per 100000 population',
    'Deaths - newly reported in last 7 days',
    'Deaths - newly reported in last 7 days per 100000 population',
    'Deaths - newly reported in last 24 hours'
]

Q2 = Data.groupby('WHO Region')[columns_to_sum].sum().reset_index()


# In[26]:


Q2.head()


# # Plotting The Pie Chart Question 2

# In[13]:


st.title('Covid Cases based on WHO Region')


# In[57]:


non_zero_sizes_list = []
non_zero_labels_list = []

selected_metric_pie = st.sidebar.selectbox(
    'Select the Criteria for pie chart',
    Q2.columns[1:],  # Exclude the 'WHO Region' column
)
plt.figure(figsize=(16, 16), dpi=600)
non_zero_sizes = [size for size in Q2[selected_metric_pie] if size > 0]
non_zero_labels = [region for region, size in zip(Q2['WHO Region'], Q2[selected_metric_pie]) if size > 0]

plt.pie(non_zero_sizes, labels=non_zero_labels, autopct='%1.1f%%',startangle=90)
plt.rcParams['font.size'] = 30
plt.title(f'World Indicators - {selected_metric_pie}')

# Display the pie chart using Streamlit
st.pyplot(plt.gcf())


# In[28]:


#Identifying the commin countries
common_countries = set(Data['Name']).intersection(Data_1['COUNTRY'])

# Filter dataframes to keep only common countries
filtered_data = Data[Data['Name'].isin(common_countries)]
filtered_data_1 = Data_1[Data_1['COUNTRY'].isin(common_countries)]

# Merge on the common column
df_merged = pd.merge(
    filtered_data[['Name', 'Cases - newly reported in last 7 days per 100000 population', 'WHO Region']],
    filtered_data_1[['COUNTRY', 'PERSONS_FULLY_VACCINATED_PER100']],
    left_on='Name',
    right_on='COUNTRY'
)

# Perform the division on the specific column to make it to 100 population
df_merged['Cases - newly reported in last 7 days per 100000 population'] /= 1000

# Drop redundant columns
df_merged.drop(columns=['COUNTRY'], inplace=True)

# Print or visualize df_merged
df_merged.head()


# # Relationship between Vaccination and Newly Reported Cases Question 3

# In[61]:


# Assuming 'WHO Region' is the attribute in df_merged with multiple names in the same region
df_merged_sorted = df_merged.sort_values(by='WHO Region')

# Streamlit app
st.title('Relationship between Vaccination and Newly Reported Cases')

# Selectbox for choosing the country
selected_country = st.selectbox('WHO Region', df_merged_sorted['WHO Region'].unique())

# Filter data for the selected country
selected_data = df_merged_sorted[df_merged_sorted['WHO Region'] == selected_country]

# Plotting the data
fig, ax = plt.subplots(figsize=(20, 12))

ax.scatter(selected_data['PERSONS_FULLY_VACCINATED_PER100'], selected_data['Cases - newly reported in last 7 days per 100000 population'], marker='o', linestyle='-', color='b')

# Adding labels and title
ax.set_xlabel('Number of People Vaccinated')
ax.set_ylabel('Number of Newly Reported Cases')
title = f'Relationship between Vaccination and Newly Reported Cases - {selected_country}'
ax.set_title(title, y=1.05) 
# Show the plot using Streamlit
st.pyplot(fig)


# # Top 10 countries with most covid cases in each WHO Region Question 4

# In[63]:


st.title('Total Covid Cases Reported')

# Dropdown to select WHO Region
selected_region = st.selectbox('Select WHO Region', ['All'] + Data['WHO Region'].unique().tolist())

# Filter data based on selected WHO Region
if selected_region != 'All':
    filtered_df =Data[Data['WHO Region'] == selected_region]
else:
    filtered_df = Data
top_countries = filtered_df.nlargest(10, 'Cases - cumulative total')
# Plotting
fig3, ax = plt.subplots(figsize=(20, 12))
sns.barplot(data=top_countries, x='Name', y='Cases - cumulative total', hue='WHO Region', ax=ax, dodge=True)

ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_title('Top 10 Countries by Cases Reported')
ax.set_xlabel('Country')
ax.set_ylabel('Number of Cases Reported')

# Display figure in Streamlit
st.pyplot(fig3)


# # To Create a Recovery Chart of Top 10 countries Question 5

# In[64]:


st.title('Recovery Chart')

# Dropdown to select WHO Region
selectbox_key = 'select_region_' + str(hash(tuple(Data['WHO Region'].unique())))

# Dropdown to select WHO Region
selected_region = st.selectbox('Select WHO Region', ['All'] + Data['WHO Region'].unique().tolist(), key=selectbox_key)

# Filter data based on selected WHO Region
if selected_region != 'All':
    filtered_df = Data[Data['WHO Region'] == selected_region]
else:
    filtered_df = Data

# Create a new column for 'Recovery Percentage'
filtered_df['Recovery Percentage'] = (filtered_df['Cases - cumulative total'] - filtered_df['Deaths - cumulative total'])/filtered_df['Cases - cumulative total']

# Select top countries based on 'Recovery Percentage'
top_countries = filtered_df.nlargest(10, 'Recovery Percentage')

# Plotting
fig3, ax = plt.subplots(figsize=(20, 12))
sns.barplot(data=top_countries, x='Name', y='Recovery Percentage', hue='WHO Region', ax=ax, dodge=True)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_title('Top 10 Countries by Recovery Cases')
ax.set_xlabel('Country')
ax.set_ylabel('Number of Recovery Cases')

# Display figure in Streamlit
st.pyplot(fig3)

