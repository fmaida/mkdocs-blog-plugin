__version__ = '0.1.0'

from mkdocs import config, utils
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Section
import os.path
import datetime


class Blog(BasePlugin):
    # This class will handle our blog

    config_scheme = (
        ('section', config.config_options.Type(
            utils.string_types, default='blog')),
        ('articles', config.config_options.Type(
            int, default=10)),
        ('previous_article', config.config_options.Type(
            utils.string_types, default='Previous article')),
        ('previous_articles', config.config_options.Type(
            utils.string_types, default='Previous % articles')),
        ('hide_previous_articles', config.config_options.Type(
            bool, default=False)),
    )

    def on_nav(self, nav, config, files):
        
        # List ordered by time
        ordered = []
        # Dictionary nested by year and month
        chronological = {}
        
        # For each file
        # for f in files:
        #     if "blog" in f.url:
        #         f.page = "Giovannona Coscialunga"
        # breakpoint()

        # import pydevd_pycharm
        # pydevd_pycharm.settrace('localhost', port=5000, stdoutToServer=True, stderrToServer=True)

        blog_config = config.data["plugins"]["blog"].config.data
        articles = blog_config["articles"]
        blog_section = blog_config["section"]

        # Searches the blog section
        blog = [e for e in nav.items if e.title and e.title.lower() == blog_section]
        if blog:
            blog = blog[0]
            # Empties the blog section
            blog.children = []
            previous_articles = Section(title="", children=[])

            for page in sorted(nav.pages,
                               key=lambda x: x.url, reverse=True):
                if blog_section + "/" in page.url.lower():
                    if len(blog.children) < articles:
                        # Adds the page to the blog
                        blog.children.append(page)
                    else:
                        if len(previous_articles.children) < articles:
                            previous_articles.children.append(page)

            articles_count = len(previous_articles.children)
            if articles_count > 1:
                previous_articles.title = blog_config["previous_articles"]\
                    .replace("%", str(articles_count))
                if not blog_config["hide_previous_articles"]:
                    blog.children.append(previous_articles)
            elif articles_count == 1:
                previous_articles.title = blog_config["previous_article"]
                if not blog_config["hide_previous_articles"]:
                    blog.children.append(previous_articles)

        return nav
