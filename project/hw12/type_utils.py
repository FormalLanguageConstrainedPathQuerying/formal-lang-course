from project.hw12.types_t import Types_t
class Env:
    def __init__(self):
        self.__variable_types: dict[str, Types_t] = {}

    def clear(self):
        self.__variable_types.clear()

    def add_variable(self, name: str, type_: Types_t):
        assert (
            type_ != Types_t.UNKNOWN
        ), "You try to assign expression with unknown to variable"
        self.__variable_types[name] = type_

    def get_variable(self, name: str) -> Types_t:
        return self.__variable_types[name]

    def contain_variable(self, name: str) -> bool:
        return name in self.__variable_types.keys()
