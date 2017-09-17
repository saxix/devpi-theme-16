import re


def compareable_text(text):
    return re.sub('\s+', ' ', text.strip())


def test_importable():
    import devpi_theme_16
    assert devpi_theme_16


def test_pkgresources_version_matches_init():
    import devpi_theme_16
    import pkg_resources
    ver = devpi_theme_16.__version__
    assert pkg_resources.get_distribution("devpi_theme_16").version == ver
