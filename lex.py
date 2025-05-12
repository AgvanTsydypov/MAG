import pandas as pd

def sort_and_filter_df(df, sort_column, ascending=True, percent=0.3):
    """
    Сортирует DataFrame по указанной колонке и возвращает верхнюю часть данных,
    соответствующую заданному проценту строк.

    Аргументы:
        df (pd.DataFrame): Входной DataFrame.
        sort_column (str): Название колонки для сортировки.
        ascending (bool): True для сортировки по возрастанию, False для убывания.
        percent (float): Процент допустимого отклонения от лучшего значения.

    Возвращает:
        pd.DataFrame: Отсортированный и отфильтрованный DataFrame.
    """
    df_sorted = df.sort_values(by=sort_column, ascending=ascending)
    df = get_best_results(df_sorted, sort_column, best_higher=ascending, deviation=percent)
    return df

def get_best_results(df, field, deviation=0.3, best_higher=True):
    if best_higher:
        best_value = df[field].max()
        threshold = best_value * (1 - deviation)
        return df[df[field] >= threshold]
    else:
        best_value = df[field].min()
        threshold = best_value * (1 + deviation)
        return df[df[field] <= threshold]

# 1️⃣ Загрузка данных
df = pd.read_csv('nodes_parameters_300.csv')

# 2️⃣ Преобразуем столбец 'Selection Probability' отдельно: удалим %, заменим , и приведём к числу
df['Selection Probability'] = (
    df['Selection Probability'].astype(str)
                               .str.replace('%', '', regex=False)
                               .str.replace(',', '.', regex=False)
)
df['Selection Probability'] = pd.to_numeric(df['Selection Probability'], errors='coerce')

# 3️⃣ Преобразуем все числовые столбцы, кроме 'Node ID' и 'Selection Probability'
for col in df.columns:
    if col in ['Node ID', 'Selection Probability']:
        continue
    df[col] = (
        df[col].astype(str)
               .str.replace(',', '.', regex=False)
    )
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 4️⃣ Распечатать корреляцию
correlation_percentage = df.select_dtypes(include='number').corr() * 100
print(correlation_percentage)

print(f'{len(df)} - Изначальное количество строк')

# 5️⃣ Последовательная фильтрация по убывающим метрикам
desc = ['Response Time (ms)', 'Task Queue Length']
asc = ['Node Performance (Score)']

for i in desc:
    percent = 0.1
    if i == 'Task Queue Length':
        percent = 2
    df = sort_and_filter_df(df, i, ascending=False, percent=percent)
    print(f'{len(df)} - текущее количество строк после фильтра по полю {i}')
    df.to_csv(f'g\\{i}lex.csv', index=False)

# 6️⃣ Фильтрация по возрастающей метрике
for i in asc:
    df = sort_and_filter_df(df, i)
    print(f'{len(df)} - текущее количество строк после фильтра по полю {i}')
    df.to_csv(f'g\\{i}lex.csv', index=False)

# 7️⃣ Финальный экспорт
output_path = 'lex.csv'
df.to_csv(output_path, index=False)
print(f'Готово — {len(df)} строк сохранены в {output_path}')