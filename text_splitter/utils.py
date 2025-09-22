def get_space_positions(original: str, split_tokens: list[str]) -> list[int]:
    """
    Находит позиции пробелов относительно исходной строки без пробелов.

    Параметры:
        original (str): исходная строка без пробелов
        split_tokens (list[str]): список слов после сегментации

    Возвращает:
        list[int]: список индексов символов, после которых нужно поставить пробелы.
                   Индексация с 0.
    """
    positions = []
    cursor = 0
    for token in split_tokens[:-1]:  # последний токен не имеет пробела после
        cursor += len(token)
        positions.append(cursor)
    return positions
