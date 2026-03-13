from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from appium import webdriver as appium_webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from utils.read_yaml import get_config
from utils.logger import logger


class DriverManager:
    """驱动管理类：封装 Web/App 驱动的创建和销毁，支持按需初始化"""
    # 分别维护 Web 和 App 驱动实例（避免互相干扰）
    _web_driver = None
    _app_driver = None
    # 调试模式开关（True=保留浏览器/App，False=自动关闭）
    DEBUG_MODE = True
    # 新增：当前执行的用例类型（web/app/all），控制驱动初始化
    _case_type = "all"

    # ===== 新增：设置用例类型（由 run_tests.py 调用）=====
    @classmethod
    def set_case_type(cls, case_type):
        """
        设置当前执行的用例类型
        :param case_type: web/app/all
        """
        if case_type not in ["web", "app", "all"]:
            raise ValueError(f"不支持的用例类型：{case_type}，仅支持 web/app/all")
        cls._case_type = case_type
        logger.info(f"✅ 当前执行用例类型：{cls._case_type}")

    # ===== Web 驱动（原有逻辑优化）=====
    @classmethod
    def get_web_driver(cls):
        """获取 Web 驱动实例（仅当用例类型为 web/all 时初始化）"""
        # 非 web/all 类型，直接返回 None，不初始化 Web 驱动
        if cls._case_type not in ["web", "all"]:
            logger.info("🔴 非 Web 用例类型，跳过 Web 驱动初始化")
            return None

        if cls._web_driver is None:
            config = get_config()["web"]
            browser = config["browser"].lower()
            implicit_wait = config["implicit_wait"]
            page_load_timeout = config["page_load_timeout"]

            # 根据浏览器类型创建驱动
            if browser == "chrome":
                # 手动指定 chromedriver 路径（替换为你的实际路径）
                chromedriver_path = r"C:\Users\Simon Cui\PycharmProjects\ui_auto_framework\driver\chromedriver.exe"
                service = ChromeService(executable_path=chromedriver_path)
                # Chrome 选项：解决路径含中文/空格、禁用日志
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
                cls._web_driver = webdriver.Chrome(service=service, options=chrome_options)
            elif browser == "firefox":
                cls._web_driver = webdriver.Firefox(service=FirefoxService())
            elif browser == "edge":
                cls._web_driver = webdriver.Edge(service=EdgeService())
            else:
                raise ValueError(f"不支持的浏览器类型：{browser}")

            # 全局配置
            cls._web_driver.implicitly_wait(implicit_wait)
            cls._web_driver.set_page_load_timeout(page_load_timeout)
            cls._web_driver.maximize_window()
            logger.info(f"✅ 成功初始化 {browser} Web 驱动")

        return cls._web_driver

    # ===== App 驱动（修复未定义 _app_driver 问题 + 按需初始化）=====
    @classmethod
    def get_app_driver(cls):
        """获取 App 驱动实例（仅当用例类型为 app/all 时初始化）"""
        # 非 app/all 类型，直接返回 None，不初始化 App 驱动
        if cls._case_type not in ["app", "all"]:
            logger.info("🔴 非 App 用例类型，跳过 App 驱动初始化")
            return None

        if cls._app_driver is None:
            config = get_config()["app"]
            # 移动端 Desired Capabilities
            desired_caps = {
                "platformName": config["platform_name"],
                "platformVersion": config["platform_version"],
                "deviceName": config["device_name"],
                "appPackage": config["app_package"],
                "appActivity": config["app_activity"],
                "udid": config["udid"],
                "noReset": True,
                "automationName": "UiAutomator2",
                "unicodeKeyboard": True,
                "resetKeyboard": True
            }
            # 连接 Appium 服务创建驱动
            cls._app_driver = appium_webdriver.Remote(
                command_executor=config["appium_server"],
                desired_capabilities=desired_caps
            )
            cls._app_driver.implicitly_wait(config["implicit_wait"])
            logger.info("✅ 成功初始化 Android App 驱动")

        return cls._app_driver

    # ===== 驱动关闭逻辑（优化，按需关闭）=====
    @classmethod
    def quit_web_driver(cls):
        """关闭 Web 驱动"""
        if cls._web_driver is not None:
            if not cls.DEBUG_MODE:
                cls._web_driver.quit()
                cls._web_driver = None
                logger.info("✅ Web 驱动已关闭")
            else:
                logger.info("📌 调试模式：Web 驱动未关闭")

    @classmethod
    def quit_app_driver(cls):
        """关闭 App 驱动"""
        if cls._app_driver is not None:
            if not cls.DEBUG_MODE:
                cls._app_driver.quit()
                cls._app_driver = None
                logger.info("✅ App 驱动已关闭")
            else:
                logger.info("📌 调试模式：App 驱动未关闭")

    @classmethod
    def quit_all(cls):
        """关闭所有已初始化的驱动（按需关闭）"""
        logger.info("🔍 开始关闭所有驱动...")
        cls.quit_web_driver()
        cls.quit_app_driver()
        # 重置用例类型和驱动实例（避免下次执行受影响）
        cls._case_type = "all"
        cls._web_driver = None
        cls._app_driver = None
        logger.info("✅ 所有驱动已重置")

    # ===== 兼容原有方法（避免旧代码报错）=====
    @classmethod
    def get_driver(cls):
        """兼容原有 Web 驱动调用方式"""
        return cls.get_web_driver()

    @classmethod
    def quit_driver(cls):
        """兼容原有 Web 驱动关闭方式"""
        cls.quit_web_driver()