# Blogs for MkDocs (MkDocs-Blog-Plugin)

From time to time you might want to have a 
small blog section inside your MkDocs 
documentation site. 

### How can I install it ?

You can install it through pip with this 
command:

```sh
pip install mkdocs-blog-plugin
```

Then, open your `mkdocs.yml` configuration 
file and add these lines:

```yaml
plugins:
    - blog
```

Last but not least, enter you `docs` folder 
and create a new subfolder and name it `blog`. 
This plugin will try to find blog articles 
inside this directory.  

Then you are ready to begin.

### How can I add new articles to my blog section ?

Inside `docs/blog` create a folder for each 
year you are planning to add new articles. 
Then, inside each year folder create twelve 
folders, numbered from `01` to `12` for each 
month.  
Now, for every article you will go inside 
the corresponding year/month folder and you 
will create a new file there.
While it is not necessary that you keep this 
strict naming convention, you should name 
your folder and your files in a way it could 
be easily ordered. My suggestion is to 
call each new file like this:

`YYYY-MM-DD--your-article-title.md`

For example:

```sh
docs
├── blog
│   ├── 2019
│   └── 2020
│       ├── 01
│       │   ├── 2020-01-20--first-article.md
│       │   └── 2020-01-26--second-article.md
│       ├── 02
│       │   ├── 2020-02-01--third-article.md
│       │   └── 2020-02-09--fourth-article.md
│       └── 03
│           └── 2020-03-16--fifth-article.md
└── index.md
```

TODO
