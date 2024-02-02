import pathlib
import setuptools

setuptools.setup(
    name="hotmart-python",
    version="0.1.0",
    description="A Python library for the Hotmart API, simplifying endpoint access and resource management.",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/im-voracity/hotmart-python",
    author="Matheus Tenório",
    author_email="matheusct16@gmail.com",
    license="Apache 2.0",
    project_urls={
        "Documentation": "https://github.com/im-voracity/hotmart-python/blob/master/README.md",
        "Source": "https://github.com/im-voracity/hotmart-python"
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10, <= 3.13",
    install_requires=["certifi==2023.11.17", "charset-normalizer==3.3.2",
                      "colorama==0.4.6", "coloredlogs==15.0.1", "humanfriendly==10.0",
                      "idna==3.6", "pyreadline3==3.4.1", "python-dotenv==1.0.1",
                      "requests==2.31.0", "urllib3==2.1.0"],
    packages=setuptools.find_packages(),
    include_package_data=True,
)
