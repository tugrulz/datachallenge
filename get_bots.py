import pandas as pd

# get_all_users
def get_all_users():
    df = pd.read_csv('./data/challenge_problem_two_21NOV.csv', usecols = ['screen_name'])
    df = df.screen_name.value_counts().reset_index()
    df.columns = ['screen_name', 'count']
    df.to_csv('output/all_users.csv', index=False)

def bot_score_compute_means():
    df = pd.read_csv('./data/palestine_botscores_after2022.csv')
    mean_by_screen_name = df.groupby('screen_name')['bot_score_english', 'bot_score_universal'].mean().reset_index()
    mean_by_screen_name.columns = ['screen_name', 'bot_score_english_mean', 'bot_score_universal_mean']
    std_by_screen_name = df.groupby('screen_name')['bot_score_english', 'bot_score_universal'].std().reset_index()
    std_by_screen_name.columns = ['screen_name', 'bot_score_english_std', 'bot_score_universal_std']
    mean_by_screen_name = mean_by_screen_name.merge(std_by_screen_name, on = 'screen_name')

    df2 = pd.read_csv('./data/palestine_botscores_before2022.csv')
    mean_by_screen_name2 = df2.groupby('screen_name')['bot_score_english', 'bot_score_universal'].mean().reset_index()
    mean_by_screen_name2.columns = ['screen_name', 'bot_score_english_mean', 'bot_score_universal_mean']
    std_by_screen_name2 = df2.groupby('screen_name')['bot_score_english', 'bot_score_universal'].std().reset_index()
    std_by_screen_name2.columns = ['screen_name', 'bot_score_english_std', 'bot_score_universal_std']
    mean_by_screen_name2 = mean_by_screen_name2.merge(std_by_screen_name2, on = 'screen_name')

    df3 = pd.concat([df, df2])
    df3 = df3.reset_index(drop = True)
    mean_by_screen_name3 = df3.groupby('screen_name')['bot_score_english', 'bot_score_universal'].mean().reset_index()
    mean_by_screen_name3.columns = ['screen_name', 'bot_score_english_mean_all', 'bot_score_universal_mean_all']
    std_by_screen_name3 = df3.groupby('screen_name')['bot_score_english', 'bot_score_universal'].std().reset_index()
    std_by_screen_name3.columns = ['screen_name', 'bot_score_english_std_all', 'bot_score_universal_std_all']
    mean_by_screen_name3 = mean_by_screen_name3.merge(std_by_screen_name3, on = 'screen_name')

    mean_by_screen_name = mean_by_screen_name.merge(mean_by_screen_name2, on = 'screen_name', suffixes = ('_after2022', '_before2022'))
    mean_by_screen_name = mean_by_screen_name.merge(mean_by_screen_name3, on = 'screen_name')
    mean_by_screen_name.to_csv('data/palestine_bot_scores.csv', index=False)


bot_score_compute_means()
exit()


# db_params = {
#     'host': 'localhost',
#     'port': 'your_port',
#     'database': 'your_database',
#     'user': 'your_user',
#     'password': 'your_password'
# }

conn = psycopg2.connect(**{'database':'botometer'})

sql_query = "SELECT screen_name, bot_score_english, bot_score_universal, most_recent_tweet FROM botscore;"


sql_query = "SELECT screen_name, bot_score_english, bot_score_universal, most_recent_tweet FROM botscore LIMIT 1000000;"
sql_query = "SELECT screen_name, bot_score_english, bot_score_universal, most_recent_tweet FROM botscore;"
sql_query = "SELECT screen_name, bot_score_english, bot_score_universal, most_recent_tweet FROM botscore WHERE most_recent_tweet >= '2022-01-01';"

df = pd.read_sql(sql_query, conn)
df.to_csv('/nobackup/telmas/botometer_after2022.csv', index=False)

output_csv_path = '/nobackup/telmas/botometer.csv'
