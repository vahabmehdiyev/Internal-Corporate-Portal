from flask_restx import Resource, Namespace
from flask import send_file, request
import os
from api.graphs_reports.graphs_reports_test import get_graph_for_excel_export, get_table_for_excel_export, build_combined_excel_file_all_lines

graph_reports_ns = Namespace('graph_reports')

@graph_reports_ns.route('/download/<source>/<date>/<type>/<line>/')
class DownloadExcel(Resource):
    def get(self, source, date, type, line):
        try:
            data = {
                "source": source,
                "date": date,
                "line": int(line),
                "type": type
            }

            if type == "table":
                file_path = get_table_for_excel_export(data)
            elif type == "graph":
                file_path = get_graph_for_excel_export(data)
            else:
                return {"error": f"Неизвестный тип: {type}"}, 400

            # Верни файл для загрузки.
            return send_file(
                file_path,
                as_attachment=True,
                download_name=os.path.basename(file_path),
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        except Exception as e:
            return {"error": str(e)}, 500


@graph_reports_ns.route('/download/<source>/<date>/')
class DownloadAllExcel(Resource):
    def get(self, source, date):
        try:
            file_path = build_combined_excel_file_all_lines(source=source, date=date)

            return send_file(
                file_path,
                as_attachment=True,
                download_name=os.path.basename(file_path),
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        except Exception as e:
            return {"error": str(e)}, 500

