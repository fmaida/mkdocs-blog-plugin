__version__ = '0.1.0'

from mkdocs import config, utils
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Section
import os.path
import datetime


class Blog(BasePlugin):
    # This class, derived from mkdocs.plugins.BasePlugin
    # will handle our blog

    config_scheme = (

        # This is the section / folder in which we'll try to build our blog
        # (Default: "blog")
        ('section', config.config_options.Type(
            utils.string_types, default='blog')),

        # How many articles do we have to display on our blog at once?
        # (this number will be then doubled by the "previous articles" section)
        # (Default: 10 articles, plus another 10 in our previous articles
        # section)
        ('articles', config.config_options.Type(
            int, default=10)),

        # Let's allow our user to slightly customize the "previous articles"
        # section. How do we have to name this section if it will contains
        # multiple articles? Remember to put a % character
        ('previous_article', config.config_options.Type(
            utils.string_types, default='Previous article')),

        # How do we have to name the "previous articles" section if it only
        # contains a single article?
        ('previous_articles', config.config_options.Type(
            utils.string_types, default='Previous % articles')),

        # Can we display the previous articles section, or is it better if we
        # hide it? (Default: Show it)
        ('hide_previous_articles', config.config_options.Type(
            bool, default=False)),
    )

    def on_nav(self, nav, config, files):

        # THE FOLLOWING 3 LINES OF CODE ARE JUST MEANT FOR DEBUGGING PURPOSES
        # ===================================================================
        # import pydevd_pycharm
        # pydevd_pycharm.settrace('localhost', port=5000, stdoutToServer=True,
        # stderrToServer=True)

        # Our plugin code starts here!

        # We are starting by reading the configuration parameters for our
        # plugin
        blog_config = config.data["plugins"]["blog"].config.data

        # How many articles do we have to display in the blog part.
        # This number will be doubled by the nested "previous articles"
        # section
        articles = blog_config["articles"]
        # The title of the section that will contain the blog part
        # By default, it searches for a section titled "blog"
        blog_section = blog_config["section"]

        # Searches for a section that is titled the blog section
        blog = [e for e in nav.items if e.title
                and e.title.lower() == blog_section]
        # Have we founded that?
        if blog:
            # Yes, we did. We'll just need the first section found
            blog = blog[0]
            # Now it's time to empty whatever that section was containing
            blog.children = []
            # If the number of articles that we are going to display will be
            # too high, we'll also need a section in which we could place the
            # exceeding articles
            previous_articles = Section(title="", children=[])

            # All right, it's time to start searching our mkdocs repository for
            # potentials blog articles. We want to sort our list of pages by
            # their URL value, in descending order.
            # Why? Because each of our blog articles will be saved in this
            # format:
            #
            # mkdocs/docs/blog/2020/01/2020-01-20--first_post.md
            # mkdocs/docs/blog/2020/01/2020-01-25--second_post.md
            # mkdocs/docs/blog/2020/02/2020-02-01--third_post.md
            #
            # By reversing the alphabetical order, We'll ensure to get this
            # articles list in this order:
            #
            # "third post"  (2020-02-01--third_post.md)
            # "second post" (2020-01-25--second_post.md)
            # "first post"  (2020-01-20--first_post.md)
            #
            for page in sorted(nav.pages,
                               key=lambda x: x.url, reverse=True):
                # Let's have a look at the URL of this page... hmm...
                # Is it nested in the folder/section we have chosen for keeping
                # our blog articles ? Let's have a case-insensitive check...
                if blog_section + "/" in page.url.lower():
                    # Yes, it is in the right folder / section.
                    # Now, let's check if we already have enough articles in
                    # our blog section
                    if len(blog.children) < articles:
                        # No, there's still space available.
                        # Let's add this page to our blog section
                        blog.children.append(page)
                    else:
                        # Our blog section is already at full capacity.
                        # Well, let's see if we can add this article to the
                        # "previous articles" section that (maybe) will be
                        # added at the end
                        if len(previous_articles.children) < articles:
                            # Yes, we can add it to the "previous articles"
                            # section, so let's do it.
                            previous_articles.children.append(page)

            # All right, we just finished scanning our mkdocs repository for
            # articles. Let's add some minor finishing touches to our sections.
            # How many articles do we have stored in the "previous articles"
            # section?
            articles_count = len(previous_articles.children)
            # Do we have more than one article in that section?
            if articles_count > 1:
                # Yes. Then let's call the section with a plural name.
                # Our user can change this name by adding a parameter.
                previous_articles.title = blog_config["previous_articles"]\
                    .replace("%", str(articles_count))
                # Did the user explicitly request to hide this section? No?
                if not blog_config["hide_previous_articles"]:
                    # Then let's add the previous articles section to our
                    # blog section
                    blog.children.append(previous_articles)
            elif articles_count == 1:
                previous_articles.title = blog_config["previous_article"]
                # Did the user explicitly request to hide this section? No?
                if not blog_config["hide_previous_articles"]:
                    # Then let's add the previous article section to our
                    # blog section
                    blog.children.append(previous_articles)

        # Finished. We can give back our modified nav to mkdocs and enjoy
        # our new blog section!
        return nav
