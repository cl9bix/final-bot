from setuptools import setup, find_namespace_packages

setup(
    name='console-bot',
    version='1',
    description='console-helper-bot',
    url='https://github.com/Dmytro-Babenko/console-helper-bot',
    author='Dmytro Babenko',
    author_email='dmytro.babenko87@gmail.com',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['console-bot = console_bot.main:main']}
)