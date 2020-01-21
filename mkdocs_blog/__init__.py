__version__ = '0.2'

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
        ("folder", config.config_options.Type(
            utils.string_types, default="blog")),

        # How many articles do we have to display on our blog at once?
        # (this number will be then augmented by the "more articles" section)
        # (Default: 6 articles)
        ("articles", config.config_options.Type(
            int, default=6)),

        # Let's allow our user to slightly customize the "more articles"
        # section. How do we have to name this section if it will contains
        # multiple articles? Remember to put a % character
        ("more-articles", config.config_options.Type(
            utils.string_types, default="More articles (%)")),

        # Which name do we have to give to each subsection inside our
        # "previous articles" section?
        ("pagination", config.config_options.Type(
            utils.string_types, default="Page % of %")),

        # Can we display the "more articles" section, or is it better if we
        # hide it? (Default: Show it)
        ("display-more-articles", config.config_options.Type(
            bool, default=True)),

        # Can we display the article date in the navbar, or is it better if we
        # hide it? (Default: Show it)
        ("display-article-date", config.config_options.Type(
            bool, default=True)),

        # How we have to display an article date on the navbar?
        ("format", config.config_options.Type(
            utils.string_types, default="[%d/%m]")),

        # Do we have to display an article date on the left or on the right?
        ("text-align", config.config_options.Type(
            utils.string_types, default="left")),
    )

    def extract_date(self, url):
        """
        Extracts a date from a URL in a format like this:
        "/<tag>/<year>/<month>/<day>/<article name>/"

        Args:
            url: The URL that has to be check

        Returns:
            a datetime.date object if a date is found,
            otherwise returns None
        """
        article_date = None
        blog_tag = self.config["folder"].lower()
        start = url.lower().find(blog_tag)
        if start >= 0:
            try:
                start += len(blog_tag) + 1
                temp = url[start:start+10].split("/")
                article_date = datetime.date(year=int(temp[0]),
                                             month=int(temp[1]),
                                             day=int(temp[2]))
            except ValueError:
                pass
        return article_date

    def on_nav(self, nav, config, files):
        """
        From MkDocs documentation:
        ==========================
        The nav event is called after the site navigation is created and can
        be used to alter the site navigation.

        Args:
            nav: Our navbar
            config: Global configuration
            files: List of files

        Returns:
            A modified navbar
        """

        # Our plugin code starts here!
        # We are starting by reading the configuration parameters
        # for our plugin

        # How many articles do we have to display in the blog part.
        # This number will be doubled by the nested "previous articles"
        # section
        articles = self.config["articles"]

        # The title of the section that will contain the blog part
        # By default, it searches for a section titled "blog"
        blog_section = self.config["folder"]

        # Searches for a section that is titled the blog section
        blogs_found = [(i, e) for i, e in enumerate(nav.items)
                       if e.title and e.title.lower() == blog_section.lower()]
        # Have we founded that?
        if not blogs_found:
            # Nope. We'll give back control to MkDocs...
            return nav

        # Yes, since we are still here we did found at least one blog folder.
        # We'll just need to pick up the first occurrence found
        blog_position, blog = blogs_found[0]

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
                        # noinspection PyUnboundLocalVariable
                        if len(subsection.children) >= articles:
                            # Yes. Add a new subsection inside of it
                            subsection = Section(title="", children=[])
                            more.children.append(subsection)

                    subsection.children.append(page)

        # All right, we just finished scanning our MkDocs repository for
        # articles. Let's add some minor finishing touches to our sections.

        # Did the user allows to show this section?
        if self.config["display-more-articles"]:

            # How many articles do we have stored in the "More articles"
            # section?
            articles_count = sum([len(sub.children)
                                  for sub in more.children])

            if articles_count > 0:

                # We will change the title of each subsection to display
                # something like "Page 1 of X"
                last_page = len(more.children)
                for actual_page, subpage in enumerate(more.children,
                                                      start=1):
                    subpage.title = self.config["pagination"]\
                        .replace("%", str(actual_page), 1)\
                        .replace("%", str(last_page), 1)

                # Last thing before adding this section to our blog...
                # We need to change our "More article" section title
                # accordingly to what our user has chosen
                more.title = self.config["more-articles"]\
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
        # Let's start by removing the blog section from wherever MkDocs has
        # put it, in first place
        del(nav.items[blog_position])

        # Now we'll append the blog section at the end of the nav element
        nav.items.append(blog)

        # All finished. We can give back our modified nav to MkDocs and enjoy
        # our new blog section!
        return nav

    def on_page_markdown(self, markdown, page, config, nav=None, **kwargs):
        """
        Now we are checking a single page.

        Args:
            markdown:
            page:
            config:
            nav:
            **kwargs:

        Returns:
            Our page content, eventually modified.
        """

        # Is our page a blog article?
        # I can recognize that because our page URL will have inside our
        # folder. For example: "/blog/2020/12/31/happy-new-years-eve.md"
        if self.config["folder"].lower() in page.url.lower():

            # Let's try to extract a date from that URL
            article_date = self.extract_date(page.url)

            # Have we found a usable date in that URL?
            if article_date and self.config["display-article-date"]:
                # Yes. Then let's change our page title accordingly.
                temp = self.config["format"]
                temp = temp.replace("%d", str(article_date.day).zfill(2))
                temp = temp.replace("%m", str(article_date.month).zfill(2))
                temp = temp.replace("%y", str(article_date.year).zfill(4)[:2])
                temp = temp.replace("%Y", str(article_date.year).zfill(4))
                if self.config["text-align"].lower() == "right":
                    page.title = "{} {}".format(page.title, temp)
                else:
                    page.title = "{} {}".format(temp, page.title)

        return markdown

