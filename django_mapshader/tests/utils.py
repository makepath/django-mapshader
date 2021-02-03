from urllib import parse


def serparete_query_params(url):
    url_parsed = parse.urlsplit(url)
    return url_parsed.path, dict(parse.parse_qs(url_parsed.query))
