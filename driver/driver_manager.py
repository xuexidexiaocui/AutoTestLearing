from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
# 注释掉自动下载的包，改用手动指定路径
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils.read_yaml import get_config
from utils.logger import logger

class DriverManager:
    """驱动管理类：封装驱动的创建和销毁"""
    _driver = None  # 单例驱动实例
    # 添加调试模式开关（True=保留浏览器，False=自动关闭）
    DEBUG_MODE = True

    @classmethod
    def get_driver(cls):
        """获取驱动实例（单例模式）"""
        if cls._driver is None:
            config = get_config()["web"]
            browser = config["browser"].lower()
            implicit_wait = config["implicit_wait"]
            page_load_timeout = config["page_load_timeout"]

            # 根据浏览器类型创建驱动
            if browser == "chrome":
                # 关键修改：手动指定 chromedriver 路径（替换为你实际的路径）
                chromedriver_path = r"C:\Users\Simon Cui\PycharmProjects\ui_auto_framework\driver\chromedriver.exe"
                service = ChromeService(executable_path=chromedriver_path)
                # 添加 Chrome 选项，解决路径含中文/空格问题
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                # 禁用日志（可选，减少干扰）
                chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
                cls._driver = webdriver.Chrome(service=service, options=chrome_options)
            elif browser == "firefox":
                # 如需使用火狐，同理手动指定 geckodriver 路径
                cls._driver = webdriver.Firefox()
            elif browser == "edge":
                # 如需使用 Edge，同理手动指定 msedgedriver 路径
                cls._driver = webdriver.Edge()
            else:
                raise ValueError(f"不支持的浏览器类型：{browser}")

            # 全局配置
            cls._driver.implicitly_wait(implicit_wait)  # 隐式等待
            cls._driver.set_page_load_timeout(page_load_timeout)  # 页面加载超时
            cls._driver.maximize_window()  # 窗口最大化
            logger.info(f"成功初始化 {browser} 驱动")

        return cls._driver

    @classmethod
    def quit_driver(cls):
        """关闭驱动（调试模式下不关闭）"""
        if not cls.DEBUG_MODE and cls._driver is not None:
            cls._driver.quit()
            cls._driver = None
            logger.info("驱动已关闭")
        elif cls.DEBUG_MODE:
            logger.info("调试模式：驱动未关闭，浏览器将保留")