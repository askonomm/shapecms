from shapecms.shape_view import PageView


class AdminView(PageView):
    def get(self):
        return "hello"
