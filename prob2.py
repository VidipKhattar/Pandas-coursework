import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('eurocup_2020_results.csv', sep=',').replace('"', '', regex=True)
# Part A.
# prints the retrieved data
print(data)

# uses panda dataframe framework so to manipulate the data
df = pd.DataFrame(data)

print(df)
print(list(df.columns))

# Part B
for index in range(len(df)):
    df.loc[index, 'team_name_home'] = (str(df.loc[index, 'team_name_home']))[1:-1]
    df.loc[index, 'team_name_away'] = (str(df.loc[index, 'team_name_away']))[1:-1]

print(df['team_name_home'].unique())

# Part C
df_G = df[(df['stage'].isin(
    [' Group stage: Matchday 1 ', ' Group stage: Matchday 2 ', ' Group stage: Matchday 3 ']))]


# Part D
def calcScore(row):
    if row['team_home_score'] > row['team_away_score']:
        return 3, 0
    elif row['team_home_score'] < row['team_away_score']:
        return 0, 3
    else:
        return 1, 1


print(calcScore(df_G.loc[17, :]))

# Part E
x = (df_G.apply(lambda row: calcScore(row), axis=1))
for i in x.index.tolist():
    df_G.loc[i, 'team_home_points'] = (x[i][0])
    df_G.loc[i, 'team_away_points'] = (x[i][1])

print(df_G)


# Part F
def GetGroupTeams(team_name):
    group_teams = []
    group_teams.append(team_name)
    for i in (df_G.index.tolist()):
        if (df.loc[i, "team_name_home"])[:] == team_name:
            group_teams.append(df.loc[i, "team_name_away"])
        elif (df.loc[i, "team_name_away"])[:] == team_name:
            group_teams.append(df.loc[i, "team_name_home"])
    return sorted(group_teams)


print(GetGroupTeams('England'))


# Part G
def GetGroupRows(team_name):
    row_list = []
    team_list = GetGroupTeams(team_name)
    for i in range(len(df_G)):
        if df_G.loc[i + 15, 'team_name_home'] in team_list:
            row_list.append(df_G.index[i])
    new_df = df_G[df_G.index.isin(row_list)]
    return new_df


x = GetGroupRows('England')

for index, row in x.iterrows():
    print(row)


# Part H
def GetTeamStats(team_name):
    stat_dict = {'Points': 0, 'Goals Scored': 0, 'Goals Conceded': 0}
    for index, row in (GetGroupRows(team_name)).iterrows():
        if row["team_name_home"] == team_name:
            stat_dict['Points'] += row["team_home_points"]
            stat_dict['Goals Scored'] += row["team_home_score"]
            stat_dict['Goals Conceded'] += row["team_away_score"]
        elif row["team_name_away"] == team_name:
            stat_dict['Points'] += row["team_away_points"]
            stat_dict['Goals Scored'] += row["team_away_score"]
            stat_dict['Goals Conceded'] += row["team_home_score"]
    return stat_dict


print(GetTeamStats('England'))


# Part I
def GetGroupTable(team_name):
    list_of_dict = []
    group_teams = GetGroupTeams(team_name)
    for team in group_teams:
        dict = GetTeamStats(team)
        dict['Goal Difference'] = dict['Goals Scored'] - dict['Goals Conceded']
        dict["Country"] = team
        list_of_dict.append(dict)
    point_df = pd.DataFrame(list_of_dict)
    point_df.reset_index(drop=True, inplace=True)
    point_df = point_df.sort_values(by='Goals Scored', ascending=[False])
    point_df = point_df.sort_values(by='Points', ascending=[False])
    countries_list = (point_df["Country"]).tolist()
    point_df = point_df.set_index([pd.Index(countries_list)])
    del point_df["Country"]
    return point_df


print(GetGroupTable('England'))
print(GetGroupTable('Italy'))


# Part J
def GetAllGroupTables():
    list_of_groups = []
    list_of_tables = []
    for country in df_G["team_name_home"].unique():
        val = GetGroupTeams(country)
        if val not in list_of_groups:
            list_of_groups.append(val)
    for el in list_of_groups:
        list_of_tables.append(GetGroupTable(el[0]))
    return list_of_tables


print(GetAllGroupTables())

#Part K

fig3, ax3 = plt.subplots()

poss_list = df["possession_home"].tolist()
pss_list = []
duels_list = df["total_shots_home"].tolist()
for el in poss_list:
    pss_list.append(int(el.strip('%')))

print(poss_list)


print(len(poss_list))
print(len(duels_list))

ax3.scatter(pss_list, duels_list, c="aqua", alpha=0.5)
ax3.set_title("Possession vs Number of shots", fontsize=16)
ax3.set_ylabel("Number of shots", fontsize=13)
ax3.set_xlabel("Possession (%)", fontsize=13)

# To show the plot
plt.show()

# Graph shows percentage of duals won vs shots of each home team in a match It is known that if
# the possesion is higher the team is more likely to have the ball at more times Meaning it is
# likely that the team with more possesion will have a higher number of shots taken The graph
# shows a slight positive correlation between shots and percentage.Lower number of shots have
# lower percentage and vice versa
