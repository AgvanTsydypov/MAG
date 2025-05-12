import pandas as pd

def sort_and_filter_df(df, sort_column, ascending=True, percent=0.3):
    """
    Сортирует DataFrame по указанной колонке и возвращает верхнюю часть данных,
    соответствующую заданному проценту строк.
    
    Аргументы:
        df (pd.DataFrame): Входной DataFrame.
        sort_column (str): Название колонки для сортировки.
        ascending (bool): True для сортировки по возрастанию, False для убывания.
        percent (float): Процент строк для возврата (по умолчанию 75 означает вернуть 75% строк).
    
    Возвращает:
        pd.DataFrame: Отсортированный и отфильтрованный DataFrame.
    """
    # # Проверка корректности переданного процента
    # if not (0 < percent <= 100):
    #     raise ValueError("Параметр 'percent' должен быть больше 0 и не превышать 100.")
    
    # Сортировка DataFrame
    df_sorted = df.sort_values(by=sort_column, ascending=ascending)

    df = get_best_results(df_sorted, sort_column, best_higher=ascending, deviation=percent)

    return df

    # best = df_sorted.iloc[0][i]
    # # print(best)

    # sorted_indices = (df_sorted[i] - best).abs().argsort()
    # return df_sorted.loc[sorted_indices].head(5)
    
    # # Вычисление количества строк для возврата
    # n_rows = int(len(df_sorted) * (percent / 100))
    # if n_rows < 1:
    #     n_rows = 1  # Гарантируем, что хотя бы одна строка будет возвращена
    
    # return df_sorted.iloc[:n_rows]

def get_best_results(df, field, deviation=0.3, best_higher=True):
    if best_higher:
        best_value = df[field].max()
        # Относительное отклонение: (best_value - value) / best_value <= deviation,
        # что эквивалентно value >= best_value * (1 - deviation)
        threshold = best_value * (1 - deviation)
        return df[df[field] >= threshold]
    else:
        best_value = df[field].min()
        # Для случая, когда меньшее значение лучше, отклонение считается так:
        # (value - best_value) / best_value <= deviation, что эквивалентно value <= best_value * (1 + deviation)
        threshold = best_value * (1 + deviation)
        return df[df[field] <= threshold]

# 1️ Загрузка данных и удаление первого столбца
df = pd.read_csv('nodes_parameters_300.csv')
# df.drop(columns=[df.columns[0]], inplace=True)

desc = ['Response Time (ms)', 'Task Queue Length'] # 'Task Queue Length' 'Active Conns'
asc = ['Node Performance (Score)']

# 2️ Преобразуем все столбцы в числовой формат (можно оставить последний — для вывода)
for col in df.columns:
    df[col] = (
        df[col].astype(str)
               .str.replace('%','',regex=False)
               .str.replace(',','.',regex=False)
    )
    df[col] = pd.to_numeric(df[col], errors='coerce')

correlation_percentage = df.corr() * 100
print(correlation_percentage)

print(f'{len(df)} - Изначальное количество строк')

for i in desc:
    percent = 0.1
    if i == 'Task Queue Length':
        percent = 2
    df = sort_and_filter_df(df, i, ascending=False, percent=percent)
    print(f'{len(df)} - текущее количество строк после фильтра по полю ' + i)
    output_path = f'g\{i}lex.csv'
    df.to_csv(output_path, index=False)

for i in asc:
    df = sort_and_filter_df(df, i)
    print(f'{len(df)} - текущее количество строк после фильтра по полю ' + i)
    output_path = f'g\{i}lex.csv'
    df.to_csv(output_path, index=False)

output_path = 'lex.csv'
df.to_csv(output_path, index=False)

print(f'Готово — {len(df)} строк сохранены в {output_path}')