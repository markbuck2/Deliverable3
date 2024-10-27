import os

# Path to the CSV file
file_path = 'SEC_Jamboree_1_Womens_5000_Meters_Junior_Varsity_24.csv'
image_dir = 'images'

if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")
    
# Reading the file and handling potential format issues
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

# For loop to capture data sections
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
    elif not line:  # Ignores the empty lines
        continue

    data = line.split(',')

    # Validate CSV structure for teams and individuals and limit to top 3 results
    if in_team_scores and len(team_scores) < 3:
        if len(data) >= 3 and all(data[:3]):
            team_scores.append(data[:3])
        else:
            print(f"Warning: Incorrect or incomplete team score data: {line}")
    elif in_individual_results and len(individual_results) < 3:
        if len(data) >= 8 and all(data[:8]):
            individual_results.append(data[:8])
        else:
            print(f"Warning: Incorrect or incomplete individual result data: {line}")

# Report any issues if less than 3 entries are found
if len(team_scores) < 3:
    print("Warning: Less than 3 valid team scores found.")
if len(individual_results) < 3:
    print("Warning: Less than 3 valid individual results found.")

# HTML content to be constructed dynamically
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <link rel="stylesheet" href="css/style.css">
   <title>Client Project - Results</title>
</head>
<body>
   <header id="main-header">
       <h1>Event Summary</h1>
       <a href="index.html" class="Welcome Page">Welcome page</a>
   </header>

   <main id="content">
       <section id="event-title">
           <h2>SEC Jamboree #1 Womens 5000 Meters Junior Varsity</h2>
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

# Adds top 3 team scores to the HTML content
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

# Close the team scores table tag
html_content += """
               </tbody>
           </table>
       </section>
"""

# Creates the HTML content for top 3 individual athletes
html_content += """
       <section id="individual-results">
           <h2>Top 3 Results</h2>
"""

for index, result in enumerate(individual_results):
    if len(result) >= 7:  # Ensure all required data is present
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

# Closing the individual results section and main content
html_content += """
       </section>
   </main>
   <footer id="main-footer">
       <p>&copy; 2024 Client Project - All rights reserved.</p>
   </footer>
   <button id="dark-mode-toggle" class="mode-toggle">Toggle Dark Mode</button>

   <!-- Dark mode toggle JavaScript -->
   <script>
     const toggleButton = document.getElementById('dark-mode-toggle');
     const currentTheme = localStorage.getItem('theme');

     // Apply the user's last preference on page load
     if (currentTheme === 'dark') {
         document.body.classList.add('dark-mode');
     }

     // Add event listener to toggle dark mode
     toggleButton.addEventListener('click', () => {
       document.body.classList.toggle('dark-mode');
       
       // Save the user's preference
       if (document.body.classList.contains('dark-mode')) {
         localStorage.setItem('theme', 'dark');
       } else {
         localStorage.setItem('theme', 'light');
       }
     });
   </script>
</body>
</html>
"""

# Save the HTML content to a file
html_file_path = 'results.html'
try:
    with open(html_file_path, 'w') as file:
        file.write(html_content)
    print(f'HTML file generated: {html_file_path}')
except Exception as e:
    raise IOError(f"Error writing to the file: {e}")
