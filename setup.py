from setuptools import setup

setup(
    name='gdtranslator',
    version='0.0.1',
    packages=['gdtranslator'],
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
    keywords='translator extension',
    url='https://github.com/xrysamuel/GD-Translator'
)