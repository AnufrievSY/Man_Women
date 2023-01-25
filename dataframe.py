from fuzzywuzzy import process # функция сравнения со списком из бибилиотеки для нечеткого сравнения строк
import pandas as pd # для создания датафрейма
df = pd.read_csv('МЖ.csv') # загружаем датафрейм
df = df.drop_duplicates() # удаляем дубликаты
# удаляем ограничения на вывод максимального колличества колонок, строк и символом в строке
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def find(df, index):
    v_1 = df.loc[index, 'Описание']
    v_2 = df['Описание'].to_list()

    index = []
    name = []
    views = []
    result = []

    for i in process.extract(v_1, v_2, limit=len(v_2)):
        idx = df.loc[df['Описание'] == i[0]].index[0]
        index.append(idx)
        name.append(df.loc[idx, 'Название'])
        result.append(i[1])
        views.append(df.loc[idx, 'Суммарное кол-во просмотров'])

    result = pd.DataFrame({'название': name, 'точность совпадения': result, 'кол-во просмотров': views}, index=index)
    result = result.iloc[1:]
    result = result.loc[result['точность совпадения'] > 80]
    result = result.loc[result['кол-во просмотров'] != 0]
    result = df.loc[result.index].sort_values('Суммарное кол-во просмотров', ascending=False)
    return result