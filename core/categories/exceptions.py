class CategoryAlreadyExists(Exception):
    def __init__(self, category_name: str):
        self.msg = f"Category {category_name} has already exists."


class CategoryNotFound(Exception):
    pass
