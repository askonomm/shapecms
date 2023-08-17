from shapecms.page_views import AdminPageView


class ContentEditView(AdminPageView):
    def get(self, identifier: str, id: int):
        return "hello"