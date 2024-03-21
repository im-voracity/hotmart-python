from setuptools import setup, find_packages

setup(
    name="hotmart_python",
    version="0.1.20",
    description="A Python library for the Hotmart API, simplifying endpoint access and resource management.",
    long_description=open("docs/README.md").read(),
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
    python_requires=">=3.7",
    install_requires=["requests>=2.31", "coloredlogs>=15.0"],
    extras_require={
        "dev": ["python-dotenv"],
    },
    packages=find_packages(),
    include_package_data=True,
)
