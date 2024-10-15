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
    description='An AI Translator as a GoldenDict Extension',
    license='MIT',
    keywords='translator extension',
    url='https://github.com/xrysamuel/GD-Translator'
)