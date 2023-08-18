# Shape CMS

Shape CMS is a composable content management system that plugs into your Python project giving you full freedom in building sites. 
It comes with an admin panel that builds itself based on the data models you create while leaving everything else up to you.

Shape CMS leverages the Flask framework under-the-hood, so you also get the full power of Flask when building apps with Shape CMS.

**Note:** There's no stable release yet, so documentation is subject to change, and I would not recommend running it in production.

## Installation

```shell
pip install shapecms
```

## Example app

A minimal example looks like this:

```python
from shapecms import ShapeCMS, PageView


class HomeView(PageView):
    def get(self):
        return "Hello, world."


app = ShapeCMS(
    import_name=__name__,
    connection_uri="sqlite:///demo.db",
    shapes=[],
    views={"/": HomeView}
)


def create_app():
    instance = app.start()
    instance.secret_key = "super-secret-key"

    return instance
```

The admin panel is automatically available at the `/admin` path. If it's your first time going to the admin panel, it will guide you through a set-up process. 

Note however that until you add any Content Shapes the admin panel will be empty as it will have no info on how to construct itself.

## Adding Content Shapes

An example Content Shape looks like this:

```python
from flask import Request
from shapecms.fields.text import TextField
from shapecms.shape import Shape

def blog_post(request: Request) -> Shape:
    return Shape(
        identifier="post",
        name="Blog Posts",
        singular_name="Blog Post",
        admin_list_view_fields=["title"],
        fields=[
            TextField(
                identifier="title", name="Post Title", placeholder="Untitled ..."
            ),
            TextField(
                identifier="slug",
                name="URL",
                prefix="{url}blog/".format(url=request.host_url),
            ),
        ],
    )
```

Pass all your content shapes into the `shapes` array when initializing ShapeCMS as references, and you're all set.