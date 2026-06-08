def test_confamnode_importable_from_package():
    from confamnode import ConfamNode
    assert ConfamNode is not None


def test_models_importable_from_package():
    from confamnode import models
    assert models is not None


def test_exceptions_importable_from_package():
    from confamnode import ConfamNodeError, ConfamAuthError, ConfamRateLimitError, ConfamModelError
    assert ConfamNodeError is not None
    assert ConfamAuthError is not None
    assert ConfamRateLimitError is not None
    assert ConfamModelError is not None


def test_version_is_defined():
    import confamnode
    assert hasattr(confamnode, "__version__")
    assert isinstance(confamnode.__version__, str)


def test_confamstream_importable_from_package():
    from confamnode import ConfamStream
    assert ConfamStream is not None