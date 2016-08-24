import pytest

@pytest.fixture(autouse=True)
def py2or3(cov):
    """Ignore code pathways specific to other Python versions."""
    if cov is None or py2or3.once:
        return
    import six
    exclude_re = r'(?i)#\s*pragma[:\s]?\s*py{}\s+only'.format(2 if six.PY3 else 3)
    cov.exclude(exclude_re)
    py2or3.once = True
py2or3.once = False
