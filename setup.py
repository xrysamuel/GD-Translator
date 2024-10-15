from setuptools import setup, find_packages

setup(
    name='gdtranslator',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "openai",
        "flask",
        "flask_cors",
        "zc.lockfile",
        "PyYAML"
    ],
    include_package_data=True,
    author='Samuel Xu',
    author_email='xry200403@gmail.com',
    description='Translator plugin for GoldenDict',
    license='MIT',
    keywords='translator plugin',
    url='https://github.com/xrysamuel'
)