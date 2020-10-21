#!/usr/bin/env python3

import os
import time

from aion.logger import lprint, initialize_logger
from aion.microservice import main_decorator, Options

import summarize

SERVICE_NAME = os.environ.get("SERVICE")
INTERVAL_TIME = 0.5
JSON_PATH = os.getcwd() + "/config/config.json"

initialize_logger(SERVICE_NAME)


@main_decorator(SERVICE_NAME)
def main(opt: Options):
    conn = opt.get_conn()
    num = opt.get_number()
    kanban = conn.set_kanban(SERVICE_NAME, num)

    # reset signal ng -> ok
    # essentially support on control-yaskawa-robot-w to reset signal, but it is a bit hard.
    # so adhoc support on summarize-ok-ng
    summary_ok_service = summarize.SummarizeOkService(JSON_PATH)
    summary_ok_service.output_json(conn, summary_ok_service.WORK_OK)

    summary_service = summarize.SummarizeNgService(JSON_PATH)
    work_ng_status = False
    session_id = session_id_old = summary_service.get_session()

    while True:
        try:
            session_id = summary_service.get_session()
            if session_id != session_id_old:
                lprint("[OK] found work detection")
                work_ng_status = None
                summary_ok_service = summarize.SummarizeOkService(JSON_PATH)
                summary_ok_service.output_json(
                    conn, summary_ok_service.WORK_OK)

            is_work_ng = summary_service.work_ng()
            if is_work_ng and is_work_ng != work_ng_status:
                lprint("[NG] work detection error")
                summarize.stop.stop_work_detection(conn)
                summary_service.output_json(conn, summary_service.WORK_NG)
                work_ng_status = is_work_ng

            session_id_old = session_id
            time.sleep(INTERVAL_TIME)

        except Exception as e:
            lprint(e)


if __name__ == "__main__":
    main()
