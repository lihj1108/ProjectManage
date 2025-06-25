from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# 用户参数格式化类
class UserBase(BaseModel):
    username: str
    password: Optional[str] = ""
    real_name: Optional[str] = ""
    is_leader: Optional[bool] = False
    phone_num: Optional[str] = ""
    origin_password: Optional[str] = ""


# 项目参数格式化类
class ProjectBase(BaseModel):
    name: str
    project_type: str
    project_stage: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    manager_name: Optional[str] = None
    supervisor_name: Optional[str] = None

# 子项目参数格式化类
class SubProjectBase(BaseModel):
    project_name: str
    sub_project_name: str
    building_name: str
    floor_area: Optional[float] = None
    architecture_leader_name: Optional[str] = None
    structure_leader_name: Optional[str] = None
    plumbing_leader_name: Optional[str] = None
    electrical_leader_name: Optional[str] = None
    architecture_designers: Optional[List[str]] = None
    structure_designers: Optional[List[str]] = None
    plumbing_designers: Optional[List[str]] = None
    electrical_designers: Optional[List[str]] = None

# 周报参数格式化类
class WeekReportBase(BaseModel):
    project_name: str
    year: int
    month: int
    week: int
    time: str
    work_schedule: str