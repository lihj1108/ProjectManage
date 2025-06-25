SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/project_manage"

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)