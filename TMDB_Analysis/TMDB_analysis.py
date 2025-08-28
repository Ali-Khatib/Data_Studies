import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

# -------------------------
# Load and clean dataset
# -------------------------
df = pd.read_csv(r"C:\Users\user\PycharmProjects\TMDB_Project\tmdbfile\movies.csv")
df = df.dropna(subset=["title", "vote_average", "release_date"])

# Convert release_date to year
df["release_year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year

# -------------------------
# Helper: Convert plots to HTML <img>
# -------------------------
def plot_to_html(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return f'<img src="data:image/png;base64,{img_base64}" style="max-width:100%;">'

# Store report parts
html_parts = ["<h1>TMDb Dataset Report</h1>"]

# ==========================
# 1. Distribution of Ratings
# ==========================
fig, ax = plt.subplots(figsize=(8,5))
sns.histplot(df["vote_average"], bins=20, kde=True, color="skyblue", ax=ax)
ax.set_title("Distribution of Movie Ratings")
ax.set_xlabel("Average Rating")
ax.set_ylabel("Number of Movies")
html_parts.append("<h2>Distribution of Ratings</h2>")
html_parts.append(plot_to_html(fig))
plt.close(fig)

# ==========================
# 2. Movies per Year
# ==========================
movies_per_year = df["release_year"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(12,6))
movies_per_year.plot(kind="line", marker="o", color="tomato", ax=ax)
ax.set_title("Movies Released per Year")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Movies")
html_parts.append("<h2>Movies per Year</h2>")
html_parts.append(plot_to_html(fig))
plt.close(fig)

# ==========================
# 3. Most Popular Movies
# ==========================
top_popular = df.sort_values("popularity", ascending=False).head(10)
fig, ax = plt.subplots(figsize=(12,6))
titles = [t if len(t) <= 20 else t[:17] + "..." for t in top_popular["title"]]
ax.barh(titles, top_popular["popularity"], color="skyblue")
ax.set_xlabel("Popularity")
ax.set_title("Top 10 Most Popular Movies")
ax.invert_yaxis()
html_parts.append("<h2>Top 10 Most Popular Movies</h2>")
html_parts.append(plot_to_html(fig))
plt.close(fig)

# ==========================
# 4. Highest Rated Movies
# ==========================
top_rated = df.sort_values("vote_average", ascending=False).head(10)
fig, ax = plt.subplots(figsize=(12,6))
titles = [t if len(t) <= 20 else t[:17] + "..." for t in top_rated["title"]]
ax.barh(titles, top_rated["vote_average"], color="salmon")
ax.set_xlabel("Vote Average")
ax.set_title("Top 10 Highest Rated Movies")
ax.invert_yaxis()
html_parts.append("<h2>Top 10 Highest Rated Movies</h2>")
html_parts.append(plot_to_html(fig))
plt.close(fig)

# ==========================
# 5. Popularity vs Vote Count
# ==========================
fig, ax = plt.subplots(figsize=(10,6))
ax.scatter(df["vote_count"], df["popularity"], alpha=0.6, color="green")
ax.set_xlabel("Vote Count (log scale)")
ax.set_ylabel("Popularity")
ax.set_title("Popularity vs Vote Count")
ax.set_xscale("log")
html_parts.append("<h2>Popularity vs Vote Count</h2>")
html_parts.append(plot_to_html(fig))
plt.close(fig)

# ==========================
# 6. Vote Average vs Vote Count
# ==========================
fig, ax = plt.subplots(figsize=(10,6))
ax.scatter(df["vote_count"], df["vote_average"], alpha=0.6, color="purple")
ax.set_xlabel("Vote Count (log scale)")
ax.set_ylabel("Vote Average")
ax.set_title("Vote Average vs Vote Count")
ax.set_xscale("log")
html_parts.append("<h2>Vote Average vs Vote Count</h2>")
html_parts.append(plot_to_html(fig))
plt.close(fig)

# ==========================
# Summary / Conclusions
# ==========================
summary = f"""
<ul>
<li>Movie ratings are mostly between 5 and 7.</li>
<li>Dataset covers years {int(movies_per_year.index.min())} to {int(movies_per_year.index.max())}.</li>
<li>Movie releases peaked in recent years.</li>
<li>Most popular movies differ from highest rated ones — popularity ≠ rating.</li>
<li>Movies with high vote counts are usually more popular (strong correlation).</li>
<li>Some lesser-known movies score high in ratings but lack popularity.</li>
</ul>
"""
html_parts.append("<h2>Summary</h2>")
html_parts.append(summary)

# ==========================
# Save as HTML
# ==========================
html_report = "\n".join(html_parts)
with open("tmdb_report.html", "w", encoding="utf-8") as f:
    f.write(html_report)

print("✅ Full report generated: tmdb_report.html (open in browser)")
