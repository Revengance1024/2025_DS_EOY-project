from modules.AbstractModule import AbstractModule

# TODO: Actually implement module support
class DuckDuckGoModule(AbstractModule):

    def can_handle(self, module_option: str) -> bool:
        return module_option.startswith('ddg')
