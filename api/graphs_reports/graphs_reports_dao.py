from concurrent.futures import ThreadPoolExecutor
from api.graphs_reports.graphs_reports_utils import get_db_connection

"""
Функция get_asse_count_for_line относится к get_asse_total_count_by_date.
(Она предназначена для получения общей информации по части asse: возвращает количество записей asse по всем линиям.)
"""
def get_asse_count_for_line(line, date):
    try:
        conn = get_db_connection(line)
        cur = conn.cursor()

        query = f"""
            SELECT COUNT(ksiv.rec_id) AS total
            FROM ksiv
            WHERE
                ksiv.timecheck BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
                AND ksiv.error = 0
                AND ksiv.product <> 0
                AND ksiv.server IS NULL
                AND ksiv.product IN (SELECT num FROM product)
        """

        cur.execute(query)
        result = cur.fetchone()
        conn.close()
        return result[0] if result and result[0] else 0

    except Exception as e:
        print("Произошла ошибка при выполнении запроса")
        # print(f"Line {line} üçün paralel sorğuda xəta: {e}")
        return 0


def get_asse_total_count_by_date(data):
    date = data.get("date")
    total_count = 0

    #Для LINE 1-4 мы отправляем один запрос, потому что они находятся на одном сервере.
    try:
        conn = get_db_connection(1)
        cur = conn.cursor()

        query = f"""
            SELECT COUNT(ksiv.rec_id) AS total
            FROM ksiv
            WHERE
                ksiv.timecheck BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
                AND ksiv.error = 0
                AND ksiv.product <> 0
                AND ksiv.server IS NULL
                AND ksiv.product IN (SELECT num FROM product)
        """

        cur.execute(query)
        result = cur.fetchone()
        if result and result[0]:
            total_count += result[0]

        conn.close()

    except Exception as e:
        print("Произошла ошибка при выполнении запроса", e)
        # print("Line 1–4 server üçün sorğuda xəta:", e)

    # Для LINE 5-7 запросы выполняются параллельно.
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(get_asse_count_for_line, line, date) for line in (5, 6, 7)]
        for future in futures:
            total_count += future.result()

    return total_count

"""
Функция get_asse_data_by_line_and_date предназначена для получения данных по asse, относящихся к выбранной линии.
"""
def get_asse_data_by_line_and_date(data):
    line = data.get("line")
    date = data.get("date")

    conn = get_db_connection(line)
    cur = conn.cursor()

    if line in (1, 2, 3, 4):
        """
        Для LINE 1-4 фильтр используется в том виде, как есть. Так как они находятся на одном сервере, нельзя получать \
         данные обобщённо — фильтруем по значению LINE. Под LINE имеется в виду конвейер.
        """
        query = f"""
            SELECT
                product.line,
                product."NAMES",
                EXTRACT(HOUR FROM ksiv.timecheck) AS hr,
                COUNT(ksiv.rec_id) AS total
            FROM ksiv
            JOIN product ON ksiv.product = product.num
            WHERE
                ksiv.timecheck BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
                AND product.line = {line}
                AND ksiv.error = 0
                AND ksiv.product <> 0
                AND ksiv.server IS NULL
            GROUP BY
                product.line,
                product."NAMES",
                EXTRACT(HOUR FROM ksiv.timecheck)
            ORDER BY
                product.line,
                hr
        """
    elif line in (5, 6, 7):
        """
        Для запросов по LINE 5-7 фильтр по линии не применяется, так как данные на этом сервере берутся обобщённо.\
         Значение LINE используется в том виде, как есть.
        """
        query = f"""
            SELECT
                {line} AS line,
                product."NAMES",
                EXTRACT(HOUR FROM ksiv.timecheck) AS hr,
                COUNT(ksiv.rec_id) AS total
            FROM ksiv
            JOIN product ON ksiv.product = product.num
            WHERE
                ksiv.timecheck BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
                AND ksiv.error = 0
                AND ksiv.product <> 0
                AND ksiv.server IS NULL
            GROUP BY
                product."NAMES",
                EXTRACT(HOUR FROM ksiv.timecheck)
            ORDER BY
                hr
        """
    else:
        conn.close()
        return []

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "line": row[0],
            "name": row[1],
            "hour": row[2],
            "total": row[3]
        }
        for row in rows
    ]

"""
Функция get_hours_count_for_line относится к get_hours_total_count_by_date.
(Она предназначена для получения общей информации по части hours: возвращает количество записей hours по всем линиям.)
"""
def get_hours_count_for_line(line, date):
    try:
        conn = get_db_connection(line)
        cur = conn.cursor()

        query = f"""
            SELECT COUNT(pack.PACK_id) AS total
            FROM pack
            JOIN product ON pack.product = product.num
            JOIN pack_kit_list ON pack.packkit = pack_kit_list.packkit
            WHERE
                pack.packtime BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
                AND pack.server IS NULL
        """

        # Yalnız line 1–4 üçün product.line filtresi yazılır
        if line in (1, 2, 3, 4):
            query += f"\n    AND product.line = {line}"

        cur.execute(query)
        result = cur.fetchone()
        conn.close()
        return result[0] if result and result[0] else 0

    except Exception as e:
        print("Произошла ошибка при выполнении запроса")
        # print(f"Line {line} üçün pack sorğuda xəta:", e)
        return 0


def get_hours_total_count_by_date(data):
    date = data.get("date")
    total_count = 0

    #Для LINE 1-4 мы отправляем один запрос, потому что они находятся на одном сервере.
    try:
        conn = get_db_connection(1)
        cur = conn.cursor()

        query = f"""
            SELECT COUNT(pack.PACK_id) AS total
            FROM pack
            JOIN product ON pack.product = product.num
            JOIN pack_kit_list ON pack.packkit = pack_kit_list.packkit
            WHERE
                pack.packtime BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
                AND pack.server IS NULL
                AND product.line IN (1, 2, 3, 4)
        """

        cur.execute(query)
        result = cur.fetchone()
        if result and result[0]:
            total_count += result[0]

        conn.close()

    except Exception as e:
        print("Произошла ошибка при выполнении запроса", e)
        # print("Line 1–4 server üçün pack sorğuda xəta:", e)

    # Для LINE 5-7 запросы выполняются параллельно.
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(get_hours_count_for_line, line, date) for line in (5, 6, 7)]
        for future in futures:
            total_count += future.result()

    return total_count

"""
Функция get_hours_data_by_line_and_date предназначена для получения данных по hours, относящихся к выбранной линии.
"""
def get_hours_data_by_line_and_date(data):
    line = data.get("line")
    date = data.get("date")

    conn = get_db_connection(line)
    cur = conn.cursor()

    if line in (1, 2, 3, 4):
        """
        Для LINE 1-4 фильтр используется в том виде, как есть. Так как они находятся на одном сервере, нельзя получать \
         данные обобщённо — фильтруем по значению LINE. Под LINE имеется в виду конвейер.
        """
        query = f"""
            SELECT
                product.line,
                pack.packkit,
                pack_kit_list."COMMENTS",
                EXTRACT(HOUR FROM pack.packtime) AS hr,
                COUNT(pack.PACK_id) AS total
            FROM pack
            JOIN product ON pack.product = product.num
            JOIN pack_kit_list ON pack.packkit = pack_kit_list.packkit
            WHERE
                pack.packtime BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
                AND product.line = {line}
                AND pack.server IS NULL
            GROUP BY
                product.line,
                pack.packkit,
                pack_kit_list."COMMENTS",
                EXTRACT(HOUR FROM pack.packtime)
            ORDER BY
                product.line,
                hr
        """
    elif line in (5, 6, 7):
        """
        Для запросов по LINE 5-7 фильтр по линии не применяется, так как данные на этом сервере берутся обобщённо.\
         Значение LINE используется в том виде, как есть.
        """
        query = f"""
            SELECT
                {line} AS line,
                pack.packkit,
                pack_kit_list."COMMENTS",
                EXTRACT(HOUR FROM pack.packtime) AS hr,
                COUNT(pack.PACK_id) AS total
            FROM pack
            JOIN product ON pack.product = product.num
            JOIN pack_kit_list ON pack.packkit = pack_kit_list.packkit
            WHERE
                pack.packtime BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
                AND pack.server IS NULL
            GROUP BY
                pack.packkit,
                pack_kit_list."COMMENTS",
                EXTRACT(HOUR FROM pack.packtime)
            ORDER BY
                hr
        """
    else:
        conn.close()
        return []

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "line": row[0],
            "packkit": row[1],
            "comments": row[2],
            "hour": row[3],
            "total": row[4],
            "date": date
        }
        for row in rows
    ]

"""
Функция get_psi_count_for_line относится к get_psi_total_count_by_date.
(Она предназначена для получения общей информации по части psi: возвращает количество записей psi по всем линиям.)
"""
def get_psi_count_for_line(line, date):
    try:
        conn = get_db_connection(line)
        cur = conn.cursor()

        query = f"""
            SELECT COUNT(psi.rec_id) AS total
            FROM psi
            JOIN product ON psi.product = product.num
            WHERE
                psi.timestart BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
                AND psi.server IS NULL
                AND psi.error = 0
                AND psi.param_code = 0
                AND psi.link_code = 0
        """

        # Line 1–4 üçün əlavə filter lazımdır
        if line in (1, 2, 3, 4):
            query += f"\n    AND product.line = {line}"

        cur.execute(query)
        result = cur.fetchone()
        conn.close()

        return result[0] if result and result[0] else 0

    except Exception as e:
        print("Произошла ошибка при выполнении запроса")
        # print(f"Line {line} üçün psi sorğuda xəta:", e)
        return 0

def get_psi_total_count_by_date(data):
    date = data.get("date")
    total_count = 0

    #Для LINE 1-4 мы отправляем один запрос, потому что они находятся на одном сервере.
    try:
        conn = get_db_connection(1)
        cur = conn.cursor()

        query = f"""
            SELECT COUNT(psi.rec_id) AS total
            FROM psi
            JOIN product ON psi.product = product.num
            WHERE
                psi.timestart BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
                AND psi.server IS NULL
                AND psi.error = 0
                AND psi.param_code = 0
                AND psi.link_code = 0
                AND product.line IN (1, 2, 3, 4)
        """

        cur.execute(query)
        result = cur.fetchone()
        if result and result[0]:
            total_count += result[0]

        conn.close()

    except Exception as e:
        print("Произошла ошибка при выполнении запроса", e)
        # print("Line 1–4 server üçün psi sorğuda xəta:", e)

    # Для LINE 5-7 запросы выполняются параллельно.
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(get_psi_count_for_line, line, date) for line in (5, 6, 7)]
        for future in futures:
            total_count += future.result()

    return total_count

"""
Функция get_psi_data_by_line_and_date предназначена для получения данных по psi, относящихся к выбранной линии.
"""
def get_psi_data_by_line_and_date(data):
    line = data.get("line")
    date = data.get("date")

    conn = get_db_connection(line)
    cur = conn.cursor()

    if line in (1, 2, 3, 4):
        """
        Для LINE 1-4 фильтр используется в том виде, как есть. Так как они находятся на одном сервере, нельзя получать \
         данные обобщённо — фильтруем по значению LINE. Под LINE имеется в виду конвейер.
        """
        query = f"""
            SELECT
                product.line,
                product."NAMES",
                EXTRACT(HOUR FROM psi.timestart) AS hr,
                psi.product,
                COUNT(psi.rec_id) AS total
            FROM psi
            JOIN product ON psi.product = product.num
            WHERE
                psi.timestart BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
                AND product.line = {line}
                AND psi.server IS NULL
                AND psi.error = 0
                AND psi.param_code = 0
                AND psi.link_code = 0
            GROUP BY
                product.line,
                product."NAMES",
                psi.product,
                EXTRACT(HOUR FROM psi.timestart)
            ORDER BY
                product.line,
                hr
        """
    elif line in (5, 6, 7):
        """
        Для запросов по LINE 5-7 фильтр по линии не применяется, так как данные на этом сервере берутся обобщённо.\
         Значение LINE используется в том виде, как есть.
        """
        query = f"""
            SELECT
                {line} AS line,
                product."NAMES",
                EXTRACT(HOUR FROM psi.timestart) AS hr,
                psi.product,
                COUNT(psi.rec_id) AS total
            FROM psi
            JOIN product ON psi.product = product.num
            WHERE
                psi.timestart BETWEEN '{date} 00:00:00' AND '{date} 23:59:59'
                AND psi.server IS NULL
                AND psi.error = 0
                AND psi.param_code = 0
                AND psi.link_code = 0
            GROUP BY
                product."NAMES",
                psi.product,
                EXTRACT(HOUR FROM psi.timestart)
            ORDER BY
                hr
        """
    else:
        conn.close()
        return []

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "line": row[0],
            "comments": row[1],
            "hour": row[2],
            "product": row[3],
            "total": row[4],
            "date": date
        }
        for row in rows
    ]
