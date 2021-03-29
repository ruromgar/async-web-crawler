from setuptools import setup, find_packages

REQUIREMENTS = [
    "asyncio==3.4.3",
    "asynctest == 0.12.2",
    "coverage==4.5.4",
    "fastapi==0.63.0",
    "Hypercorn==0.11.2",
    "pytest==5.2.0",
    "pytest-asyncio==0.10.0",
    "pytest-cov==2.7.1",
    "redis==3.5.3",
]

setup(
    name='common-utils',
    version='1.0.0',
    description='Utilities',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=['*tests']),
    include_package_data=True,
    setup_requires=[
        'pytest-runner',
    ],
    test_suite='test.unittest'
)
