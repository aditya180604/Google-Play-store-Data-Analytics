import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    # Load the datasets
    apps_df = pd.read_csv('C:\\Users\\msadi\\Desktop\\Null class\\Play Store Data.csv')
    reviews_df = pd.read_csv('C:\\Users\\msadi\\Desktop\\Null class\\User Reviews.csv')
    
    # Basic data cleaning
    apps_df = apps_df.dropna(subset=['Rating'])
    
    # Clean and convert 'Reviews' column
    apps_df['Reviews'] = apps_df['Reviews'].replace(r'[^\d.]', '', regex=True)  # Remove non-numeric characters
    apps_df['Reviews'] = apps_df['Reviews'].replace('', '0')  # Replace empty strings with '0'
    apps_df['Reviews'] = apps_df['Reviews'].astype(float)  # Convert to float first
    apps_df['Reviews'] = apps_df['Reviews'].astype(int)  # Then convert to int
    
    reviews_df = reviews_df.dropna(subset=['Translated_Review'])
    
    return apps_df, reviews_df

def sentiment_distribution(apps_df, reviews_df):
    # Merge apps and reviews data
    merged_df = pd.merge(apps_df, reviews_df, on='App')
    
    # Filter apps with more than 1000 reviews
    popular_apps = merged_df[merged_df['Reviews'] > 1000]
    
    # Create rating groups
    popular_apps['Rating_Group'] = pd.cut(popular_apps['Rating'], bins=[0, 2, 4, 5], labels=['1-2 stars', '3-4 stars', '4-5 stars'])
    
    # Get top 5 categories
    top_categories = popular_apps['Category'].value_counts().nlargest(5).index
    
    # Filter for top 5 categories
    popular_apps = popular_apps[popular_apps['Category'].isin(top_categories)]
    
    # Calculate sentiment distribution
    sentiment_dist = popular_apps.groupby(['Category', 'Rating_Group', 'Sentiment']).size().unstack(fill_value=0)
    
    # Normalize to get percentages
    sentiment_dist_pct = sentiment_dist.div(sentiment_dist.sum(axis=1), axis=0)
    
    # Create the stacked bar chart using Matplotlib
    ax = sentiment_dist_pct.plot(kind='bar', stacked=True, figsize=(10, 6), color=['green', 'gray', 'red'])
    
    # Set the title and labels
    plt.title('Sentiment Distribution by Rating Groups and Categories')
    plt.xlabel('App Categories')
    plt.ylabel('Percentage')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
    plt.legend(title='Sentiment')
    
    # Show the plot
    plt.tight_layout()  # Adjust layout for better fit
    plt.show()

# Load the data
apps_df, reviews_df = load_data()

# Call the function
sentiment_distribution(apps_df, reviews_df)
