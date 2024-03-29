from setuptools import setup, find_packages

setup(
    name='your_project_name',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Dependencies listed in requirements.txt will be automatically added here
    ],
)
