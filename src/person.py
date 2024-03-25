class Person:
    def __init__(self, name, wiki_url=None, additional_data=None):
        self._wiki_url = wiki_url
        self._name = name
        if additional_data is None:
            additional_data = {}
        self.additional_data = additional_data

    def get_wiki_url(self):
        return self._wiki_url

    def get_name(self):
        return self._name

    def __str__(self):
        return self._name

    def __eq__(self, other):
        if isinstance(other, Person):
            if self._wiki_url is not None:  # and other._wiki_url is not None
                return self._wiki_url == other._wiki_url
            return self._name == other._name
        else:
            return False

    def update(self, other):
        if not isinstance(other, Person):
            raise NotImplementedError("cant update ManIdentity with instance of different class")
        if self._wiki_url is None:
            self._wiki_url = other._wiki_url

            if self.additional_data == {}:
                self.additional_data = other.additional_data

        elif self._name is None:
            self._name = other._name

    def __hash__(self):
        return hash("")
