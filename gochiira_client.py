import requests


class GochiiraClient():
    def __init__(self, token, endpoint):
        self.endpoint = endpoint
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    def getRankings(self):
        return requests.get(
            f"{self.endpoint}/ranking/monthly/likes",
            headers=self.headers
        ).json()

    def getTagList(self, page=1, sort="c", order="d"):
        return requests.get(
            f"{self.endpoint}/catalog/tags",
            params={"page": page, "sort": sort, "order": order},
            headers=self.headers
        ).json()

    def getCharacterList(self, page=1, sort="c", order="d"):
        return requests.get(
            f"{self.endpoint}/catalog/characters",
            params={"page": page, "sort": sort, "order": order},
            headers=self.headers
        ).json()