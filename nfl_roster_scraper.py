import bs4
import requests
import pandas as pd
import teams


def get_player_info(team_url):
    roster_list = []
    page = requests.get(team_url)

    # Create BeautifulSoup object
    soup = bs4.BeautifulSoup(page.text, features="html.parser")

    try:
        for tr in soup.find_all('tr')[2:]:
            tds = tr.find_all('td')

            name = tds[0].text.strip()
            number = tds[1].text
            position = tds[2].text
            height = tds[3].text
            weight = tds[4].text
            age = tds[5].text
            experience = tds[6].text
            college = tds[7].text

            player = {
                "Name": name,
                "Number": number,
                "Position": position,
                "Height": height,
                "Weight": weight,
                "Age": age,
                "Experience": experience,
                "College": college
            }

            roster_list.append(player)

    except IndexError:
        print("Index out of range")

    return roster_list


def create_data_frame(roster_list):
    # Create pandas DataFrame from list
    team_df = pd.DataFrame(roster_list,
                           columns=['Name', 'Number', 'Position', 'Height',
                                    'Weight', 'Age', "Experience", "College"
                                    ])

    # team_df['Number'] = pd.to_numeric(team_df['Number'])
    # team_df['Age'] = pd.to_numeric(team_df['Age'])
    # team_df['Weight'] = pd.to_numeric(team_df['Weight'])

    return team_df


def find_exp(df, operator, years):
    if operator.lower() == 'greater':
        df_exp = df[df["Experience"] >= years]
    elif operator.lower() == 'less':
        df_exp = df[df["Experience"] <= years]
    else:
        print("Incorrect Operator")
    return df_exp


def find_position(df, position):
    df_pos = df[df['Position'] == position.upper()]
    return df_pos


def main():

    # # Ravens
    # ravens_roster = get_player_info(teams.urls['ravens'])
    # ravens_df = create_data_frame(ravens_roster)
    # print(ravens_df.to_string())
    #
    # # Find players that are QBs
    # print(find_position(ravens_df, 'QB').to_string())
    #
    # # Cardinals
    # cardinals_roster = get_player_info(teams.urls['cardinals'])
    # cardinals_df = create_data_frame(cardinals_roster)
    # print(cardinals_df.to_string())

    # Creates a DataFrame including every player from every NFL Team
    concat_all_teams()


def concat_all_teams():
    nfl_teams = []
    for team, url in teams.urls.items():
        team_roster = get_player_info(url)
        nfl_df = create_data_frame(team_roster)
        nfl_df['Team'] = team.title()
        nfl_teams.append(nfl_df)
    complete_df = pd.concat(nfl_teams)
    complete_df = complete_df.reset_index()
    complete_df.rename(columns={"index": "Team Index"}, inplace=True)
    print(complete_df.to_string())


if __name__ == '__main__':
    main()