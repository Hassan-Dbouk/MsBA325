import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Suicide Rates per 100K Population')

raw_data = pd.read_csv("https://raw.githubusercontent.com/Hassan-Dbouk/MsBA325/main/Merged_data.csv")

if st.checkbox('Show Raw Data'):
    st.subheader('Raw Data')
    st.write(raw_data)


#Creating Scatter Plot for Albania Suicide Rates:

df = pd.read_csv("https://raw.githubusercontent.com/Hassan-Dbouk/MsBA325/main/master.csv")


#grouping by year and age:
grouped_df = df.groupby(['year','age','country']).agg({'population':'sum',
                                                       'suicides_no' : 'sum'}).reset_index()
grouped_df['suicide/100k'] = ( grouped_df['suicides_no']/grouped_df['population'])*100000

# Adding Subheader:
st.subheader('Suicide Rates Over Years')

#Creating a selectbox:
option = st.selectbox('Choose a Country:', np.array(grouped_df['country']))

#Creating a SLider for Years:
selected_year = st.slider('Select Year', min_value=min(grouped_df['year']), max_value=max(grouped_df['year']), value=1987)

#Selecting the min and max values over y-axis:
y_min, y_max = grouped_df['suicide/100k'].min(), grouped_df['suicide/100k'].max()


#Plotting Scatter Plot Based on Selected Year Using Pyplot:

filtered_data = grouped_df[ (grouped_df['year'] == selected_year) & (grouped_df['country'] == option)]
# Check if there is any data for the selected year
import plotly.express as px

if not filtered_data.empty:
    # Create a scatter plot using Plotly Express
    fig = px.scatter(filtered_data, x='age', y='suicide/100k', title='Suicide Rate vs. Age Range')
    fig.update_xaxes(title_text="Age Range")
    fig.update_yaxes(title_text="Suicide Rate per 100K")

    # Set fixed axis limits (adjust y_min and y_max as needed)
    fig.update_yaxes(range=[y_min, y_max])

    # Display the plot
    st.plotly_chart(fig)
else:
    # Display a message if there is no data for the selected year
    st.write(f"No data available for the year {selected_year}")

##################################################################################################

#Creating a Map Plot for Suicide Rates Over the World:

df = pd.read_csv("https://raw.githubusercontent.com/Hassan-Dbouk/MsBA325/main/master.csv")
grouped_df = df.groupby(['country', 'year']).agg({'suicides_no':'sum',
                                                  'population':'sum',
                                                  }).reset_index()
grouped_df['suicides/100k'] = (grouped_df['suicides_no']/grouped_df['population'])*100000

#Reading another dataframe that has longitude and latitude for each country:
geom_df = pd.read_csv("https://raw.githubusercontent.com/Hassan-Dbouk/MsBA325/main/world_country_and_usa_states_latitude_and_longitude_values.csv")

# Merge the DataFrames based on the 'country' column, using a left join:
merged_df = pd.merge(grouped_df, geom_df[['country', 'latitude', 'longitude']],  # Select only 'country', 'lat', and 'lon' columns
    left_on='country',  # Column from suicide_rate_df
    right_on='country',  # Column from country_lat_lon_df
    how='left'  # Left join to keep all rows from suicide_rate_df
)

#Dropping NA longitude or latitude values
merged_df = merged_df.dropna(subset=['latitude', 'longitude'])

#Writing a subheader:
st.subheader('Suicide Rates Map Plot')

#SLider to slide over years:
selected_year = st.slider('select year', min_value= min(merged_df['year']), max_value=max(merged_df['year']))
selected_data = merged_df[ merged_df['year'] == selected_year ]
#Plotting Selected Data
fig = px.scatter_geo(
    selected_data,
    locations="country",
    locationmode="country names",
    lat="latitude",
    lon="longitude",
    hover_name="country",
    hover_data=["suicides/100k"],
    color="suicides/100k",
    color_continuous_scale="reds",  # Adjust color scale as needed
    size="suicides/100k",  # Marker size based on suicide rate
    projection="natural earth"  # Adjust projection as needed
)
fig.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="lightgray")


st.plotly_chart(fig)



###############################################################################################################
#Generating a Histogram:
st.subheader('Histogram of Suicide Rates per 100K')
selected_year = st.slider('Select Year', min_value= min(merged_df['year']), max_value= max(merged_df['year']))
fig = px.histogram(merged_df[ merged_df['year'] == selected_year ], x= 'suicides/100k', color='country')

st.plotly_chart(fig)

# output_path = 'D:/AUB/Visualization/lect 3/Merged_data.csv'
# merged_df.to_csv(output_path, index=False)
#streamlit run Streamlit_vis_2.py