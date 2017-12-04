import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--token",
        action="store",
        default="testtoken",
        help="Crosswalk API token"
    )

    parser.addoption(
        "--service",
        action="store",
        default="http://localhost:8000/api/",
        help="Crosswalk API service location"
    )


@pytest.fixture
def token(request):
    return request.config.getoption("--token")


@pytest.fixture
def service(request):
    return request.config.getoption("--service")
