import psycopg2
import config

def connect_to_db():
    conn = psycopg2.connect(**config.login_parameters)
    return conn