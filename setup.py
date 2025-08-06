# setup.py
from setuptools import setup, find_packages

setup(
    name="occgpu",
    version="0.1.0",
    author="Three Liu",
    author_email="liushurui66666@example.com",
    description="A tool to occupy free GPU memory and prevent others from using it",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourname/occgpu",  # 可选
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "occgpu=occgpu.cli:main", 
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: System :: Monitoring",
    ],
)