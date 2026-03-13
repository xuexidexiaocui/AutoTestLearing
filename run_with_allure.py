import os
import sys
import pytest
import subprocess
import argparse
from datetime import datetime
from utils.logger import logger
from driver.driver_manager import DriverManager


def parse_args():
    """解析命令行参数：指定执行用例类型（web/app/all）"""
    parser = argparse.ArgumentParser(description="执行自动化测试：支持 web/app/all 类型")
    parser.add_argument(
        "--case-type",
        type=str,
        default="all",  # 默认执行所有用例
        choices=["web", "app", "all"],  # 仅允许这三个值
        help="指定执行的用例类型：web（仅Web）、app（仅移动端）、all（全部）"
    )
    return parser.parse_args()


def run_tests():
    # 1. 解析命令行参数
    args = parse_args()
    case_type = args.case_type
    if case_type == "web-smoke":
        args.append("-m 'web and smoke'")
    # 执行 Web 或 App 标签的用例（等价于 all）
    args.append("-m 'web or app'")
    logger.info(f"🚀 开始执行 {case_type} 类型用例...")

    # 2. 定义 Allure 报告目录（带时间戳）
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    allure_results_dir = os.path.join(os.path.dirname(__file__), "reports", "allure_results")
    # 按用例类型生成不同的报告目录
    if case_type == "web":
        allure_report_dir = os.path.join(os.path.dirname(__file__), f"web_report_{timestamp}")
    elif case_type == "app":
        allure_report_dir = os.path.join(os.path.dirname(__file__), f"app_report_{timestamp}")
    else:
        allure_report_dir = os.path.join(os.path.dirname(__file__), f"all_report_{timestamp}")
    # 创建目录（不存在则新建）
    for dir_path in [allure_results_dir, allure_report_dir]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    # 3. 构造 pytest 基础参数
    pytest_args = [
        "test_cases/",  # 用例根目录
        "-v",  # 详细输出
        "-s",  # 输出打印信息
        f"--alluredir={allure_results_dir}",  # Allure 原始数据
        "--clean-alluredir",  # 清空旧报告数据
        f"--reruns={1}",  # 失败重跑1次
        "--reruns-delay=2",  # 重跑延迟2秒
        "-W ignore::DeprecationWarning"  # 忽略弃用警告
    ]

    # 4. 根据 case_type 筛选用例（核心：通过 -m 筛选标签）
    if case_type == "web":
        pytest_args.append("-m web")  # 仅执行 @pytest.mark.web 的用例
    elif case_type == "app":
        pytest_args.append("-m app")  # 仅执行 @pytest.mark.app 的用例
    # case_type == "all" 时，不添加 -m 参数，执行所有用例

    # 5. 执行 pytest 用例
    try:
        pytest.main(pytest_args)
    except Exception as e:
        logger.error(f"❌ 用例执行失败：{e}")
        raise
    finally:
        # 无论是否失败，都关闭驱动
        DriverManager.quit_all()

    # 6. 生成 Allure HTML 报告
    logger.info(f"📊 开始生成 Allure 报告：{allure_report_dir}")
    subprocess.call(
        [f"allure generate {allure_results_dir} -o {allure_report_dir} --clean"],
        shell=True
    )

    # 7. 自动打开报告（Windows）
    subprocess.call([f"allure open {allure_report_dir}"], shell=True)
    logger.info(f"✅ 测试完成！报告路径：{allure_report_dir}")


if __name__ == "__main__":
    run_tests()