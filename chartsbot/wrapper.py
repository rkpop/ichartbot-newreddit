import prawcore
from simplejson import dumps


class PrawcoreWrapper:
    def __init__(self, details):
        self.authenticator = prawcore.TrustedAuthenticator(
            prawcore.Requestor("chartsbot 0.1.0 /u/jonicrecis"),
            client_id=details["client_id"],
            client_secret=details["client_secret"],
        )
        self.authorizer = prawcore.ScriptAuthorizer(
            self.authenticator, details["username"], details["password"]
        )
        self.authorizer.refresh()

    def make_call(self, url, method="GET", payload=None):
        if not self._check_validity():
            self.authorizer.refresh()
        with prawcore.session(self.authorizer) as session:
            retval = session.request(method, url, json=payload)
        return retval

    def _check_validity(self):
        return self.authorizer.is_valid()


class WidgetWrapper(PrawcoreWrapper):
    def __init__(self, details):
        super().__init__(details)
        self._widget_id = None
        self._get_widget_to_update()

    def _get_widget_to_update(self):
        payload = self.make_call("/r/kpop/api/widgets")
        for item in payload["items"]:
            if (
                "shortName" in payload["items"][item]
                and "iChart" in payload["items"][item]["shortName"]
            ):
                self._widget_id = payload["items"][item]["id"]

    def make_update(self, table):
        payload = dumps(
            {
                "text": table,
                "kind": "custom",
                "shortName": "Realtime iChart",
                "css": "body {}",
                "imageData": [],
                "styles": {"backgroundColor": None, "headerColor": None},
                "height": 500,
            }
        )
        self.make_call(
            "/r/kpop/api/widget/" + self._widget_id,
            method="PUT",
            payload=payload,
        )
