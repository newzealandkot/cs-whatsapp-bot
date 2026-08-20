def test_whatsapp_cloud_api_is_installed() -> None:
    try:
        import whatsapp_cloud_api
    except ModuleNotFoundError:
        assert False
    assert whatsapp_cloud_api is not None
