import os
from werkzeug.utils import secure_filename
from flask import request, send_from_directory
from api.docs.docs_dao import DocsDAO
from config.utils import get_client_ip


class DocsService:
    def __init__(self, session):
        self.docs_dao = DocsDAO(session)

    def get_docs(self):
        """Выдача всех документов"""

        args = request.args
        ordering = args.get('ordering')

        docs = self.docs_dao.get_docs(ordering)

        response = [
            {
                "id": doc.id,
                "name": doc.name,
                "author": f'{doc.author.first_name} {doc.author.first_name} {doc.author.patronymic}',
                "creation_date": doc.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
                "description": doc.description,
            }
            for doc in docs
        ]

        return response

    def search(self):
        """Задача № 11837. Выдача документов по поисковому запросу"""

        args = request.args
        search_query = args.get('search')

        docs = self.docs_dao.search(search_query)

        response = [
            {
                "id": doc.id,
                "name": doc.name,
                "author": f'{doc.author.first_name} {doc.author.first_name} {doc.author.patronymic}',
                "creation_date": doc.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
                "description": doc.description,
            }
            for doc in docs
        ]

        return response

    def upload_file(self):
        """Задача № 11837. По ИП находим пользователя, закидываем метаданные файла в базу с привязкой к пользователю"""

        ip_address = get_client_ip()
        user = self.docs_dao.get_ip(ip_address)

        if 'file' not in request.files:
            return "Файл не был загружен"

        file = request.files['file']

        if file.filename == '':
            return "Файл не выбран"
        upload_folder = os.path.join(os.getcwd(), 'files', 'docs')

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filename = secure_filename(file.filename)  # Безопасное имя файла

        self.docs_dao.upload_file(file.filename, user.user_id, upload_folder)
        file.save(os.path.join(upload_folder, filename))

        return f"Файл {filename} успешно загружен!"

    def download_file(self, doc_id):
        """Задача № 11837. Находим файл по айдишнику и скачиваем"""

        file = self.docs_dao.get_file(doc_id)

        if not file:
            return "Файл не найден"

        return send_from_directory(file.path, file.name)
