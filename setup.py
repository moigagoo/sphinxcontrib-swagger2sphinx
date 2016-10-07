from setuptools import setup

def readme():
    try:
        with open("README.rst") as f:
            return f.read()
    except IOError:
        pass


setup(
    name="sphinxcontrib-swagger2sphinx",
    version="0.1.4",
    url="https://github.com/moigagoo/sphinxcontrib-swagger2sphinx",
    download_url="https://pypi.org/project/sphinxcontrib-swagger2sphinx",
    license="MIT",
    author="Konstantin Molchanov",
    author_email="moigagoo@live.com",
    description="Converter from Swagger to Sphinx HTTP domain.",
    long_description=readme(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Documentation",
        "Topic :: Utilities",
    ],
    py_modules=["sphinxcontrib.swagger2sphinx"],
    packages=["sphinxcontrib"],
    package_dir={"sphinxcontrib": '.'},
    platforms="any",
    install_requires=["Sphinx>=1.0", "requests"]
)
