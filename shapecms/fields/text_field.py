from shapecms.shape_field import ShapeField


class TextField(ShapeField):
    placeholder: str = ""
    prefix: str = ""
    suffix: str = ""

    def set_placeholder(self, placeholder):
        self.placeholder = placeholder

    def set_prefix(self, prefix):
        self.prefix = prefix

    def set_suffix(self, suffix):
        self.suffix = suffix
