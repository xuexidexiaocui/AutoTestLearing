import os
from datetime import datetime
from utils.logger import logger


def take_screenshot(driver, screenshot_name="screenshot"):
    """
    截取页面截图
    :param driver: WebDriver 实例
    :param screenshot_name: 截图名称
    :return: 截图保存路径
    """
    # 创建截图目录
    screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # 截图文件名（时间戳避免重复）
    screenshot_path = os.path.join(
        screenshot_dir,
        f"{screenshot_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )

    try:
        driver.save_screenshot(screenshot_path)
        logger.info(f"截图成功，保存路径：{screenshot_path}")
        return screenshot_path
    except Exception as e:
        logger.error(f"截图失败：{str(e)}")
        return None