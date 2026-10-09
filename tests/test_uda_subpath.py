"""Authenticated app mount regression with in-memory test database."""
def test_uda_and_lan_routes(client):
    local=client.get("/")
    assert local.status_code==200
    assert '<base href="/">' in local.get_data(as_text=True)
    headers={"X-Forwarded-Prefix":"/apps/xmas-list","X-Forwarded-Host":"tanyaanne.ddns.net","X-Forwarded-Proto":"https"}
    proxied=client.get("/",headers=headers)
    assert proxied.status_code==200
    html=proxied.get_data(as_text=True)
    assert '<base href="/apps/xmas-list/">' in html
    assert '/apps/xmas-list/static/css/style.css' in html
    assert '/apps/xmas-list/login' in html
