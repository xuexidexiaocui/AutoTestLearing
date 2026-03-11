import yaml
import os

def read_yaml(file_path):
    """读取 YAML 文件"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"YAML 文件不存在：{file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# 读取全局配置的快捷方法
def get_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.yaml")
    return read_yaml(config_path)

if __name__ == '__main__':
    print(read_yaml(r'C:\Users\Simon Cui\PycharmProjects\ui_auto_framework\test_data\login_data.yaml'))