from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库配置
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/project_manager"

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明模型基类
Base = declarative_base()
