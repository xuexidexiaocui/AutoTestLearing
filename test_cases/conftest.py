import pytest
from driver.driver_manager import DriverManager
from utils.logger import logger
from utils.screenshot import take_screenshot

@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    """全局夹具：所有用例执行前初始化驱动，执行后关闭驱动"""
    logger.info("===== 开始执行 UI 自动化测试 =====")
    yield  # 执行测试用例
    DriverManager.quit_driver()
    logger.info("===== UI 自动化测试执行完毕 =====")

@pytest.fixture(scope="function", autouse=True)
def case_teardown(request):
    """用例级夹具：用例失败时自动截图"""
    yield
    # 检查用例是否失败
    if request.node.rep_call.failed:
        logger.error(f"用例 {request.node.name} 执行失败，自动截图")
        take_screenshot(DriverManager.get_driver(), request.node.name)

# 修复 pytest-html 报告中失败用例的截图展示
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)