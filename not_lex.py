import pandas as pd

# 1️ Загрузка данных и удаление первого столбца
df = pd.read_csv('nodes_parameters_300.csv')
df.drop(columns=[df.columns[0]], inplace=True)

# Определяем последний столбец (его не будем учитывать в расчетах)
last_col = df.columns[-1]
calc_cols = ['Response Time (ms)', 'Task Queue Length', 'Node Performance (Score)']
selected_df = df[calc_cols]

# 2️ Преобразуем все столбцы в числовой формат (можно оставить последний — для вывода)
for col in df.columns:
    df[col] = (
        df[col].astype(str)
               .str.replace('%','',regex=False)
               .str.replace(',','.',regex=False)
    )
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 3️ Размер «топ‑50%»
half_count = int(len(df) * 0.02)

# 4️ Собираем выборки только по вычисляемым столбцам
special = ['Response Time (ms)', 'Task Queue Length']
top_sets = []
for col in calc_cols:
    if col in special:
        top_sets.append(df.nsmallest(half_count, col))
    else:
        top_sets.append(df.nlargest(half_count, col))

# 5️ Объединяем и удаляем дубликаты
union_df = pd.concat(top_sets, ignore_index=True).drop_duplicates().reset_index(drop=True)

# 6️ Лексикографическая сортировка без учета последнего столбца
ascending = [col in special for col in calc_cols]
union_sorted = union_df.sort_values(by=list(calc_cols), ascending=ascending).reset_index(drop=True)

# 7️ Сохраняем результат (последний столбец остаётся в выходном файле, но не влиял на расчёты)
output_path = 'not_lex.csv'
union_sorted.to_csv(output_path, index=False)

print(f'Готово — {len(union_sorted)} строк сохранены в {output_path}')