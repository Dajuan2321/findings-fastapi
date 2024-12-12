from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

# 使用mysqlclient
# SQLALCHEMY_DATABASE_URL = "mysql://fastapi_user:xKdicHla49UP5kqm@mysql.sqlpub.com:3306/my_fastapi"

# 或者使用PyMySQL
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://fastapi_user:xKdicHla49UP5kqm@db4free.net:3306/my_fastapi"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:EbxmFAsLIviIIRwzTEdzQLPIEGTAxdMD@autorack.proxy.rlwy.net:23149/railway"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

