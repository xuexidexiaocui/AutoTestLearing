import os
import pytest
from utils.logger import logger

if __name__ == "__main__":
    # 定义测试报告路径
    report_dir = os.path.join(os.path.dirname(__file__), "reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    report_path = os.path.join(report_dir, "test_report.html")

    # 构造 pytest 命令参数
    pytest_args = [
        "test_cases/",                # 测试用例目录
        "-v",                         # 详细输出
        "-s",                         # 输出打印信息
        f"--html={report_path}",      # 生成 HTML 报告
        "--self-contained-html",      # 报告独立（包含图片）
        f"--reruns={0}",              # 失败重跑次数
        "--reruns-delay=2",           # 重跑延迟（秒）
        "-W ignore::DeprecationWarning"  # 忽略弃用警告
    ]

    # 执行测试用例
    logger.info("开始执行测试用例...")
    pytest.main(pytest_args)
    logger.info(f"测试报告已生成：{report_path}")