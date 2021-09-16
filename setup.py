from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="malibu",
    version="0.0.1",
    description="A game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ian Laird",
    license='MIT',
    author_email="irlaird@gmail.com",
    url="https://github.com/en0/codename-malibu",
    install_requires=['pygame'],
    packages=["malibu", "malibu_lib", "malibu_utils"],
    include_package_data=True,
    package_data={'malibu': ['assets/*']},
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)