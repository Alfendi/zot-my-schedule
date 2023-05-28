import pymysql
import sqlalchemy
import config

from flask import jsonify
from google.cloud.sql.connector import Connector, IPTypes


def getconn() -> pymysql.connections.Connection:
    with Connector() as connector:
        conn = connector.connect(
            config.DB_CONNECTION_NAME,
            "pymysql",
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            db=config.DB_NAME,
            ip_type=IPTypes.PUBLIC,
            enable_iam_auth=False,
        )
    return conn


pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)


def get_cached():
    with pool.connect() as db_conn:
        test = []
        result = db_conn.execute(sqlalchemy.text("SELECT * FROM cachedcourses")).fetchall()
        # for row in result:
        #     print(row)
        for row in result:
            test.append(row)
        return test


def insert_cached(professor_first, professor_last, department, course, quality, difficulty, summary):
    insert_stmt = sqlalchemy.text(
        "INSERT INTO cachedcourses (professor_first, professor_last, department, course, quality, difficulty, "
        "summary) "
        "VALUES (:professor_first, :professor_last, :department, :course, :quality, :difficulty, :summary)",
    )
    with pool.connect() as db_conn:
        db_conn.execute(insert_stmt, parameters={"professor_first": professor_first, "professor_last": professor_last, "department": department, "course": course, "quality": quality, "difficulty": difficulty, "summary": summary})
        db_conn.commit()