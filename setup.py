from pathlib import Path
from setuptools import setup, find_packages

setup(
    name="xue",
    version="0.0.31",
    description="A minimalist web front-end framework composed of HTMX and Python.",
    long_description=Path("README.md").open(encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "xue": ["icons/*"]  # 包含xue包下的icons目录中的所有文件
    },
    py_modules=["xue"],
)