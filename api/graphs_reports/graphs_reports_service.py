from api.graphs_reports.graphs_reports_dao import get_asse_data_by_line_and_date, get_asse_total_count_by_date, \
    get_hours_data_by_line_and_date, get_hours_total_count_by_date, \
    get_psi_total_count_by_date, get_psi_data_by_line_and_date

from collections import defaultdict
from transliterate import translit
from concurrent.futures import ThreadPoolExecutor
from api.graphs_reports.graphs_reports_utils import COLOR_PALETTE

# Преобразует строку из кириллицы в латиницу и форматирует в стиль slug (нижний регистр, подчёркивания)
def slugify(name: str) -> str:
    latin = translit(name, 'ru', reversed=True)
    return latin.lower().replace("-", "_").replace(" ", "_")

def get_ksiv_data(data):
    type = data.get("type")
    line = int(data.get("line"))
    date = data.get("date")

    ksiv_rows = get_asse_data_by_line_and_date(data)
    count_all = get_asse_total_count_by_date(data)

    product_names = []
    for row in ksiv_rows:
        name = row.get("name")
        if name not in product_names:
            product_names.append(name)

    series = {}
    used_colors = []

    for i, name in enumerate(product_names):
        slug = slugify(name)
        color = COLOR_PALETTE[i % len(COLOR_PALETTE)]
        used_colors.append(color)
        series[slug] = {
            "name": name,
            "strokeColor": color,
            "type": "line"
        }

    series["count"] = {
        "name": "Итого",
        "strokeColor": "#CBD5E1",
        "type": "bar"
    }

    hour_map = defaultdict(lambda: {slugify(name): 0 for name in product_names})

    for row in ksiv_rows:
        hour = row["hour"]
        name = row["name"]
        total = row["total"]
        slug = slugify(name)
        hour_map[hour][slug] += total

    graph_data = []
    for hour in sorted(hour_map.keys()):
        item = hour_map[hour].copy()
        item["count"] = sum(item.values())
        item["label"] = f"{hour} hour"
        graph_data.append(item)

    hours = sorted(set(row["hour"] for row in ksiv_rows))
    headers = ["Наименование изделия"] + [f"{h} час" for h in hours] + ["Итого"]

    table_data = {}
    for row in ksiv_rows:
        name = row["name"]
        hour = row["hour"]
        total = row["total"]

        if name not in table_data:
            table_data[name] = {}
        table_data[name][hour] = total

    rows = []
    for name, hour_data in table_data.items():
        row = [name]
        row_total = 0
        for h in hours:
            val = hour_data.get(h, 0)
            row.append(val)
            row_total += val
        row.append(row_total)
        rows.append(row)

    footer = ["Итого по часам"]
    for h in hours:
        col_sum = sum(hour_data.get(h, 0) for hour_data in table_data.values())
        footer.append(col_sum)
    footer.append(sum(footer[1:]))
    rows.append(footer)

    cards = []

    if type == "graph":
        cards.append({
            "type": "graph",
            "line": line,
            "graph": {
                "series": series,
                "list": graph_data
            }
        })
    elif type == "table":
        cards.append({
            "type": "table",
            "line": line,
            "table": {
                "headers": headers,
                "rows": rows
            }
        })

    return {
        "date": date,
        "count_all": count_all,
        "cards": cards
    }

def get_pack_data(data):
    type = data.get("type")
    line = data.get("line")
    date = data.get("date")

    pack_rows = get_hours_data_by_line_and_date(data)
    count_all = get_hours_total_count_by_date(data)

    product_names = []
    for row in pack_rows:
        name = row.get("comments")
        if name not in product_names:
            product_names.append(name)

    series = {}
    used_colors = []

    for i, name in enumerate(product_names):
        slug = slugify(name)
        color = COLOR_PALETTE[i % len(COLOR_PALETTE)]
        used_colors.append(color)
        series[slug] = {
            "name": name,
            "strokeColor": color,
            "type": "line"
        }

    series["count"] = {
        "name": "Итого",
        "strokeColor": "#CBD5E1",
        "type": "bar"
    }

    hour_map = defaultdict(lambda: {slugify(name): 0 for name in product_names})

    for row in pack_rows:
        hour = row["hour"]
        name = row["comments"]
        total = row["total"]
        slug = slugify(name)
        hour_map[hour][slug] += total

    graph_data = []
    for hour in sorted(hour_map.keys()):
        item = hour_map[hour].copy()
        item["count"] = sum(item.values())
        item["label"] = f"{hour} hour"
        graph_data.append(item)

    hours = sorted(set(row["hour"] for row in pack_rows))
    headers = ["Наименование изделия"] + [f"{h} час" for h in hours] + ["Итого"]

    table_data = {}
    for row in pack_rows:
        name = row["comments"]
        hour = row["hour"]
        total = row["total"]

        if name not in table_data:
            table_data[name] = {}
        table_data[name][hour] = total

    rows = []
    for name, hour_data in table_data.items():
        row = [name]
        row_total = 0
        for h in hours:
            val = hour_data.get(h, 0)
            row.append(val)
            row_total += val
        row.append(row_total)
        rows.append(row)

    footer = ["Итого по часам"]
    for h in hours:
        col_sum = sum(hour_data.get(h, 0) for hour_data in table_data.values())
        footer.append(col_sum)
    footer.append(sum(footer[1:]))
    rows.append(footer)

    cards = []

    if type == "graph":
        cards.append({
            "type": "graph",
            "line": line,
            "graph": {
                "series": series,
                "list": graph_data
            }
        })
    elif type == "table":
        cards.append({
            "type": "table",
            "line": line,
            "table": {
                "headers": headers,
                "rows": rows
            }
        })

    return {
        "date": date,
        "count_all": count_all,
        "cards": cards
    }

def get_psi_data(data):
    type = data.get("type")
    line = data.get("line")
    date = data.get("date")

    psi_rows = get_psi_data_by_line_and_date(data)
    count_all = get_psi_total_count_by_date(data)

    product_names = []
    for row in psi_rows:
        name = row.get("comments")
        if name not in product_names:
            product_names.append(name)

    series = {}
    used_colors = []

    for i, name in enumerate(product_names):
        slug = slugify(name)
        color = COLOR_PALETTE[i % len(COLOR_PALETTE)]
        used_colors.append(color)
        series[slug] = {
            "name": name,
            "strokeColor": color,
            "type": "line"
        }

    # "count" seriyası (sabit qalır)
    series["count"] = {
        "name": "Итого",
        "strokeColor": "#CBD5E1",
        "type": "bar"
    }

    hour_map = defaultdict(lambda: {slugify(name): 0 for name in product_names})

    for row in psi_rows:
        hour = row["hour"]
        name = row["comments"]
        total = row["total"]
        slug = slugify(name)
        hour_map[hour][slug] += total

    graph_data = []
    for hour in sorted(hour_map.keys()):
        item = hour_map[hour].copy()
        item["count"] = sum(item.values())
        item["label"] = f"{hour} hour"
        graph_data.append(item)

    hours = sorted(set(row["hour"] for row in psi_rows))
    headers = ["Наименование изделия"] + [f"{h} час" for h in hours] + ["Итого"]

    table_data = {}
    for row in psi_rows:
        name = row["comments"]
        hour = row["hour"]
        total = row["total"]

        if name not in table_data:
            table_data[name] = {}
        table_data[name][hour] = total

    rows = []
    for name, hour_data in table_data.items():
        row = [name]
        row_total = 0
        for h in hours:
            val = hour_data.get(h, 0)
            row.append(val)
            row_total += val
        row.append(row_total)
        rows.append(row)

    footer = ["Итого по часам"]
    for h in hours:
        col_sum = sum(hour_data.get(h, 0) for hour_data in table_data.values())
        footer.append(col_sum)
    footer.append(sum(footer[1:]))
    rows.append(footer)

    cards = []

    if type == "graph":
        cards.append({
            "type": "graph",
            "line": line,
            "graph": {
                "series": series,
                "list": graph_data
            }
        })
    elif type == "table":
        cards.append({
            "type": "table",
            "line": line,
            "table": {
                "headers": headers,
                "rows": rows
            }
        })

    return {
        "date": date,
        "count_all": count_all,
        "cards": cards
    }


def process_section(section: str, section_data: dict):
    if not isinstance(section_data, dict):
        return section, {}

    date = section_data.get("date")
    if not date:
        return section, {}

    cards = section_data.get("cards", [])
    result_cards = []

    # count_all
    if section == "asse":
        count = get_asse_total_count_by_date({"date": date})
    elif section == "psi":
        count = get_psi_total_count_by_date({"date": date})
    elif section == "hours":
        count = get_hours_total_count_by_date({"date": date})
    else:
        count = 0

    for card in cards:
        type_ = card.get("type")
        line = card.get("line")

        if not (type_ and line is not None):
            continue

        input_data = {
            "type": type_,
            "line": line,
            "date": date
        }

        if section == "asse":
            result = get_ksiv_data(input_data)
        elif section == "psi":
            result = get_psi_data(input_data)
        elif section == "hours":
            result = get_pack_data(input_data)
        else:
            result = {}

        for item in result.get("cards", []):
            if not isinstance(item, dict):
                continue

            if item.get("type") != type_ or item.get("line") != line:
                continue

            data = item.get(type_)
            if not data:
                continue

            card_result = {
                "type": type_,
                "line": line,
                type_: data
            }
            result_cards.append(card_result)

    return section, {
        "count_all": count,
        "cards": result_cards
    }


def get_dashboard_data(payload: dict):
    try:
        if not isinstance(payload, dict):
            raise ValueError("Payload должен быть в формате словаря.")

        sections = ["asse", "psi", "hours"]
        response = {}

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(process_section, section, payload.get(section)): section
                for section in sections
            }

            for future in futures:
                section, section_result = future.result()
                response[section] = section_result

        return {
            "data": {
                "code": 200,
                "message": "Ответы успешно возвращены"
            },
            "response": response
        }

    except Exception as e:
        return {
            "data": {
                "code": 500,
                "message": f"Произошла ошибка: {str(e)}"
            },
            "response": {}
        }