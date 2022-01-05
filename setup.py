from setuptools import find_packages, setup
import os

__version__, requirements = '', []

with open(os.path.join(os.path.dirname(__file__), 'yaplee', '__init__.py')) as init_file:
    for line in init_file.read().splitlines():
        if(line.lower().startswith('__version__')):
            exec(line)

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as req_file:
    requirements = req_file.read().splitlines()
    req_file.close()

setup(
    name="Yaplee",
    version=str(__version__),
    description="Yaplee is a fun and simple python framework to build user interfaces on web pages",
    url="https://github.com/Yaplee",
    author='Matin Najafi',
    author_email="contact.thisismatin@gmail.com",
    license="MIT",
    include_package_data=True,
    long_description='Yaplee is a Powerful, Fun and Open Souce MIT-Licenced project for front-end programming in Python. Yaplee framework is very simple and does not have complicated details.',
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'yaplee = yaplee.main:YapleeManager'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
    zip_safe=False
)