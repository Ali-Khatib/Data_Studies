import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Load the dataset
# -------------------------
csv_file = r"C:\Users\user\PycharmProjects\TMDB_Project\tmdbfile\movies.csv"
df = pd.read_csv(csv_file)

# Preview dataset
print("First 5 rows of the dataset:")
print(df.head())
print("\nColumns in the dataset:")
print(df.columns)

# -------------------------
# Research Question 1:
# Most popular movies by popularity
# -------------------------
top_popular = df.sort_values('popularity', ascending=False).head(10)

plt.figure(figsize=(12,6))
titles = [t if len(t) <= 20 else t[:17] + '...' for t in top_popular['title']]  # truncate long titles
plt.barh(titles, top_popular['popularity'], color='skyblue')
plt.xlabel('Popularity')
plt.title('Top 10 Most Popular Movies')
plt.gca().invert_yaxis()  # highest on top
plt.show()

# -------------------------
# Research Question 2:
# Highest rated movies by vote_average
# -------------------------
top_rated = df.sort_values('vote_average', ascending=False).head(10)

plt.figure(figsize=(12,6))
titles = [t if len(t) <= 20 else t[:17] + '...' for t in top_rated['title']]
plt.barh(titles, top_rated['vote_average'], color='salmon')
plt.xlabel('Vote Average')
plt.title('Top 10 Highest Rated Movies')
plt.gca().invert_yaxis()
plt.show()

# -------------------------
# Research Question 3:
# Popularity vs Vote Count
# -------------------------
plt.figure(figsize=(10,6))
plt.scatter(df['vote_count'], df['popularity'], alpha=0.6, color='green')
plt.xlabel('Vote Count')
plt.ylabel('Popularity')
plt.title('Popularity vs Vote Count')
plt.xscale('log')  # use log scale to handle big differences
plt.show()

# -------------------------
# Research Question 4:
# Vote Average vs Vote Count
# -------------------------
plt.figure(figsize=(10,6))
plt.scatter(df['vote_count'], df['vote_average'], alpha=0.6, color='purple')
plt.xlabel('Vote Count')
plt.ylabel('Vote Average')
plt.title('Vote Average vs Vote Count')
plt.xscale('log')
plt.show()

# -------------------------
# Conclusions
# -------------------------
print("""
Conclusions:
1. The most popular movies by 'popularity' metric are visually distinct from highest rated movies by 'vote_average'.
2. Some movies have very high vote counts which strongly correlates with popularity.
3. Vote averages do not always correspond to high popularity; some less popular movies are highly rated.
4. Data visualization improves readability by truncating long movie titles and using log scales for vote count comparisons.
""")
