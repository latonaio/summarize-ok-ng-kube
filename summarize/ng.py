#!/usr/bin/env python3

from datetime import datetime, timedelta

from aion.logger import lprint

from .db import SummrizeCollection
from .util import read_config_json

DB_NAME = "SewingMachine"
DB_COLLECTION = "WorkObjectDetection"

# work NG 検出時間
# WORK_NG_TIME = 0.5
# debug
WORK_NG_TIME = 0.01


class SummarizeNgService():
    WORK_NG = 1
    GROOVE_NG = 2
    STICH_NG = 3

    def __init__(self, json_path):
        self.commands = read_config_json(json_path)

    def work_ng(self):
        """
        同一セッションにて、workが連続 x[s]見つからない場合を検知する
        """
        works = self.get_work_detection_result()
        if not works:
            lprint("no work detection result")
            return False

        works.sort(key=lambda x: x['timestamp'])
        total = None
        for pre_work, next_work in zip(works, works[1:]):
            if not pre_work.get('is_work') and not next_work.get('is_work'):
                pre_t = datetime.strptime(
                    pre_work.get('timestamp'), "%Y%m%d%H%M%S%f")
                next_t = datetime.strptime(
                    next_work.get('timestamp'), "%Y%m%d%H%M%S%f")
                diff_t = next_t - pre_t

                if total:
                    total += diff_t
                else:
                    total = diff_t
                if total and total >= timedelta(seconds=WORK_NG_TIME):
                    lprint(f"work was not found for {str(total)}")
                    return True
            else:
                total = None

        return False

    def groove_ng(self):
        pass

    def stitch_ng(self):
        pass

    def scan_ng(self):
        pass

    def get_session(self):
        with SummrizeCollection(DB_NAME, DB_COLLECTION) as db:
            session_id = db.find_one_latest_session_id()
            if session_id is None:
                lprint("not found session id")
                return None

        return session_id

    def get_work_detection_result(self):
        # get results from latest session id

        works = []
        with SummrizeCollection(DB_NAME, DB_COLLECTION) as db:
            session_id = db.find_one_latest_session_id()
            if session_id is None:
                lprint("not found session id")
                return None

            cur = db.find_equals_session_id(session_id)

            works = list(map(lambda x: {"timestamp": x.get('timestamp'),
                                        "is_work": x.get('is_work')}, cur))
        return works

    def output_json(self, conn, _type):
        if _type != self.WORK_NG:
            return

        conn.output_kanban(
            metadata={"write_command": self.commands['work_ng']},
        )
