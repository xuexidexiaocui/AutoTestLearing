from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver.driver_manager import DriverManager
from utils.logger import logger
from utils.screenshot import take_screenshot

class BasePage:
    """页面基类：封装所有页面通用的操作"""
    def __init__(self):
        self.driver = DriverManager.get_driver()
        self.logger = logger

    def wait_for_element(self, locator, timeout=10):
        """
        显式等待元素可见
        :param locator: 元素定位器，格式 (By.ID, "element_id")
        :param timeout: 超时时间
        :return: 元素对象
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.info(f"元素 {locator} 已可见")
            return element
        except Exception as e:
            self.logger.error(f"等待元素 {locator} 失败：{str(e)}")
            take_screenshot(self.driver, f"wait_element_fail_{locator[1]}")
            raise

    def click(self, locator):
        """点击元素"""
        element = self.wait_for_element(locator)
        element.click()
        self.logger.info(f"点击元素 {locator}")

    def send_keys(self, locator, text):
        """输入文本"""
        element = self.wait_for_element(locator)
        element.clear()  # 清空输入框
        element.send_keys(text)
        self.logger.info(f"向元素 {locator} 输入文本：{text}")

    def get_text(self, locator):
        """获取元素文本"""
        element = self.wait_for_element(locator)
        text = element.text
        self.logger.info(f"获取元素 {locator} 文本：{text}")
        return text

    def open_url(self, url):
        """打开网址"""
        self.driver.get(url)
        self.logger.info(f"打开网址：{url}")