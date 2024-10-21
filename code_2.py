import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

def load_data():
    # Load the dataset
    apps_df = pd.read_csv('C:\\Users\\msadi\\Desktop\\Null class\\Play Store Data.csv')
    
    # Clean and convert 'Installs' column
    apps_df['Installs'] = apps_df['Installs'].replace('Free', '0')  # Replace 'Free' with '0'
    apps_df['Installs'] = apps_df['Installs'].str.replace('+', '').str.replace(',', '')
    apps_df['Installs'] = pd.to_numeric(apps_df['Installs'], errors='coerce')  # Convert to numeric, invalid values become NaN
    apps_df['Installs'] = apps_df['Installs'].fillna(0).astype(int)  # Replace NaN with 0 and convert to int
    
    # Add a dummy 'Country' column for testing purposes
    apps_df['Country'] = 'United States'  # You can change this to appropriate values if needed

    return apps_df

def create_choropleth_map(apps_df):
    # Get current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    
    # Check if current time is between 12 PM and 6 PM
    if 12 <= current_time.hour < 18:
        print("This graph is not available between 12 PM and 6 PM IST.")
        return
    
    # Filter categories not starting with A, C, G, S
    filtered_df = apps_df[~apps_df['Category'].str.startswith(('A', 'C', 'G', 'S'))]
    
    # Get top 5 categories
    top_categories = filtered_df['Category'].value_counts().nlargest(5).index
    
    # Filter for top 5 categories and installs > 1 million
    map_data = filtered_df[
        (filtered_df['Category'].isin(top_categories)) & 
        (filtered_df['Installs'] > 1000000)
    ].copy()  # Make a copy to avoid SettingWithCopyWarning
    
    # Check if there's data to plot
    if map_data.empty:
        print("No data available for the selected filters.")
        return
    
    # Create choropleth map
    fig = px.choropleth(
        map_data,
        locations='Country',  # Use the 'Country' column
        locationmode='country names',
        color='Installs',
        hover_name='Country',  # Hover over the 'Country' column
        color_continuous_scale='Viridis',
        title='Global App Installs by Country (Top 5 Categories, >1M Installs)',
        labels={'Installs': 'Number of Installs'},
        scope='world',
        template='plotly'
    )

    # Update layout
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="LightGrey"
    )

    # Show the figure
    fig.show()

# Load the data
apps_df = load_data()

# Create and display the map
create_choropleth_map(apps_df)
