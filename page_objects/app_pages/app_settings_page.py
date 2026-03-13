import allure
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from page_objects.app_pages.app_base_page import AppBasePage
# 给移动端用例打 @pytest.mark.app 标签
@allure.epic("移动端自动化")
@allure.feature("设置APP")
@pytest.mark.app  # 移动端用例标签
class SettingsPage(AppBasePage):
    """安卓设置页面"""
    # 元素定位器（移动端常用 ID/XPATH/ACCESSIBILITY_ID）
    SEARCH_BTN = (AppiumBy.ID, "com.android.settings:id/search")
    SEARCH_INPUT = (AppiumBy.ID, "android:id/search_src_text")
    WIFI_ITEM = (AppiumBy.XPATH, "//*[@text='WLAN']")

    def click_search(self):
        """点击搜索按钮"""
        self.click(self.SEARCH_BTN)

    def search_text(self, text):
        """在搜索框输入文本"""
        self.send_keys(self.SEARCH_INPUT, text)

    def click_wifi(self):
        """点击 WLAN 选项"""
        self.click(self.WIFI_ITEM)

    def get_wifi_text(self):
        """获取 WLAN 文本"""
        return self.get_element_text(self.WIFI_ITEM)