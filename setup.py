
from distutils.core import setup

setup(
    name="mkdocs-blog-plugin",
    version="0.1.0",
    author="Francesco Maida",
    author_email="francesco.maida@gmail.com",
    packages=["mkdocs_blog"],
    license="LICENSE.txt",
    description="Keeps a really simple blog in your mkdocs",
    install_requires=[
        "mkdocs",
    ],

    entry_points={
        "mkdocs.plugins": [
            "blog = mkdocs_blog:Blog",
        ]
    }
)

