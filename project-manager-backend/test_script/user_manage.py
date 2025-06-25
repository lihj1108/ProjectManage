import requests

# FastAPI 服务地址
url = "http://127.0.0.1:8000/users/"


# 添加人员
def add_user():
    # 要添加的用户数据
    user_data = {"username": "zhaosi", "password": "123456", "real_name": "赵四", "is_leader": True}

    # 发送 POST 请求
    response = requests.post(url, json=user_data)

    # 打印结果
    if response.status_code == 200:
        print("用户添加成功：", response.json())
    else:
        print("添加失败：", response.status_code, response.text)


# 查看所有人员信息
def get_all_users():
    response = requests.get(url)
    print("查看所有人员信息:", response.json())


# 修改人员信息
def update_user(username, user_data):
    response = requests.put(f"{url}{username}", json=user_data)
    print("修改人员信息:", response.json())


# 删除人员
def delete_user(username):
    response = requests.delete(f"{url}{username}")
    print("删除人员:", response.json())


if __name__ == "__main__":
    # add_user()
    get_all_users()
    # update_user("wangwu", {"username": "wangwu", "is_leader": False})
    # delete_user("zhaosi")
