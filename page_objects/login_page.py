import time

import allure
import pytest
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
from utils.read_yaml import get_config
@allure.epic("Web 自动化")
@allure.feature("登录功能")
@pytest.mark.web  # Web 用例标签
class LoginPage(BasePage):
    """登录页面：封装登录页的元素和操作"""
    # 元素定位器（统一管理，便于维护）
    INPUT_USERNAME = (By.XPATH, '//*[@id="account_input"]')  # 百度登录账号输入框
    INPUT_PASSWORD = (By.XPATH, '//*[@id="password_input"]')  # 密码输入框
    BTN_IPS_LOGIN = (By.XPATH,'//*[@id="root"]/section/main/div/div[1]/div[3]/div/div[2]/div[2]/div[2]/div[4]')
    BTN_AGREEMENT = (By.XPATH, '//*[@id="root"]/section/main/div/div[1]/div[3]/div/div[2]/div[1]/div[3]/label/span/div')         # 登录按钮
    BTN_LOGIN = (By.XPATH, '//*[@id="root"]/section/main/div/div[1]/div[3]/div/div[2]/div[1]/div[1]/form/button')          # 错误提示

    def __init__(self):
        super().__init__()
        self.config = get_config()
        self.login_url = self.config["web"]["url"]  # 登录页 URL

    def open_login_page(self):
        """打开登录页面"""
        self.open_url(self.login_url)

    def login(self, username, password):
        """执行登录操作"""
        self.click(self.BTN_IPS_LOGIN)
        self.click(self.BTN_AGREEMENT)
        self.send_keys(self.INPUT_USERNAME, username)
        self.send_keys(self.INPUT_PASSWORD, password)
        self.click(self.BTN_LOGIN)
        time.sleep(10)

    # def get_error_text(self):
    #     """获取登录错误提示"""
    #     return self.get_text(self.TXT_ERROR)
if __name__ == '__main__':
    login= LoginPage()
    a = login.open_login_page()
    c= login.login(get_config())
    print("登录操作执行完成，浏览器将保持打开，按回车键关闭...")
    input()  # 等待用户按回车，再执行后续操作