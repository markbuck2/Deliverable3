import os

# Path to the CSV file and image directory
file_path = 'SEC_Jamboree_1_Womens_5000_Meters_Junior_Varsity_24.csv'
image_dir = 'images'

# Check if the CSV file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")
    
# Read the file and handle format issues
try:
    with open(file_path, 'r') as file:
        lines = file.readlines()
except Exception as e:
    raise IOError(f"Error reading the file: {e}")

# Variables to store team scores and individual results
team_scores = []
individual_results = []

# Booleans to detect sections
in_team_scores = False
in_individual_results = False

# Capture data sections
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
    elif not line:  # Ignores empty lines
        continue

    data = line.split(',')

    # Add top 3 results for teams and individuals
    if in_team_scores and len(team_scores) < 3:
        if len(data) >= 3 and all(data[:3]):
            team_scores.append(data[:3])
    elif in_individual_results and len(individual_results) < 3:
        if len(data) >= 8 and all(data[:8]):
            individual_results.append(data[:8])

# Function to generate HTML content for a page
def generate_html_content(title, welcome_link, file_name):
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
       <a href="{welcome_link}" class="Welcome Page">Welcome page</a>
   </header>

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
    for index, score in enumerate(team_scores):
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
           <h2>Top 3 Results</h2>
    """

    for index, result in enumerate(individual_results):
        if len(result) >= 7:
            athlete_link = result[3]
            athlete_id = athlete_link.split('/')[-2]
            image_path = os.path.join(image_dir, f"{athlete_id}.jpg")
            if os.path.exists(image_path):
                image_path = f"images/{athlete_id}.jpg"
            else:
                image_path = f"images/default.jpg"
        
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

   <!-- JavaScript for interactivity -->
   <script src="js/script.js"></script>
</body>
</html>
    """
    # Write the HTML content to the specified file
    with open(file_name, 'w') as file:
        file.write(html_content)
    print(f"{file_name} has been created successfully.")

# Generate the results HTML page
generate_html_content("Results Page", "index.html", "results.html")
