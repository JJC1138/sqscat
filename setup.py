import setuptools

setuptools.setup(
    name = 'sqscat',
    version = '1.0.0dev',
    packages = setuptools.find_packages(),
    entry_points = {'console_scripts': [
        'sqscat = sqscat.__main__:main',
    ]},
)
