#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import logging
import time
from datetime import datetime

import requests
from lxml import etree
from requests import RequestException


class Coze():
    def __init__(self, conf: dict) -> None:
        self.api_key = conf.get("api_key")
        self.api_url = conf.get("api_url", "")
        self.LOG = logging.getLogger("Coze")

    @staticmethod
    def value_check(conf: dict) -> bool:
        if conf:
            if conf.get("api_key") and conf.get("api_url"):
                return True
        return False

    def get_answer(self, question: str, wxid: str) -> str:
        if not question.strip():
            raise ValueError("输入文本不能为空")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": {"text": question},
            "response_mode": "blocking",
            "user": ""
        }

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            print(data)
            return data.get('data', {}).get('outputs', {}).get('content')

        except RequestException as e:
            self.LOG.error(f"Coze API 返回了错误：{str(e)}")
            return f"Coze API 返回了错误：{str(e)}"


if __name__ == "__main__":
    from configuration import Config

    config = Config().COZE
    if not config:
        exit(0)

    chat = Coze(config)

    while True:
        q = input(">>> ")
        try:
            time_start = datetime.now()
            print(chat.get_answer(q, "wxid"))
            time_end = datetime.now()
            print(f"{round((time_end - time_start).total_seconds(), 2)}s")
        except Exception as e:
            print(e)
