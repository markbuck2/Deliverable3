import os

# Placeholder paths for CSV and images
file_path = 'SEC_Jamboree_1_Womens_5000_Meters_Junior_Varsity_24.csv'
image_dir = 'images'

# Placeholder team and individual data (Example data for illustration)
team_scores = [
    ["1", "Ypsilanti Lincoln", "22"],
    ["2", "Saline", "73"],
    ["3", "Dexter", "81"],
    ["4", "Ann Arbor Pioneer", "84"],
    ["5", "Ann Arbor Skyline", "134"]
]

individual_results = [
    ["1", "11", "Riley Provost", "https://www.athletic.net/athlete/14164024/cross-country", "23:15.00", "Saline", "https://www.athletic.net/athlete/14164024/cross-country", "14164024.jpg"],
    ["2", "9", "Claire Steinbrecher", "https://www.athletic.net/athlete/21411167/cross-country", "23:18.50", "Dexter", "https://www.athletic.net/athlete/21411167/cross-country", "21411167.jpg"],
    ["3", "11", "Mahalia Staton", "https://www.athletic.net/athlete/22262892/cross-country", "23:20.50", "Saline", "https://www.athletic.net/athlete/22262892/cross-country", "22262892.jpg"],
    ["4", "10", "Julianna Richards", "https://www.athletic.net/athlete/19005084/cross-country", "23:32.50", "Dexter", "https://www.athletic.net/athlete/19005084/cross-country", "19005084.jpg"],
    ["5", "12", "Elizabeth Thibeault", "https://www.athletic.net/athlete/18817762/cross-country", "23:34.00", "Saline", "https://www.athletic.net/athlete/18817762/cross-country", "18817762.jpg"]
]

# Function to generate HTML content for each page with a navigation bar
def generate_html_content(title, file_name, team_data, individual_data):
    # Navigation bar HTML with link back to results.html
    nav_bar = """
    <nav>
        <a href="results.html">Main Results</a> |
        <a href="results_overall.html">Overall Results</a> |
        <a href="top_teams.html">Top Teams</a> |
        <a href="top_individuals.html">Top Individuals</a> |
        <a href="team_highlights.html">Team Highlights</a> |
        <a href="index.html">Welcome Page</a>
    </nav>
    """

    # Main HTML structure with navigation included
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <link rel="stylesheet" href="css/style.css">
   <title>{title}</title>
</head>
<body>
   <header id="main-header">
       <h1>{title}</h1>
   </header>

   {nav_bar}

   <main id="content">
       <section id="event-title">
           <h2>SEC Jamboree #1 5000 Meters Junior Varsity</h2>
       </section>

       <section id="team-scores">
           <h2>Team Scores</h2>
           <table>
               <thead>
                   <tr>
                       <th>Place</th>
                       <th>Team</th>
                       <th>Score</th>
                   </tr>
               </thead>
               <tbody>
    """
    for index, score in enumerate(team_data):
        css_class = ['first-place', 'second-place', 'third-place'][index] if index < 3 else ''
        if len(score) >= 3:
            html_content += f"""
                    <tr class="{css_class}">
                        <td>{score[0]}</td>
                        <td>{score[1]}</td>
                        <td>{score[2]}</td>
                    </tr>
            """

    html_content += """
               </tbody>
           </table>
       </section>

       <section id="individual-results">
           <h2>Top Results</h2>
    """

    for index, result in enumerate(individual_data):
        if len(result) >= 7:
            athlete_link = result[3]
            athlete_id = result[7]
            image_path = os.path.join(image_dir, athlete_id) if os.path.exists(f"{image_dir}/{athlete_id}") else "images/default.jpg"
        
            html_content += f"""
            <div class="athlete">
                <h3>{result[2]}</h3>
                <p>Place: {result[0]}</p>
                <p>Grade: {result[1]}</p>
                <p>Time: {result[4]}</p>
                <p>Team: {result[5]}</p>
                <img src="{image_path}" alt="Profile Picture of {result[2]}" width="150">
            </div>
            <hr>
            """

    html_content += """
       </section>
   </main>
   <footer id="main-footer">
       <p>&copy; 2024 Client Project - All rights reserved.</p>
   </footer>
   <button id="dark-mode-toggle" class="mode-toggle">Toggle Dark Mode</button>

   <script src="js/script.js"></script>
</body>
</html>
    """
    # Write the HTML content to the specified file
    with open(file_name, 'w') as file:
        file.write(html_content)
    print(f"{file_name} has been created successfully.")

# Generate four results HTML pages with varied content 
titles = ["Overall Results", "Top Teams", "Top Individuals", "Team Highlights"]
file_names = ["results_overall.html", "top_teams.html", "top_individuals.html", "team_highlights.html"]

for i in range(4):
    team_data = team_scores[:i + 1] if i < 3 else team_scores  # Different team data for each file
    individual_data = individual_results[:i + 1] if i < 3 else individual_results  # Different individual data for each file
    generate_html_content(titles[i], file_names[i], team_data, individual_data)

# Generate the additional results.html page with navigation links
generate_html_content("Results Page", "results.html", team_scores[:3], individual_results[:3])
