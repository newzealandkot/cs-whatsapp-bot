from http import HTTPMethod

import pytest
import pytest_httpserver as server


HTTPSERVER_HOST_PORT = ("localhost", 4000)


@pytest.fixture(scope="session")
def httpserver_listen_address():
    return HTTPSERVER_HOST_PORT


@pytest.fixture
def remote_uri():
    return "/remote"


@pytest.fixture
def test_server(httpserver, remote_uri):
    httpserver.expect_request(
        remote_uri,
        method=HTTPMethod.POST,
    ).respond_with_json({})
    yield httpserver.host, httpserver.port
    httpserver.assert_request_made(
        server.RequestMatcher(remote_uri, method=HTTPMethod.POST)
    )
