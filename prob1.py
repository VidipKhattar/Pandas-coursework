import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('eurovision_winners.csv', sep=',').replace('"', '', regex=True)
# Part A.
# prints the retrieved data
# print(data)

# uses panda dataframe framework so to manipulate the data
df = pd.DataFrame(data)

# PartB
print(df[df['Year'].duplicated()])
# Year 1969 has 3 winners and no runner up, so the year 1969 has 2 additional rows

# Part C

limitDF = df[['Year', 'Points', 'Margin']]

print(limitDF)

# Part D

point_list = list(df['Points'])
year_list = list(df['Year'])
city_list = list((df['Host City']).unique())

no_of_host = {}

for city in city_list:
    for host in df['Host City']:
        if city == host:
            if city in no_of_host.keys():
                no_of_host[city] += 1
            else:
                no_of_host[city] = 1

sorted_dict = dict(sorted(no_of_host.items(), key=lambda item: item[1], reverse=True))

fig1, ax1 = plt.subplots()

ax1.hist(point_list, 7, facecolor='green', edgecolor='black', alpha=0.7)
ax1.set_title("Eurovision winner points histogram", fontsize=16)
ax1.set_ylabel("Frequency", fontsize=13)
ax1.set_xlabel("Winner points", fontsize=13)

# Part E
fig2, ax2 = plt.subplots()

ax2.plot(year_list, point_list, color='darkred', marker='D')
ax2.set_title("Points by Year", fontsize=16)
ax2.set_ylabel("Points", fontsize=13)
ax2.set_xlabel("Year", fontsize=13)

# Part F

plt.rcdefaults()
fig, ax = plt.subplots()

city_list = (list(sorted_dict.keys()))[:6]

no_of_host = (list(sorted_dict.values()))[:6]

ax.barh(city_list, no_of_host, align='center', color='salmon')
ax.set_yticks(city_list)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Number of times hosted')
ax.set_ylabel('City')
ax.set_title('Ranking of Top Hosting Cities (more than twice)')


# Part G

# a
def wordpoints(row):
    word_point = []
    song = (df["Song"][row]).split()
    points = df["Points"][row]
    for word in song:
        word_point.append((word, points))

    return word_point


word_point_total = []
final_list = []

# b
for i in df.apply(lambda row: wordpoints(row.name), axis=1):
    word_point_total.append(i)

for word in word_point_total:
    for el in word:
        final_list.append(el)

# c
word_points = pd.DataFrame(final_list, columns=['word', 'points'])

# d
dup_list = word_points.pivot_table(columns=['word'], aggfunc='size')
dup_list = dup_list[dup_list > 2]

# e
word_point_dict = {}
for row in range(len(word_points)):
    print(word_points.loc[row, 'word'])
    val = word_points.loc[row, 'word']
    if val in dup_list:
        if val in word_point_dict:
            word_point_dict[val] += word_points.loc[row, 'points']
        else:
            word_point_dict[val] = word_points.loc[row, 'points']

dict_dup = dup_list.to_dict()

for word in word_point_dict:
    word_point_dict[word] = word_point_dict[word] / dict_dup[word]

# f
print(word_point_dict)
marklist = sorted(word_point_dict.items(), key=lambda x: x[1])
sortdict = dict(marklist)

word_list = (list(sortdict.keys()))[-1::-1]
points_list = (list(sortdict.values()))[-1::-1]

fig, ax = plt.subplots()

ax.bar(word_list, points_list, color='lightpink')
ax.set_xlabel('Word')
ax.set_ylabel('Average Points')
ax.set_title('Ranking of Song Words (at least 3 occurrences')

# Part H

fig3, ax3 = plt.subplots()

year_list = df["Year"].tolist()
margin_list = df["Margin"].tolist()
points2_list = df["Points"].tolist()
print(points_list)

ax3.scatter(year_list, points2_list, c="aqua", alpha=0.5)
ax3.set_title("Margin between winner and runner up", fontsize=16)
ax3.set_ylabel("Margin of Points", fontsize=13)
ax3.set_xlabel("Year", fontsize=13)

# To show the plot
plt.show()

# This graph shows the margin of points between the runner up and winner every year
# We can see that as time moves forward, the number of points increase and therefore the margin
# the winner and runner up increasses, the last 4 years saw and huge increase in margin
# The graph is shown to be exponential showing how the winners lead gets bigger and bigger each year
