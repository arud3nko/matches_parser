from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


class DatabaseHandler:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def add_record(self, record):
        """
        Добавляет новую запись в базу данных.
        :param record: Экземпляр класса, соответствующего таблице.
        :return: None
        """
        session = self.Session()
        try:
            session.add(record)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_records_by_user_id(self, model_class):
        """
        Получает записи из базы данных
        :param model_class: Класс модели, соответствующий таблице.
        :return: Список экземпляров класса модели.
        """
        session = self.Session()
        try:
            records = session.query(model_class).all()
            return records
        except SQLAlchemyError as e:
            raise e
        finally:
            session.close()
