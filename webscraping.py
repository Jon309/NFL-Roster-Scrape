import bs4
import requests
import pandas as pd

roster_list = []

def get_player_info(team_url):
    page = requests.get(team_url)

    # Create BeautifulSoup object
    soup = bs4.BeautifulSoup(page.text, features="html.parser")

    try:
        for tr in soup.find_all('tr')[2:]:
            tds = tr.find_all('td')

            player_name = tds[0].text.strip()
            player_number = tds[1].text
            player_position = tds[2].text
            player_height = tds[3].text
            player_weight = tds[4].text
            player_age = tds[5].text
            player_experience = tds[6].text
            player_college = tds[7].text

            player = {
                "Name": player_name,
                "Number": player_number,
                "Position": player_position,
                "Height": player_height,
                "Weight": player_weight,
                "Age": player_age,
                "Experience": player_experience,
                "College": player_college
            }

            roster_list.append(player)

    except IndexError:
        print("Index out of range")

def createDataFrame(roster_list):
    # Create pandas DataFrame from list
    team_df = pd.DataFrame(roster_list,
                             columns=['Name', 'Number', 'Position', 'Height',
                                      'Weight', 'Age', "Experience", "College"
                                      ])

    team_df['Number'] = team_df['Number'].astype(int)
    team_df['Age'] = pd.to_numeric(team_df['Age'])
    team_df['Experience'] = pd.to_numeric(team_df['Experience'])
    team_df['Weight'] = pd.to_numeric(team_df['Weight'])

    return team_df

def printRoster():
    for player in sorted(roster_list):
        print(player)


def findExp(df, operator, years):
    if (operator.lower() == 'greater'):
        df_exp = df[df["Experience"] >= years]
    elif (operator.lower() == 'less'):
        df_exp = df[df["Experience"] <= years]
    else:
        print("Incorrect Operator")
    return df_exp

def findPosition(df, position):
    df_pos = df[df['Position'] == position.upper()]
    return df_pos

if __name__ == '__main__':
    get_player_info('https://www.baltimoreravens.com/team/players-roster/')

    ravens_df = createDataFrame(roster_list)
    print(ravens_df.to_string())

    # Find players with less than 2 years experience
    print(findExp(ravens_df, 'less', 2).to_string())

    # Find players that are QBs
    print(findPosition(ravens_df, 'QB'))
