from appium.webdriver.common.appiumby import AppiumBy  # 移动端定位方式
from driver.driver_manager import DriverManager
from utils.logger import logger
from utils.screenshot import take_screenshot

class AppBasePage:
    """移动端页面基类"""
    def __init__(self):
        self.driver = DriverManager.get_app_driver()
        self.logger = logger

    def wait_for_element(self, locator, timeout=10):
        """显式等待元素（移动端定位器：(AppiumBy.ID, "id")）"""
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.info(f"✅ 元素 {locator} 已可见")
            return element
        except Exception as e:
            self.logger.error(f"❌ 等待元素失败：{e}")
            take_screenshot(self.driver, f"wait_fail_{locator[1]}")
            raise

    def click(self, locator):
        """点击元素"""
        self.wait_for_element(locator).click()
        self.logger.info(f"🔍 点击元素：{locator}")

    def send_keys(self, locator, text):
        """输入文本"""
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"📝 输入文本：{text} 到 {locator}")

    def swipe_up(self, duration=500):
        """向上滑动页面"""
        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        self.driver.swipe(
            start_x=width/2, start_y=height*0.8,
            end_x=width/2, end_y=height*0.2,
            duration=duration
        )
        self.logger.info("📱 向上滑动页面")

    def get_element_text(self, locator):
        """获取元素文本"""
        return self.wait_for_element(locator).text