
from setuptools.config.pyprojecttoml import read_configuration
import tomllib
if __name__ == '__main__':
    try:
        with open('pyproject.toml', 'rb') as f:
                tomllib.load(f)
        print('✅ TOML语法正确')
    except Exception as e:
        print(f'❌ TOML语法错误: {e}')
        
    try:
        config = read_configuration('pyproject.toml')
        print('✅ 配置文件语法正确')
        print('项目名称:', config.get('name'))
    except Exception as e:
        print('❌ 配置错误:', e)
