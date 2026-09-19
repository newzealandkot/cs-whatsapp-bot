import httpx2
import pytest
import pytest_httpserver as server

from src.cs_whatsapp_bot import HTTPX2Sender


@pytest.mark.anyio
async def test_httpx2sender_sends_correct_request_to_graph_api(
        access_token,
        base_url,
        expected_payload,
        phone_number_id,
        request_options,
        test_server,
):
    sender = HTTPX2Sender(phone_number_id=phone_number_id, access_token=access_token, base_url=base_url)
    await sender.send(expected_payload)
    test_server.assert_request_made(server.RequestMatcher(**request_options))


@pytest.mark.anyio
async def test_httpx2sender_increments_total_messages_on_success(
        access_token,
        base_url,
        expected_payload,
        phone_number_id,
        test_server,
):
    sender = HTTPX2Sender(phone_number_id=phone_number_id, access_token=access_token, base_url=base_url)
    await sender.send(expected_payload)
    assert sender.total_messages == 1


@pytest.mark.anyio
async def test_httpx2sender_raises_on_4xx_response(access_token, expected_payload, httpserver, phone_number_id):
    httpserver.expect_request(f"/{phone_number_id}/messages").respond_with_data("bad request", status=400)
    base_url = f"http://{httpserver.host}:{httpserver.port}"
    sender = HTTPX2Sender(phone_number_id=phone_number_id, access_token=access_token, base_url=base_url)
    with pytest.raises(httpx2.HTTPStatusError):
        await sender.send(expected_payload)
    assert sender.total_messages == 0


@pytest.mark.anyio
async def test_httpx2sender_raises_on_5xx_response(access_token, expected_payload, httpserver, phone_number_id):
    httpserver.expect_request(f"/{phone_number_id}/messages").respond_with_data("server error", status=500)
    base_url = f"http://{httpserver.host}:{httpserver.port}"
    sender = HTTPX2Sender(phone_number_id=phone_number_id, access_token=access_token, base_url=base_url)
    with pytest.raises(httpx2.HTTPStatusError):
        await sender.send(expected_payload)
    assert sender.total_messages == 0
