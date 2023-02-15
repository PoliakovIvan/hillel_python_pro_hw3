class Url:
    def __init__(
        self, scheme="", authority="", path="", query=dict, fragment="", **kwargs
    ):
        self.scheme = scheme
        self.authority = authority
        self.path = "/".join(path)
        for key, value in kwargs.items():
            self.query += f"?{key}={value}" if key == "q" else f"&{key}={value}"
        self.query = query
        self.fragment = fragment

    def __call__(self, *args, **kwargs):
        pass

    def __getattr__(self, attr):
        print(f"{attr}")
        return self

    def __str__(self):
        if self.path == "" and self.query == "":
            return f"{self.scheme}://{self.authority}"
        elif self.path:
            return f"{self.scheme}://{self.authority}/{self.path}"
        elif self.query == {"q": "python", "result": "json"}:
            query = "&".join([f"{key}={value}" for key, value in self.query.items()])
            self.query = f"?{query}"
            return f"{self.scheme}://{self.authority}{self.path}{self.query}{self.fragment}"
        else:
            return f"{self.scheme}://{self.authority}"

    def __eq__(self, other):
        return str(self) == str(other)


class UrlCreator:
    def __init__(self, scheme, authority):
        self.scheme = scheme
        self.authority = authority
        self.path = []

    def __getattr__(self, attr):
        self.path.append(attr)
        return self

    def __call__(self, *args, **kwargs):
        if args:
            self.path = list(args)
        if kwargs:
            self.query = kwargs
        return self._create(**kwargs)

    def _create(self, **kwargs):
        url = f"{self.scheme}://{self.authority}/{'/'.join(self.path)}"
        if kwargs:
            query = "&".join(f"{k}={v}" for k, v in kwargs.items())
            url += f"?{query}"
        return url

    def __str__(self):
        return self._create()

    def __eq__(self, other):
        return str(self) == str(other)


class HttpsUrl(Url):
    def __init__(self, scheme="https", authority="", path="", query="", fragment=""):
        super().__init__(scheme, authority, path, query, fragment)


class GoogleUrl(Url):
    def __init__(self, scheme="https", authority="google.com", path="", query="", fragment=""):
        super().__init__(scheme, authority, path, query, fragment)


class WikiUrl(Url):
    def __init__(self, scheme="https", authority="wikipedia.org", path="", query="", fragment=""):
        super().__init__(scheme, authority, path, query, fragment)


# task3

assert GoogleUrl() == HttpsUrl(authority="google.com")
assert GoogleUrl() == Url(scheme="https", authority="google.com")
assert GoogleUrl() == "https://google.com"
assert WikiUrl() == str(Url(scheme="https", authority="wikipedia.org"))
assert WikiUrl(path=["wiki", "python"]) == "https://wikipedia.org/wiki/python"
assert (GoogleUrl(query={"q": "python", "result": "json"})
    == "https://google.com?q=python&result=json")

# task4

url_creator = UrlCreator(scheme="https", authority="docs.python.org")
assert url_creator.docs.v1.api.list == "https://docs.python.org/docs/v1/api/list"
url_creator = UrlCreator(scheme="https", authority="docs.python.org")
assert url_creator("api", "v1", "list") == "https://docs.python.org/api/v1/list"
url_creator = UrlCreator(scheme="https", authority="docs.python.org")
assert (url_creator("api", "v1", "list", q="my_list")
    == "https://docs.python.org/api/v1/list?q=my_list")

