import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

def load_data():
    # Load the dataset
    apps_df = pd.read_csv('C:\\Users\\msadi\\Desktop\\Null class\\Play Store Data.csv')

    # Clean and convert 'Size' column
    apps_df['Size'] = apps_df['Size'].str.replace('M', '').str.replace('k', '').replace('', '0')  # Handle 'k' and empty values
    apps_df['Size'] = apps_df['Size'].replace('Varies with device', '0')  # Replace non-numeric entries with '0'
    apps_df['Size'] = pd.to_numeric(apps_df['Size'], errors='coerce')  # Convert to numeric, invalid values become NaN
    apps_df['Size'] = apps_df['Size'].fillna(0)  # Fill NaN values with 0

    # Clean and convert 'Installs' column
    apps_df['Installs'] = apps_df['Installs'].replace('Free', '0')  # Replace 'Free' with '0'
    apps_df['Installs'] = apps_df['Installs'].str.replace('+', '').str.replace(',', '')
    apps_df['Installs'] = pd.to_numeric(apps_df['Installs'], errors='coerce')  # Convert to numeric
    apps_df['Installs'] = apps_df['Installs'].fillna(0).astype(int)  # Replace NaN with 0 and convert to int

    # Clean and convert 'Rating' column
    apps_df['Rating'] = pd.to_numeric(apps_df['Rating'], errors='coerce').fillna(0)

    return apps_df

def create_bubble_chart(apps_df):
    # Check the current time
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    if not (12 <= current_time.hour < 16):
        print("This graph is only available between 12 PM and 4 PM IST.")
        return

    # Print basic statistics for debugging
    print("Data Overview:")
    print(apps_df[['Category', 'Rating', 'Installs']].describe(include='all'))

    # Check and print all unique categories
    unique_categories = apps_df['Category'].unique()
    print("Unique Categories:", unique_categories)

    # Filter for the correct "Game" category (not "Games")
    games_apps = apps_df[apps_df['Category'] == 'GAME']
    print(f"Total 'GAME' category apps: {len(games_apps)}")

    # Filter for apps with Rating > 3.5
    high_rating_apps = games_apps[games_apps['Rating'] > 3.5]
    print(f"Apps with rating > 3.5: {len(high_rating_apps)}")

    # Filter for apps with Installs > 50,000
    final_filtered_apps = high_rating_apps[high_rating_apps['Installs'] > 50000]
    print(f"Final filtered apps count: {len(final_filtered_apps)}")

    # Check if there are no filtered apps
    if final_filtered_apps.empty:
        print("No data available for the selected filters.")
        return
    
    # Plot the bubble chart
    fig = px.scatter(
        final_filtered_apps,
        x='Size', 
        y='Rating', 
        size='Installs',
        hover_name='App',
        title='Bubble Chart of Apps: Size vs Rating',
        labels={'Size': 'Size (MB)', 'Rating': 'Average Rating'},
        size_max=60
    )
    fig.show()

# Assuming you have the load_data function and the rest of your code correctly set up
apps_df = load_data()
create_bubble_chart(apps_df)
