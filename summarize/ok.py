#!/usr/bin/env python3

from .util import read_config_json

# work NG 検出時間
WORK_NG_TIME = 0.5


class SummarizeOkService():
    WORK_OK = 1
    GROOVE_OK = 2
    STICH_OK = 3

    def __init__(self, json_path):
        self.commands = read_config_json(json_path)

    def work_ok(self):
        pass

    def groove_ok(self):
        pass

    def stitch_ok(self):
        pass

    def scan_ok(self):
        pass

    def output_json(self, conn, _type):
        if _type != self.WORK_OK:
            return

        conn.output_kanban(
            metadata={"write_command": self.commands['work_ok']},
        )
