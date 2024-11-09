import os

# Paths for CSV files and image directory
file_path_grade_9 = 'SEC_Jamboree_1_Womens_5000_Meters_Junior_Varsity_24.csv'
file_path_men = '37th_Early_Bird_Open_Mens_5000_Meters_HS_Open_5K_24.csv'
image_dir = 'images'

# Placeholder data for team scores and individual results
team_scores_grade_9 = []
individual_results_grade_9 = []
team_scores_men = []
individual_results_men = []

# Function to read CSV data and store in lists
def read_csv(file_path, team_scores, individual_results):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    in_team_scores = False
    in_individual_results = False

    for line in lines:
        line = line.strip()
        if line.startswith("Place,Team,Score"):
            in_team_scores = True
            in_individual_results = False
            continue
        elif line.startswith("Place,Grade,Name,Athlete Link,Time,Team,Team Link,Profile Pic"):
            in_team_scores = False
            in_individual_results = True
            continue
        elif not line:
            continue

        data = line.split(',')
        
        if in_team_scores and len(team_scores) < 3:
            if len(data) >= 3 and all(data[:3]):
                team_scores.append(data[:3])
        elif in_individual_results:
            if len(data) >= 8 and all(data[:8]):
                individual_results.append(data[:8])

# Read data for both grade 9 and men's events
read_csv(file_path_grade_9, team_scores_grade_9, individual_results_grade_9)
read_csv(file_path_men, team_scores_men, individual_results_men)

# Filter Grade 9 and Grade 10 Results
grade_9_results = [result for result in individual_results_grade_9 if result[1].strip() == "9"]
grade_10_results = [result for result in individual_results_grade_9 if result[1].strip() == "10"]

# Combine individual results for top 10 athletes across both datasets and sort by time
combined_individual_results = individual_results_grade_9 + individual_results_men
combined_individual_results = sorted(combined_individual_results, key=lambda x: x[4])  # Assuming time is at index 4

# Get the top 10 athletes
top_10_athletes = combined_individual_results[:10]

# Function to generate HTML content for a page
def generate_html_content(title, file_name, team_data, individual_data, include_table=False, include_top_results_heading=True):
    nav_bar = """
    <nav>
        <a href="results.html">Women's Results</a> |
        <a href="mens_results.html">Men's Results</a> |
        <a href="results_overall.html">Top 10 Athletes Across All Genders</a> |
        <a href="grade_9_results.html">Grade 9 Results</a> |
        <a href="grade_10_results.html">Grade 10 Results</a> |
        <a href="index.html">Welcome Page</a>
    </nav>
    """

    # Main HTML structure without <h1> header to prevent duplication
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
   {nav_bar}

   <main id="content">
       <section id="event-title">
           <h2>{title}</h2>
       </section>
    """

    # Include the team scores table only if specified
    if include_table:
        html_content += """
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
    """

    # Include the "Top Results" heading only if specified
    if include_top_results_heading:
        html_content += """
       <section id="individual-results">
           <h2>Top Results</h2>
    """
    else:
        html_content += """
       <section id="individual-results">
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
    with open(file_name, 'w') as file:
        file.write(html_content)
    print(f"{file_name} has been created successfully.")

# Generate HTML pages with the updated nav bar and titles
generate_html_content("Women's Results", "results.html", team_scores_grade_9[:3], individual_results_grade_9[:3], include_table=True)
generate_html_content("Top 10 Athletes Across All Genders", "results_overall.html", [], top_10_athletes, include_top_results_heading=False)
generate_html_content("Grade 9 Results", "grade_9_results.html", [], grade_9_results, include_top_results_heading=False)
generate_html_content("Grade 10 Results", "grade_10_results.html", [], grade_10_results, include_top_results_heading=False)
generate_html_content("Men's Results", "mens_results.html", team_scores_men, individual_results_men, include_table=True)
