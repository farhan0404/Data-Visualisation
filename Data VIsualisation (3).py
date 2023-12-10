#!/usr/bin/env python
# coding: utf-8

# # DATA VISUALISATION

# Importing Relevant Libraries

# In[1]:


#pip install geopandas


# In[2]:


import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd


# In[3]:



Data = pd.read_csv(r"C:\Msc data Science\Data Visualisation\Datasets (Coursework)-20231209\1. WHO-COVID-19-global-table-data.csv")
Data_1 = pd.read_csv(r"C:\Msc data Science\Data Visualisation\Datasets (Coursework)-20231209\2. vaccination-data.csv")


# In[4]:


Data.tail()


# In[5]:


Data_1.head()


# In[6]:


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


# In[7]:


world = world.merge(Data_1, how='left', left_on='name', right_on='COUNTRY')


# In[8]:


st.title('World Vaccination Heat Map')


# In[9]:


selected_metric = st.sidebar.selectbox('Select metric', ['TOTAL_VACCINATIONS', 'PERSONS_VACCINATED_1PLUS_DOSE', 'TOTAL_VACCINATIONS_PER100', 'PERSONS_VACCINATED_1PLUS_DOSE_PER100', 'PERSONS_FULLY_VACCINATED', 'PERSONS_FULLY_VACCINATED_PER100'], index=0)


# In[10]:


fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.boundary.plot(ax=ax)
world.plot(column=selected_metric, cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
plt.title(f'World Vaccination Heat Map - {selected_metric}')
plt.axis('off')

# Display the map in Streamlit
st.pyplot(fig)


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


# In[12]:


print(Q2)


# In[13]:


st.title('Pie Chart')


# In[14]:


non_zero_sizes_list = []
non_zero_labels_list = []

# Loop through each attribute
selected_metric_pie = st.sidebar.selectbox(
    'Select metric',
    Q2.columns[1:],  # Exclude the 'WHO Region' column
)
plt.figure(figsize=(16, 16), dpi=600)
non_zero_sizes = [size for size in Q2[selected_metric_pie] if size > 0]
non_zero_labels = [region for region, size in zip(Q2['WHO Region'], Q2[selected_metric_pie]) if size > 0]

plt.pie(non_zero_sizes, labels=non_zero_labels, autopct='%.0f%%')
plt.title(f'World Indicators - {selected_metric_pie}')

# Display the pie chart using Streamlit
st.pyplot(plt.gcf())


# In[15]:


# Assuming 'Name' is the common column name in 'filtered_data' and 'COUNTRY' in 'filtered_data_1'
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

# Perform the division on the specific column
df_merged['Cases - newly reported in last 7 days per 100000 population'] /= 100

# Drop redundant columns
df_merged.drop(columns=['COUNTRY'], inplace=True)

# Print or visualize df_merged
print(df_merged)


# In[16]:


df_merged.head()


# In[17]:


# Assuming 'WHO Region' is the attribute in df_merged with multiple names in the same region
df_merged_sorted = df_merged.sort_values(by='WHO Region')

# Streamlit app
st.title('COVID-19 Data Visualization')

# Selectbox for choosing the country
selected_country = st.selectbox('Select Country', df_merged_sorted['WHO Region'].unique())

# Filter data for the selected country
selected_data = df_merged_sorted[df_merged_sorted['WHO Region'] == selected_country]

# Plotting the data
fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(selected_data['PERSONS_FULLY_VACCINATED_PER100'], selected_data['Cases - newly reported in last 7 days per 100000 population'], marker='o', linestyle='-', color='b')

# Adding labels and title
ax.set_xlabel('Number of People Vaccinated')
ax.set_ylabel('Number of Newly Reported Cases')
ax.set_title(f'Relationship between Vaccination and Newly Reported Cases - {selected_country}')

# Show the plot using Streamlit
st.pyplot(fig)


# In[ ]:




