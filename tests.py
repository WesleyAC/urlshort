import main
import json
import unittest

class MainTestCase(unittest.TestCase):
    def setUp(self):
        main.map_len = 0
        main.url_map = []
        self.app = main.app.test_client()

    def test_make_slug(self):
        slugs = []
        for i in range(0,10000):
            slugs.append(main.make_slug())
        assert len(set(slugs)) == len(slugs)

    def test_add_url(self):
        url = "http://example.com"
        rv = self.app.post("/urls", data={"url": url})
        assert len(main.url_map) == 1
        assert main.url_map[0]["url"] == url

    def test_find_item_by_type(self):
        items = []
        for i in range(0, 100):
            url = "http://example.com/{}".format(i)
            rv = self.app.post("/urls", data={"url": url})
            items.append(json.loads(rv.get_data()))
        for item in items:
            assert main.find_item_by("slug", item["slug"]) == item
            assert main.find_item_by("url", item["url"]) == item

    def test_list_urls(self):
        for i in range(0, 100):
            url = "http://example.com/{}".format(i)
            self.app.post("/urls", data={"url": url})
        rv = self.app.get("/urls")
        assert json.loads(rv.get_data()) == main.url_map

    def test_url_exists(self):
        for i in range(0, 100):
            url = "http://example.com/{}".format(i)
            self.app.post("/urls", data={"url": url})
        assert main.url_exists("http://example.com/42")
        assert not main.url_exists("http://example.com/666")

    def test_duplicate_urls(self):
        url = "http://example.com"
        for i in range(0, 100):
            self.app.post("/urls", data={"url": url})
        assert len(main.url_map) == 1

    def test_increment_views(self):
        self.app.post("/urls", data={"url": "http://google.com"})
        for i in range(0, 100):
            assert main.url_map[0]["views"] == i
            self.app.get("/r/{}".format(main.url_map[0]["slug"]))

    def test_url_add_error(self):
        rv = self.app.post("/urls", data={})
        assert rv.status_code == 500
        assert "Error" in str(rv.get_data())

    def test_get_url_info(self):
        url = "http://example.com"
        self.app.post("/urls", data={"url": url})
        rv = self.app.get("/urls/{}".format(main.url_map[0]["slug"]))
        assert json.loads(rv.get_data()) == main.url_map[0]

    def test_redirect(self):
        url = "http://example.com"
        self.app.post("/urls", data={"url": url})
        rv = self.app.get("/r/{}".format(main.url_map[0]["slug"]))
        assert rv.status_code == 301
        assert rv.headers["Location"] == url

if __name__ == "__main__":
    unittest.main()
