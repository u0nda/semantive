from werkzeug.contrib.cache import SimpleCache

c = SimpleCache()


def status_pending():
    c.set('status', 'recent task still pending')


def status_completed():
    c.set('status', 'recent task completed')
