from setuptools import setup

setup(
    name="shmup",
    version="0.0.1",
    packages=["shmup"],
    install_requires=["pygame"],
    entry_points={
        "console_scripts" : "shmup = shmup.__main__:main"
    }
)