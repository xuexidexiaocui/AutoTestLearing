import pytest
import os
from page_objects.web_pages.login_page import LoginPage
from utils.read_yaml import read_yaml


# 读取测试数据（修复核心问题 + 增加校验 + 打印日志）
def get_login_data():
    # 1. 计算 YAML 文件绝对路径（兼容中文/空格路径）
    # __file__ = 当前文件（test_login.py）路径
    # os.path.dirname(__file__) = test_cases/ 目录
    # os.path.dirname(上一级) = 项目根目录
    first_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root_dir = os.path.dirname(first_root_dir)
    data_path = os.path.join(root_dir, "test_data", "login_data.yaml")

    # 2. 打印路径 + 校验文件是否存在（关键排查步骤）
    print(f"🔍 YAML 文件路径：{data_path}")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ 未找到 YAML 文件，请检查路径：{data_path}")

    # 3. 读取 YAML 数据 + 校验数据结构
    yaml_data = read_yaml(data_path)
    print(f"📝 读取到的原始 YAML 数据：{yaml_data}")  # 打印原始数据，确认是否读到

    # 校验 test_login 节点是否存在
    if "test_login" not in yaml_data:
        raise ValueError(f"❌ YAML 文件中缺少 'test_login' 节点，当前数据：{yaml_data}")

    # 4. 转换数据格式（核心修复：字典列表 → 元组列表）
    login_data = []
    for item in yaml_data["test_login"]:
        # 校验每个条目是否有 username/password 字段
        if "username" not in item or "password" not in item:
            raise ValueError(f"❌ YAML 数据缺少字段：{item}（需包含 username/password）")
        # 提取字段，组装成 parametrize 能识别的元组
        login_data.append((item["username"], item["password"]))

    print(f"✅ 解析后的测试数据（parametrize 可用）：{login_data}")
    return login_data


class TestLogin:
    """登录功能测试用例"""

    def setup_method(self):
        """每个用例执行前初始化登录页"""
        self.login_page = LoginPage()
        self.login_page.open_login_page()

    # 关键修复：直接传转换后的 login_data（无需再取 ["test_login"]）
    @pytest.mark.parametrize("username, password", get_login_data())
    def test_login(self, username, password):
        """登录测试用例（参数化）"""
        # 打印当前传入的参数，确认是否取到值
        print(f"\n🚀 执行登录用例：username={username}, password={password}")
        # 执行登录
        self.login_page.login(username, password)

        # （可选）添加断言（根据你的业务调整）
        # 示例：登录后检查页面标题（替换成你的业务断言）
        # assert "登录成功" in self.login_page.driver.title
if __name__ == '__main__':
    print(read_yaml())