from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import User, Project, SubProject, WeekReport
from param_format import UserBase, ProjectBase, SubProjectBase, WeekReportBase

import logging

formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)  # 日志写入格式：时间-级别-日志内容
handler = logging.FileHandler(filename="./log.log")  # 实例化handler，设置日志文件存放地址
handler.setFormatter(formatter)  # 给handler设置日志格式
handler.setLevel(logging.INFO)  # 给handler设置日志级别，这决定了handler写入文件的最低日志级别
logger = logging.getLogger("main_log")  # 实例化名为main_log的logger
logger.addHandler(handler)  # 给logger添加handler
logger.setLevel(logging.INFO)  # 给logger设置日志级别，这决定了logger发送给handler的最低日志级别


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 替换为你的前端地址
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法，包括 OPTIONS
    allow_headers=["*"],  # 允许所有头
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""人员管理接口"""


# 查看所有人员信息
@app.get("/users/", response_model=List[UserBase])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# 添加人员
@app.post("/users/", response_model=UserBase)
def create_user(user: UserBase, db: Session = Depends(get_db), current_user: str = ""):
    existing = db.query(User).filter_by(username=user.username).first()
    if existing:
        return JSONResponse({"code": 400, "message": "用户名已存在，请使用其他用户名！"})
    db_user = User(
        username=user.username,
        password=user.password,
        real_name=user.real_name,
        is_leader=user.is_leader,
        phone_num=user.phone_num,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"当前用户：{current_user}，添加人员成功，用户名：{user.username}, 姓名：{user.real_name}")
    return JSONResponse({"code": 200, "message": "添加人员成功"})


# 修改人员密码
@app.put("/users/", response_model=UserBase)
def update_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(username=user.username).first()
    if not db_user:
        return JSONResponse({"code": 400, "message": "用户未找到"})
    if user.origin_password and (db_user.password != user.origin_password):
        return JSONResponse({"code": 400, "message": "原密码错误"})
    if user.phone_num and (db_user.phone_num != user.phone_num):
        return JSONResponse({"code": 400, "message": "手机号码错误"})
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return JSONResponse({"code": 200, "message": "修改密码成功"})


# 删除人员
@app.delete("/users/")
def delete_user(user: UserBase, db: Session = Depends(get_db), current_user: str = ""):
    db_user = db.query(User).filter_by(username=user.username).first()
    if not db_user:
        logger.info("用户未找到")
        return JSONResponse({"code": 400, "message": "用户未找到"})
    if db_user.username == "admin":
        logger.info("admin用户不能删除")
        return JSONResponse({"code": 400, "message": "admin用户不能删除"})
    if db_user.real_name != user.real_name:
        logger.info("用户名和姓名不匹配")
        return JSONResponse({"code": 400, "message": "用户名和姓名不匹配"})
    db.delete(db_user)
    db.commit()
    logger.info(f"当前用户：{current_user}, 删除人员成功, 用户名：{user.username}, 姓名：{user.real_name}")
    return JSONResponse({"code": 200, "message": "用户删除成功"})


# 人员登录
@app.post("/login/")
def login(user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(username=user.username).first()

    if not db_user:
        logger.info("用户名错误")
        return JSONResponse({"code": 400, "message": "用户名或密码错误"})
    print("-----db_user: ", db_user.password, user.password)
    if db_user.password != user.password:
        logger.info("密码错误")
        return JSONResponse({"code": 400, "message": "用户名或密码错误"})
    logger.info("登录成功")
    return JSONResponse({"code": 200, "message": "登录成功"})


"""项目管理接口"""


# 新建项目
@app.post("/projects/", response_model=ProjectBase)
def create_project(project: ProjectBase, db: Session = Depends(get_db), current_user: str = ""):
    existing = db.query(Project).filter_by(name=project.name).first()
    if existing:
        return JSONResponse({"code": 400, "message": "项目名已存在，请使用其他项目名称！"})
    db_project = Project(
        name=project.name,
        project_type=project.project_type,
        project_stage=project.project_stage,
        start_date=project.start_date,
        end_date=project.end_date,
        manager_name=project.manager_name,
        supervisor_name=project.supervisor_name,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    logger.info(f"当前用户：{current_user}，新建项目成功，项目名称：{project.name}")
    return JSONResponse({"code": 200, "message": "新建项目成功"})


# 查看所有项目
@app.get("/projects/", response_model=List[ProjectBase])
def get_all_projects(db: Session = Depends(get_db), current_user: str = ""):
    # projects = db.query(Project).filter_by(manager_name=current_user).all()
    projects = db.query(Project).all()
    return projects


# 查看单个项目
@app.get("/projects/{project_name}", response_model=ProjectBase)
def get_project(project_name: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter_by(name=project_name).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目未找到")
    return project


# 编辑项目
@app.put("/projects/{project_name}", response_model=ProjectBase)
def update_project(project_name: str, project: ProjectBase, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter_by(name=project_name).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="项目未找到")
    db_project.name = project.name if project.name else db_project.name
    db_project.project_type = project.project_type if project.project_type else db_project.project_type
    db_project.project_stage = project.project_stage if project.project_stage else db_project.project_stage
    db_project.start_date = project.start_date if project.start_date else db_project.start_date
    db_project.end_date = project.end_date if project.end_date else db_project.end_date
    db_project.manager_name = (
        project.manager_name if project.manager_name is not None else db_project.manager_name
    )
    db_project.supervisor_name = (
        project.supervisor_name if project.supervisor_name is not None else db_project.supervisor_name
    )
    db.commit()
    db.refresh(db_project)
    return db_project


# 删除项目
@app.delete("/projects/{project_name}", response_model=dict)
def delete_project(project_name: str, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter_by(name=project_name).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="项目未找到")
    db.delete(db_project)
    db.commit()
    return {"message": "项目已删除"}


"""子项目管理接口"""


# 添加子项目
@app.post("/sub_projects/", response_model=SubProjectBase)
def create_sub_project(sub_project: SubProjectBase, db: Session = Depends(get_db)):
    existing = db.query(SubProject).filter_by(sub_project_name=sub_project.sub_project_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="子项目名称已存在，请使用其他项目名称！")
    db_sub_project = SubProject(
        project_name=sub_project.project_name,
        sub_project_name=sub_project.sub_project_name,
        building_name=sub_project.building_name,
        floor_area=sub_project.floor_area,
        architecture_leader_name=sub_project.architecture_leader_name,
        structure_leader_name=sub_project.structure_leader_name,
        plumbing_leader_name=sub_project.plumbing_leader_name,
        electrical_leader_name=sub_project.electrical_leader_name,
        architecture_designers=sub_project.architecture_designers,
        structure_designers=sub_project.structure_designers,
        plumbing_designers=sub_project.plumbing_designers,
        electrical_designers=sub_project.electrical_designers,
    )
    db.add(db_sub_project)
    db.commit()
    db.refresh(db_sub_project)
    return db_sub_project


# 查看所有子项目信息
@app.get("/sub_projects/", response_model=List[SubProjectBase])
def get_all_sub_projects(db: Session = Depends(get_db)):
    sub_projects = db.query(SubProject).all()
    return sub_projects


# 查看单个子项目信息
@app.get("/sub_projects/{sub_project_name}", response_model=SubProjectBase)
def get_sub_project(sub_project_name: str, db: Session = Depends(get_db)):
    sub_project = db.query(SubProject).filter_by(sub_project_name=sub_project_name).first()
    if not sub_project:
        raise HTTPException(status_code=404, detail="子项目未找到")
    return sub_project


# 修改子项目信息
@app.put("/sub_projects/{sub_project_name}", response_model=SubProjectBase)
def update_sub_project(sub_project_name: str, sub_project: SubProjectBase, db: Session = Depends(get_db)):
    db_sub_project = db.query(SubProject).filter_by(sub_project_name=sub_project_name).first()
    if not db_sub_project:
        raise HTTPException(status_code=404, detail="子项目未找到")
    db_sub_project.project_name = (
        sub_project.project_name if sub_project.project_name else db_sub_project.project_name
    )
    db_sub_project.sub_project_name = (
        sub_project.sub_project_name if sub_project.sub_project_name else db_sub_project.sub_project_name
    )
    db_sub_project.building_name = (
        sub_project.building_name if sub_project.building_name else db_sub_project.building_name
    )
    db_sub_project.floor_area = (
        sub_project.floor_area if sub_project.floor_area is not None else db_sub_project.floor_area
    )
    db_sub_project.architecture_leader_name = (
        sub_project.architecture_leader_name
        if sub_project.architecture_leader_name
        else db_sub_project.architecture_leader_name
    )
    db_sub_project.structure_leader_name = (
        sub_project.structure_leader_name
        if sub_project.structure_leader_name
        else db_sub_project.structure_leader_name
    )
    db_sub_project.plumbing_leader_name = (
        sub_project.plumbing_leader_name
        if sub_project.plumbing_leader_name
        else db_sub_project.plumbing_leader_name
    )
    db_sub_project.electrical_leader_name = (
        sub_project.electrical_leader_name
        if sub_project.electrical_leader_name
        else db_sub_project.electrical_leader_name
    )
    db_sub_project.architecture_designers = (
        sub_project.architecture_designers
        if sub_project.architecture_designers
        else db_sub_project.architecture_designers
    )
    db_sub_project.structure_designers = (
        sub_project.structure_designers
        if sub_project.structure_designers
        else db_sub_project.structure_designers
    )
    db_sub_project.plumbing_designers = (
        sub_project.plumbing_designers
        if sub_project.plumbing_designers
        else db_sub_project.plumbing_designers
    )
    db_sub_project.electrical_designers = (
        sub_project.electrical_designers
        if sub_project.electrical_designers
        else db_sub_project.electrical_designers
    )
    db.commit()
    db.refresh(db_sub_project)
    return db_sub_project


# 删除子项目
@app.delete("/sub_projects/{sub_project_name}", response_model=dict)
def delete_sub_project(sub_project_name: str, db: Session = Depends(get_db)):
    db_sub_project = db.query(SubProject).filter_by(sub_project_name=sub_project_name).first()
    if not db_sub_project:
        raise HTTPException(status_code=404, detail="子项目未找到")
    db.delete(db_sub_project)
    db.commit()
    return {"message": "子项目已删除"}


"""周报管理接口"""


# 添加周报
@app.post("/week_report/")
def create_weekly_report(week_report: WeekReportBase, db: Session = Depends(get_db), current_user: str = ""):
    db_weekly_report = WeekReport(
        project_name=week_report.project_name,
        year=week_report.year,
        month=week_report.month,
        week=week_report.week,
        time=week_report.time,
        work_schedule=week_report.work_schedule,
    )
    db.add(db_weekly_report)
    db.commit()
    db.refresh(db_weekly_report)
    logger.info(
        f"当前用户：{current_user}, 添加周报, 项目名称：{week_report.project_name}, 年份：{week_report.year}, 月份：{week_report.month}, 周数：{week_report.week}"
    )
    return JSONResponse({"code": 200, "message": "添加周报成功"})


# 根据项目名称查看周报
@app.get("/week_report/{project_name}", response_model=List[WeekReportBase])
def get_weekly_reports_by_project(project_name: str, db: Session = Depends(get_db)):
    weekly_reports = db.query(WeekReport).filter_by(project_name=project_name).all()
    if not weekly_reports:
        return JSONResponse({"code": 400, "message": "未找到相关周报"})
    return weekly_reports


# 删除周报
@app.delete("/week_report/{project_name}", response_model=dict)
def delete_weekly_report(project_name: str, db: Session = Depends(get_db), year: int = 0, month: int = 0, week: int = 0, current_user: str = ""):
    db_weekly_reports = db.query(WeekReport).filter_by(project_name=project_name,year=year, month=month, week=week).all()
    if not db_weekly_reports:
        return JSONResponse({"code": 400, "message": "周报未找到"})
    for report in db_weekly_reports:
        db.delete(report)
    db.commit()
    logger.info(f"当前用户：{current_user}, 删除周报, 项目名称：{project_name}, 年份：{year}, 月份：{month}, 周数：{week}")
    return JSONResponse({"code": 200, "message": "删除周报成功"})


"""日志管理接口"""


@app.get("/logs/")
def get_logs():
    with open("./log.log", "r+") as log_file:
        lines = log_file.readlines()
        last_1000_lines = lines[-1000:] if len(lines) > 1000 else lines
        log_file.seek(0)
        log_file.truncate()
        log_file.writelines(last_1000_lines)
    return JSONResponse({"code": 200, "message": "查看日志成功", "data": "".join(last_1000_lines)})


# 启动命令
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
