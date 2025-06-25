from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DECIMAL, JSON, TIMESTAMP
from database import Base
from sqlalchemy.sql import func


# 定义用户模型
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    real_name = Column(String, nullable=True)
    phone_num = Column(String)
    is_leader = Column(Boolean, default=False)


# 定义项目模型
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    project_type = Column(String, nullable=False)
    project_stage = Column(String, nullable=False)
    start_date = Column(Date, nullable=True)  # 使用字符串存储日期
    end_date = Column(Date, nullable=True)  # 使用字符串存储日期
    manager_name = Column(String, nullable=True)
    supervisor_name = Column(String, nullable=True)


# 定义子项目模型
class SubProject(Base):
    __tablename__ = "sub_projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_name = Column(String(100), nullable=False)
    sub_project_name = Column(String(100), nullable=False)
    building_name = Column(String(100), nullable=False)
    floor_area = Column(DECIMAL(10, 2), nullable=True)
    architecture_leader_name = Column(String(100), nullable=True)
    structure_leader_name = Column(String(100), nullable=True)
    plumbing_leader_name = Column(String(100), nullable=True)
    electrical_leader_name = Column(String(100), nullable=True)
    architecture_designers = Column(JSON, nullable=True)
    structure_designers = Column(JSON, nullable=True)
    plumbing_designers = Column(JSON, nullable=True)
    electrical_designers = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

# 定义周报模型
class WeekReport(Base):
    __tablename__ = "week_report"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    week = Column(Integer, nullable=False)  
    time = Column(String, nullable=False)  # 使用字符串存储日期
    work_schedule = Column(String, nullable=False)