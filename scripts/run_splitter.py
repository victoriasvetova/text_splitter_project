import sys
import os

# Добавляем корень проекта в PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


import pandas as pd
from text_splitter.splitter import split_text
from text_splitter.utils import get_space_positions


# Пути из аргументов или значения по умолчанию
input_path = sys.argv[1] if len(sys.argv) > 1 else "data/dataset_1937770_3.txt"
output_path = sys.argv[2] if len(sys.argv) > 2 else "output/predicted_positions.csv"

# Загружаем данные
task_data = pd.read_csv(
    input_path,
    names=["id", "text_no_spaces"],
    header=0,
    usecols=[0, 1],
)

# Разбиваем строки
task_data["split_text"] = task_data["text_no_spaces"].apply(
    lambda t: " ".join(split_text(t)) if split_text(t) else t
)

# Считаем позиции пробелов по исходной строке
def compute_positions(row):
    original = row["text_no_spaces"]
    tokens = row["split_text"].split(" ")
    return get_space_positions(original, tokens)

result = pd.DataFrame({
    "id": task_data["id"],
    "predicted_positions": task_data.apply(compute_positions, axis=1)
})

# Сохраняем результат
os.makedirs(os.path.dirname(output_path), exist_ok=True)
result.to_csv(output_path, index=False)

print(f"Готово! Результат сохранён в: {output_path}")