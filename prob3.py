import matplotlib
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('owid-covid-data.csv', sep=',').replace('"', '', regex=True)
# Part A.
# uses panda datagram framework so to manipulate the data
df = pd.DataFrame(data)

print(df)
print(list(df.columns))

# Part B
print(df['date'].unique())

# Part C
# Part D
for i in df['iso_code'].unique():
    if "OWID_" in i:
        index_names = df[df['iso_code'] == i].index
        df.drop(index_names, inplace=True)

print(len(df['iso_code'].unique()))

# Part E
df_v = df[df['new_vaccinations'].notnull()]
print(df_v['date'].min())

# Part F
df_v['total_vaccinations_per_million'] = (df_v['total_vaccinations_per_hundred'] * 10000)

# Part G
df_v[['date']] = df_v[['date']].apply(pd.to_datetime)
df_v['DaysSince3Dec20'] = (df_v['date'] - df_v['date'].min()).dt.days

# Part H
country_df = pd.DataFrame()
grouped_df = df_v.groupby('iso_code')
country_df['total_vaccinations_per_hundred'] = grouped_df["total_vaccinations_per_hundred"].max()
country_df['total_deaths_per_million_earliest'] = grouped_df["total_deaths_per_million"].min()
country_df['total_deaths_per_million'] = grouped_df["total_deaths_per_million"].max()

for i in country_df.index:
    country_df.loc[i, 'TotalDeathPerMSinceVac'] = country_df.loc[i, 'total_deaths_per_million'] - \
                                                  country_df.loc[
                                                      i, 'total_deaths_per_million_earliest']

# Part I
fig1, ax1 = plt.subplots()
ax1.scatter(country_df['total_vaccinations_per_hundred'].tolist(),
            country_df['TotalDeathPerMSinceVac'].tolist(), c="aqua", alpha=0.5)

# To show the plot
ax1.set_yscale('log')
ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.xlabel('Total Vaccinations (per 100)')
plt.ylabel('Total Death Since December 2020 (per million)')
plt.title("Total Deaths Since Vaccines and Total Vaccination per Country")
ax1.annotate("CUB", (country_df.loc["CUB", "total_vaccinations_per_hundred"],
                     (country_df.loc["CUB", "TotalDeathPerMSinceVac"])))
ax1.annotate("CHN", (country_df.loc["CHN", "total_vaccinations_per_hundred"],
                     (country_df.loc["CHN", "TotalDeathPerMSinceVac"])))
ax1.annotate("GBR", (country_df.loc["GBR", "total_vaccinations_per_hundred"],
                     (country_df.loc["GBR", "TotalDeathPerMSinceVac"])))
ax1.annotate("IND", (country_df.loc["IND", "total_vaccinations_per_hundred"],
                     (country_df.loc["IND", "TotalDeathPerMSinceVac"])))

# Part J
df_GBR = df_v[df_v['iso_code'] == 'GBR']

# Part K
gbr_list = df_GBR.index.tolist()
df_GBR['total_vaccinations_per_hundred_smoothed'] = df_GBR.total_vaccinations_per_hundred.rolling(
    7).mean().tolist()
x = df_GBR['DaysSince3Dec20'].to_list()
GBR_y = df_GBR['total_vaccinations_per_million'].to_list()
GBR_y1 = df_GBR['icu_patients_per_million'].to_list()
GBR_y2 = df_GBR['total_cases_per_million'].to_list()
GBR_y3 = df_GBR['total_deaths_per_million'].to_list()

df_ZAF = df_v[df_v['iso_code'] == 'ZAF']

x1 = df_ZAF['DaysSince3Dec20'].to_list()
ZAF_y = df_ZAF['total_vaccinations_per_million'].to_list()
ZAF_y1 = df_ZAF['icu_patients_per_million'].to_list()
ZAF_y2 = df_ZAF['total_cases_per_million'].to_list()
ZAF_y3 = df_ZAF['total_deaths_per_million'].to_list()

df_KOR = df_v[df_v['iso_code'] == 'KOR']

x2 = df_KOR['DaysSince3Dec20'].to_list()
KOR_y = df_KOR['total_vaccinations_per_million'].to_list()
KOR_y1 = df_KOR['icu_patients_per_million'].to_list()
KOR_y2 = df_KOR['total_cases_per_million'].to_list()
KOR_y3 = df_KOR['total_deaths_per_million'].to_list()

fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(18, 5))
plt.title("Total COVID-19 cases, ICU patients, death, and vaccinations per million in: "
          "United Kingdom, South Africa, South Korea")
plt.xlabel("Total Numbers per Million")
plt.ylabel("Days since 2020-12-03")
ax[0].set_yscale('log')
ax[1].set_yscale('log')
ax[2].set_yscale('log')

ax[0].plot(x[61:], GBR_y2[61:], label='cases', color="yellow")
ax[0].plot(x[61:], GBR_y1[61:], label='icu', color="red")
ax[0].plot(x[61:], GBR_y3[61:], label='death', color="black")
ax[0].plot(x[61:], GBR_y[61:], label='vacc', color="green", linestyle="--")
fig.legend(['Cases', 'ICU patients', 'Deaths', 'Vaccinations'])

ax[1].plot(x1[22:], ZAF_y2[22:], label='cases', color="yellow")
ax[1].plot(x1[22:], ZAF_y1[22:], label='icu', color="red")
ax[1].plot(x1[22:], ZAF_y3[22:], label='death', color="black")
ax[1].plot(x1[22:], ZAF_y[22:], label='vacc', color="green", linestyle="--")

ax[2].plot(x2[22:], KOR_y2[22:], label='cases', color="yellow")
ax[2].plot(x2[22:], KOR_y1[22:], label='icu', color="red")
ax[2].plot(x2[22:], KOR_y3[22:], label='death', color="black")
ax[2].plot(x2[22:], KOR_y[22:], label='vacc', color="green", linestyle="--")

# Part M
for i in df_GBR:
    print(i)

x = df_GBR['date'].to_list()
GBR_y = df_GBR['new_deaths'].to_list()

fig4, ax4 = plt.subplots()
plt.title("number of new daily cases per day in the UK")
plt.xlabel("number of new cases")
plt.xlabel("Date")

ax4.plot(x, GBR_y, label='cases', color="red")

# This graph show the new number of daily cases in the UK The first date of the graph is the
# first date of vaccination in the uk Therefore we can see the direct effect that the vaccine has
# the the daily case rate since there is an immediate and steep reduce in daily cases


plt.show()
