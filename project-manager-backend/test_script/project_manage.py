import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. 添加项目
def create_project():
    project_data = {
        "name": "杭州养路站",
        "project_type": "重点项目",
        "project_stage": "深度设计",
        "start_date": "2025-12-01",
        "end_date": "2025-12-31",
        "manager_name": 'zhangsan',
        "supervisor_name": 'lisi'
    }
    response = requests.post(f"{BASE_URL}/projects/", json=project_data)
    print("添加项目:", response.json())

# 2. 查看所有项目
def get_all_projects():
    response = requests.get(f"{BASE_URL}/projects/")
    print("查看所有项目:", response.json())

# 3. 查看单个项目
def get_project(project_name):
    response = requests.get(f"{BASE_URL}/projects/{project_name}")
    print("查看单个项目:", response.json())

# 4. 修改项目
def update_project(project_name):
    updated_data = {
        "name": "Updated Project A",
        "project_type": "Type 2",
        "project_stage": "Execution",
        "start_date": "2025-05-01",
        "end_date": "2025-11-30",
        "manager_name": "zhangsan",
        "supervisor_name": "lisi"
    }
    response = requests.put(f"{BASE_URL}/projects/{project_name}", json=updated_data)
    print("修改项目:", response.json())

# 5. 删除项目
def delete_project(project_name):
    response = requests.delete(f"{BASE_URL}/projects/{project_name}")
    print("删除项目:", response.json())

# 示例调用
if __name__ == "__main__":
    # 添加项目
    # create_project()

    # 查看所有项目
    # get_all_projects()

    # # 查看单个项目
    # get_project("京杭棚户区改造")

    # # 修改项目
    # update_project("京杭棚户区改造")

    # # 删除项目
    delete_project('Updated Project A')