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
from shapecms import ShapeCMS
from shapecms import PageView


class HomeView(PageView):
    def get(self):
        return "Hello, world."


shape = ShapeCMS(__name__, "sqlite:///demo.db")
shape.add_url("/", HomeView, "home")


def create_app():
    instance = shape.start()
    instance.secret_key = "super-secret-key"

    return instance
```

The admin panel is automatically available at the `/admin` path. If it's your first time going to the admin panel, it will guide you through a set-up process. 

Note however that until you add any Content Shapes the admin panel will be empty as it will have no info on how to construct itself.

## Adding Content Shapes

To be written.