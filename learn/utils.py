from urlparse import urlparse

def is_s3_url(url):
    return urlparse(url).scheme == 's3'
