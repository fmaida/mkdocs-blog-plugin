__version__ = '0.1.3'

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
            int, default=6)),

        # Let's allow our user to slightly customize the "previous articles"
        # section. How do we have to name this section if it will contains
        # multiple articles? Remember to put a % character
        ('more_articles', config.config_options.Type(
            utils.string_types, default='More articles (%)')),

        # Which name do we have to give to each subsection inside our
        # "previous articles" section?
        ('pagination', config.config_options.Type(
            utils.string_types, default='Page % of %')),

        # Can we display the previous articles section, or is it better if we
        # hide it? (Default: Show it)
        ('hide_previous_articles', config.config_options.Type(
            bool, default=False)),
    )

    def on_nav(self, nav, config, files):

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
                and e.title.lower() == blog_section.lower()]
        # Have we founded that?
        if blog:
            # Yes, we did. We'll just need the first section found
            blog = blog[0]
            # Now it's time to empty whatever that section was containing
            blog.children = []
            # If the number of articles that we are going to display will be
            # too high, we'll also need a section in which we could place the
            # exceeding articles
            more = Section(title="", children=[])

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

                        # Is the "More articles" section empty ?
                        if len(more.children) == 0:
                            subsection = Section(title="", children=[])
                            more.children.append(subsection)
                        else:
                            # Or the default subsection is already full ?
                            if len(subsection.children) >= articles:
                                # Yes. Add a new subsection inside of it
                                subsection = Section(title="", children=[])
                                more.children.append(subsection)

                        subsection.children.append(page)

            # All right, we just finished scanning our mkdocs repository for
            # articles. Let's add some minor finishing touches to our sections.

            # Did the user explicitly request to hide this section?
            if not blog_config["hide_previous_articles"]:

                # How many articles do we have stored in the "More articles"
                # section?
                articles_count = sum([len(sub.children)
                                      for sub in more.children])

                # We will change the title of each subsection to display
                # something like "Page 1 of X"
                last_page = len(more.children)
                for actual_page, subpage in enumerate(more.children,
                                                      start=1):
                    subpage.title = blog_config["pagination"]\
                        .replace("%", str(actual_page), 1)\
                        .replace("%", str(last_page), 1)

                # Last thing before adding this section to our blog...
                # We need to change our "More article" section title accordingly
                # to what our user has chosen
                more.title = blog_config["more_articles"]\
                    .replace("%", str(articles_count))

                # Finished. Let's add our "More articles" section to our
                # Blog section.
                blog.children.append(more)

        # THE FOLLOWING 3 LINES OF CODE ARE JUST MEANT FOR DEBUGGING PURPOSES
        # ===================================================================
        # import pydevd_pycharm
        # pydevd_pycharm.settrace('localhost', port=5000, stdoutToServer=True,
        # stderrToServer=True)

        # Search for the blog section in the nav, and move it to the bottom
        # (this code sucks, I shall refactor it at a later time)
        found = False
        for i, item in enumerate(nav.items):
            if item.title and item.title.lower() == blog_section.lower():
                found = True
                break
        if found:
            del(nav.items[i])
            nav.items.append(blog)

        # All finished. We can give back our modified nav to mkdocs and enjoy
        # our new blog section!
        return nav
