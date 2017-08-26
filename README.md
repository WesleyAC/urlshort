# URL Shortener

[![Travis CI Badge](https://api.travis-ci.org/WesleyAC/urlshort.svg?branch=master)](https://travis-ci.org/WesleyAC/urlshort)

This is a simple API to shorten URLs, written in Python and Flask.

Features:

* Adding URLs
* Redirects
* Short slugs (using an incrementing base36 number for each slug)
* Duplicate URLs share slugs

Non-features:

* Persistent storage
* User interface
