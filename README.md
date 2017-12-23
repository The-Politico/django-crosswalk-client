![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# django-crosswalk-client

See the docs for [django-crosswalk](http://django-crosswalk.readthedocs.io/en/latest/).

### Testing

Pip install `pytest` and `us`.

Requires a running, **clean** instance of django-crosswalk to test against.

To run tests, pass your token and the service address to your running instance to pytest:

```
$ pytest --token YOURTOKENHERE --service http://localhost:8000/api/
```
