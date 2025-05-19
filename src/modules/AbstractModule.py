
class AbstractModule:

    def __init__(self):
        super().__init__()
        self.options: dict = {}

    def add_options(self, options: str):
        if ':' in options:
            options = options.split(':')[1]

        for option in options.split(','):
            if '=' in option:
                key, value = option.split('=', 1)
                self.options[key] = value
            else:
                self.options[option] = True

    def can_handle(self, module_option: str) -> bool:
        return False
