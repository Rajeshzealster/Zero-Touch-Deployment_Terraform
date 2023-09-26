import csv
import pandas as pd
import random
from flask import Flask, render_template, jsonify, request, redirect, url_for
import numpy as np

app = Flask(__name__, static_folder='static')

# Sample list of team names (you can replace this with your data)
teams = ["Saran_Team1", "Karthik_Team2", "Sudeep_Team3", "JwalaPrasad_Team4", "SouravKumar_Team5", "NVinay_Team6", "Sourabh_Team7", "Mahesh_Team8",
         "AkashBhati_Team9", "Sachi_Team10"]

val_to_file={1:"Saran_Team1", 2:"Karthik_Team2", 3:"Sudeep_Team3", 4:"JwalaPrasad_Team4", 5:"SouravKumar_Team5", 6:"NVinay_Team6", 7:"Sourabh_Team7", 8:"Mahesh_Team8",
         9:"AkashBhati_Team9", 10:"Sachi_Team10"}


# Define a function to read player data from players.csv  for displaying team_info
def read_player_data():
    player_data = {}
    with open('players.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player_data[row['rowid']] = row
    return player_data

# Load player data from CSV into a Pandas DataFrame
def load_player_data():
    return pd.read_csv('players.csv')
players_data = load_player_data()

# Preparing a list for random number generation
global choiceList
choiceList = list(np.arange(0,len(players_data)))
icon_players_list=[25,116,218,18,94,93,101,110,217,216]
#choiceList=choiceList-icon_players_list
choiceList= [x for x in choiceList if x+1 not in icon_players_list]

# Restart Scenario
'''duplicate = []
with open('soldList.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        duplicate.append(row)
choiceList = [x for x in choiceList if x not in duplicate] # remove alreadyauctioned players

'''


# Index route
@app.route('/')
def index():
    data = []
    # Read data from CSV file
    with open('data.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

# Create a list of tuples by zipping data and teams
    data_and_teams = list(zip(data, teams))

    return render_template('index.html', data_and_teams=data_and_teams)
    #return render_template('index.html',teams=teams)


# API route to fetch player details by a random index
@app.route('/get_next_player')
def get_next_player():
    # Generate a random index within the range of available players
    global random_index
    global player_info
    random_index = random.choice(choiceList)
    
    # Select the player by the random index
    random_player = players_data.iloc[random_index]

    # Convert the player information to a dictionary
    player_info = random_player.to_dict()

    # Pass the player info as parameters to the player_details.html template
    return render_template('player_details.html', player_info=player_info)



# Index route
@app.route('/updateHome', methods=['POST'])
def updateHome():
    data = []
    # Read data from CSV file
    with open('data.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    df = pd.DataFrame(data) 
    if request.method == 'POST':
        team_name = int(request.form.get('teamSelect')) - 1
        player_price = int(request.form.get('playerPrice'))
        #player_ID = random_index
        df.iloc[team_name]['Amount used'] = int(df.iloc[team_name]['Amount used']) + player_price
        df.iloc[team_name]['Amount left'] = int(df.iloc[team_name]['Amount left']) - player_price
        df.iloc[team_name]['No of Players'] = int(df.iloc[team_name]['No of Players'])  + 1
        
        # Find the team in the data
        df.to_csv('data.csv', index=True)
        
        

        # Open the CSV file in append mode and write the new data
        with open("soldList.csv", mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([random_index+1])
        #choiceList.remove(random_index)
        #fileName = 'team'+str(team_name + 1 )+'.csv' 
        fileName=val_to_file[team_name+1] +".csv"
        with open(fileName, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([random_index+1])
    data = []
    # Read data from CSV file
    with open('data.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row) 
    data_and_teams = list(zip(data, teams))
    
    with open('generated_list.txt','a') as gen:
        gen.write(str(random_index+1)+"\n")
    choiceList.remove(random_index)   
    return render_template('index.html', data_and_teams=data_and_teams)

@app.route('/unsold')
def unsold():
    
    with open('players.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        source_data = list(csv_reader)
        row_to_append = source_data[random_index+1]

    # Open the target CSV file for appending
    with open("unsold.csv", mode='a', newline='') as target_file:
        csv_writer = csv.writer(target_file)
    # Write the row from the source CSV to the target CSV
        csv_writer.writerow(row_to_append)
        
    
    data = []
    # Read data from CSV file
    with open('data.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    
    data_and_teams = list(zip(data, teams))
    choiceList.remove(random_index)
    return render_template('index.html', data_and_teams=data_and_teams)

@app.route('/<team_name>')
def team_info(team_name):
    player_data = read_player_data()

    # Assuming you have a CSV file for each team with player IDs
    # Replace 'teamX.csv' with the actual filename for each team
    team_filename = f'{team_name}.csv'

    team_data = []
    with open(team_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            player_id = row[0]
            if player_id in player_data:
                team_data.append(player_data[player_id])

    return render_template('team_info.html', team_name=team_name, team_info=team_data)


if __name__ == '__main__':
    app.run(debug=True)



