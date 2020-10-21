from .const import (STOP_SERVICE)


def stop_work_detection(conn):
    conn.output_kanban(
        metadata={
            "type": "terminate",
            "name": STOP_SERVICE
        },
    )
