from setuptools import setup
from easyraac.__init__ import version

setup(name='easyraac',
    version=version,
    description='an intelligent protein analysis toolkit based on raac and pssm ',
    url='https://github.com/KingoftheNight/RPCT-package',
    author='liangyc',
    author_email='1694822092@qq.com',
    license='BSD 2-Clause',
    packages=['easyraac'],
    install_requires=[],
    entry_points={
        'console_scripts': [
        'easyraac=easyraac.__main__:rpct_main',
            ]
        },
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=True)