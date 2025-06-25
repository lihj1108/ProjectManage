import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. 添加子项目
def create_sub_project():
    sub_project_data = {
        "project_name": "杭州高速公路收费站",
        "sub_project_name": "杭州高速公路收费站二期子项",
        "building_name": "水电站",
        "floor_area": 1434.56,
        "architecture_leader_name": "zhangsan",
        "structure_leader_name": "zhangsan",
        "plumbing_leader_name": "lisi",
        "electrical_leader_name": "wangwu",
        "architecture_designers": ["wangwu", "lisi"],
        "structure_designers": ["wangzong"],
        "plumbing_designers": ["guogong"],
        "electrical_designers": ["wangwu", "ligong", "guogong"]
    }
    response = requests.post(f"{BASE_URL}/sub_projects/", json=sub_project_data)
    print("添加子项目:", response.json())

# 2. 查看所有子项目信息
def get_all_sub_projects():
    response = requests.get(f"{BASE_URL}/sub_projects/")
    print("查看所有子项目信息:", response.json())

# 3. 查看单个子项目信息
def get_sub_project(sub_project_name):
    response = requests.get(f"{BASE_URL}/sub_projects/{sub_project_name}")
    print("查看单个子项目信息:", response.json())

# 4. 修改子项目信息
def update_sub_project(sub_project_name):
    updated_data = {
        "project_name": "京杭高速公路收费站",
        "sub_project_name": "京杭高速公路收费站一期子项",
        "building_name": "收费站",
        "floor_area": 1500.75,
        "architecture_leader_name": "Updated John Doe",
        "structure_leader_name": "Updated Jane Smith",
        "plumbing_leader_name": "Updated Alice Johnson",
        "electrical_leader_name": "Updated Bob Brown",
        "architecture_designers": ["Updated Designer A", "Updated Designer B"],
        "structure_designers": ["Updated Designer C"],
        "plumbing_designers": ["Updated Designer D"],
        "electrical_designers": ["Updated Designer E", "Updated Designer F"]
    }
    response = requests.put(f"{BASE_URL}/sub_projects/{sub_project_name}", json=updated_data)
    print("修改子项目信息:", response.json())

# 5. 删除子项目
def delete_sub_project(sub_project_id):
    response = requests.delete(f"{BASE_URL}/sub_projects/{sub_project_id}")
    print("删除子项目:", response.json())

# 示例调用
if __name__ == "__main__":
    # 添加子项目
    # create_sub_project()

    # 查看所有子项目信息
    # get_all_sub_projects()

    # 查看单个子项目信息
    # get_sub_project('杭州高速公路收费站二期子项') 

    # 修改子项目信息
    # update_sub_project("京杭高速公路收费站一期子项") 

    # 删除子项目
    delete_sub_project("京杭高速公路收费站一期子项")  