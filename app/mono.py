import os
import requests

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from sqlitedict import SqliteDict


class MonoHandler:

    def __init__(self):
        self.__token = os.getenv("TOKEN")
        self.__account = os.getenv("ACCOUNT")

        self.start_date = datetime(day=1, month=9, year=2022)
        self.api_url = "https://api.monobank.ua"

    def __get_transactions(self):
        """Get list of all transaction for last month days.\

        Transaction structure:
        {
        "id": "2KLTHz_RiCxjzxDaxrpXDsrocpsKddpo19JlRGAjeA",
        "time": 1662206225,
        "description": "",
        "comment": "Тест 5",
        "mcc": 4829,
        "originalMcc": 4829,
        "amount": 100,
        "operationAmount": 100,
        "currencyCode": 980,
        "commissionRate": 0,
        "cashbackAmount": 0,
        "balance": 2900,
        "hold": false
        }
        """

        today = datetime.now()
        if today.month != self.start_date.month:
            self.start_date = datetime(day=1, month=today.month, year=today.year)

        end_date = self.start_date + relativedelta(months=1)
        epoch_start_date = int(time.mktime(self.start_date.timetuple()))
        epoch_end_date = int(time.mktime(end_date.timetuple()))
        response = requests.get(
            f"{self.api_url}/personal/statement/{self.__account}/{epoch_start_date}/{epoch_end_date}",
            headers={"X-Token": self.__token}
        )
        return response.json()

    def get_last_transactions(self):
        """Get last 5 transactions."""

        return self.__get_transactions()[:5]

    def get_best_donate(self):
        """Get best donate."""

        storage = SqliteDict('db.sqlite', autocommit=True)
        current_best_donate = storage.get("best_donate", 0)

        transactions = self.__get_transactions()

        for transaction in transactions:
            amount = transaction["amount"]

            if amount > current_best_donate:
                current_best_donate = amount

        storage["best_donate"] = current_best_donate
        storage.close()

        return current_best_donate
