from distutils.core import setup

# Read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst"), encoding='utf-8') as f:
    read_me = f.read()

setup(
    name="mkdocs-blog-plugin",
    version="0.25",
    author="Francesco Maida",
    author_email="francesco.maida@gmail.com",
    packages=["mkdocs_blog"],
    url='https://github.com/fmaida/mkdocs-blog-plugin',
    license="MIT",
    description="Keeps a really simple blog section inside your MkDocs site.",
    long_description_content_type="text/x-rst",
    long_description=read_me,
    install_requires=[],

    entry_points={
        "mkdocs.plugins": [
            "blog = mkdocs_blog:Blog",
        ]
    }
)

