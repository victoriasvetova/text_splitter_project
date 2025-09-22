import pymorphy3

morph = pymorphy3.MorphAnalyzer()

def calc_score(z):
    """
    Считает "правдоподобность" слова на основе морфологических разборов pymorphy3.

    Параметры:
        z (list[Parse]): список разборов слова от pymorphy3.

    Возвращает:
        float: суммарный скор по валидным разбором.
    """
    score = 0
    for m in z:
        if 'UNKN' not in m.tag and \
           'FakeDictionary' not in str(m.methods_stack) and \
           'UnknownPrefixAnalyzer' not in str(m.methods_stack):
            score += m.score
    return round(score, 2)

def split_text(text, start=0):
    """
    Рекурсивно разбивает строку без пробелов на токены (слова).

    Алгоритм:
    - перебираем все возможные окончания слова (фрагменты текста)
    - считаем их скор через calc_score
    - сортируем кандидатов по убыванию
    - выбираем наилучшее разбиение

    Параметры:
        text (str): строка без пробелов
        start (int): текущая позиция (для рекурсии)

    Возвращает:
        list[str] | None: список токенов или None, если сегментация невозможна
    """
    if start >= len(text):
        return []

    candidates = []
    for end in range(start + 1, len(text) + 1):
        fragment = text[start:end]
        parses = morph.parse(fragment)
        score = calc_score(parses)
        if score > 0:
            candidates.append((score, end, fragment))

    candidates.sort(reverse=True)

    for score, end, fragment in candidates:
        rest = split_text(text, end)
        if rest is not None:
            return [fragment] + rest

    return None