import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

# Load dataset
df = pd.read_csv(r"/tmdbfile/movies.csv")

# Quick clean-up
df = df.dropna(subset=["title", "vote_average", "release_date"])

# Function to convert plots to base64 HTML <img>
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
df["release_year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
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
# Short Findings
# ==========================
summary = f"""
<ul>
<li>Movie ratings are mostly between 5 and 7.</li>
<li>Dataset covers years {int(movies_per_year.index.min())} to {int(movies_per_year.index.max())}.</li>
<li>Movie releases peaked in recent years.</li>
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

print("✅ Report generated: tmdb_report.html (open in browser)")
