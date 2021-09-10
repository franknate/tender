import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .serializers import TenderOnlySerializer
from .serializers import TenderSerializer
from .serializers import UnitSerializer
from .serializers import BidSerializer
from .serializers import BidRoundSerializer
from .models import Tender 
from .models import Unit 
from .models import BidRound 
from .models import Bid 
from .models import OurBid


class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser("admin", "admin@example.com", "admin")

    def test_valid_login(self):
        data = {"username": "admin", "password": "admin"}
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        data = {"username": "", "password": ""}
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TenderViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser("admin", "admin@example.com", "admin")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def post_tender(self):
        bid_file = open("docs/bid_file.xlsx", "rb")
        drops_file = open("docs/drops.xlsx", "rb")
        data = {"bid_file": bid_file, "drops_file": drops_file}
        return self.client.post("/api/tenders/", data)

    def test_list_tenders(self):
        response = self.client.get("/api/tenders/", {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_tenders_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/tenders/", {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_tender_valid(self):
        response = self.post_tender()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_create_tender_invalid(self):
        response = self.client.post("/api/tenders/", {})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_create_tender_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.post("/api/tenders/", {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_tender_valid(self):
        tender_id = self.post_tender().data["id"]
        response = self.client.get("/api/tenders/{}/".format(tender_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_tender_invalid(self):
        response = self.client.get("/api/tenders/-1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_tender_unauthorized(self):
        tender_id = self.post_tender().data["id"]
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/tenders/{}/".format(tender_id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_tender_valid(self):
        tender_id = self.post_tender().data["id"]
        round_file = open("docs/result_round1.xlsx", "rb")
        data = {"round_file": round_file, "tender_id": tender_id, "bid_round": 1}
        response = self.client.put("/api/tenders/{}/".format(tender_id), data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_update_tender_invalid_data(self):
        tender_id = self.post_tender().data["id"]
        response = self.client.put("/api/tenders/{}/".format(tender_id), {})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_update_tender_unauthorized(self):
        tender_id = self.post_tender().data["id"]
        self.client.force_authenticate(user=None)
        response = self.client.put("/api/tenders/{}/".format(tender_id), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_tender_valid(self):
        tender_id = self.post_tender().data["id"]
        response = self.client.delete("/api/tenders/{}/".format(tender_id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_tender_invalid(self):
        response = self.client.delete("/api/tenders/-1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_tender_unauthorized(self):
        tender_id = self.post_tender().data["id"]
        self.client.force_authenticate(user=None)
        response = self.client.delete("/api/tenders/{}/".format(tender_id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BidViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser("admin", "admin@example.com", "admin")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        bid_file = open("docs/bid_file.xlsx", "rb")
        drops_file = open("docs/drops.xlsx", "rb")
        data = {"bid_file": bid_file, "drops_file": drops_file}
        self.tender_id = self.client.post("/api/tenders/", data).data["id"]

    def test_get_bids_valid(self):
        response = self.client.get("/api/bid/{}/".format(self.tender_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_bids_invalid(self):
        response = self.client.get("/api/bid/-1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_bids_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/bid/{}/".format(self.tender_id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_bids_valid(self):
        bids = self.client.get("/api/bid/{}/".format(self.tender_id)).data
        response = self.client.post("/api/bid/{}/".format(self.tender_id), bids, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_bids_invalid(self):
        response = self.client.post("/api/bid/{}/".format(self.tender_id), {})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)     

    def test_post_bids_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.post("/api/bid/{}/".format(self.tender_id), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)                         
