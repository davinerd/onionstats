import motor
import settings as ts
from tornado import gen
from pymongo.errors import BulkWriteError



@gen.coroutine
def insert_bridges(bridges):
    coll_bridges = ts.db[ts.COLL_BRIDGES]
    bulk = coll_bridges.initialize_unordered_bulk_op()

    for bridge in bridges:
        bulk.insert(bridge)

    try:
        yield bulk.execute()
    except BulkWriteError as err:
        print err.details


@gen.coroutine
def insert_relays(relays):
    coll_relays = ts.db[ts.COLL_RELAYS]
    bulk = coll_relays.initialize_unordered_bulk_op()

    for relay in relays:
        bulk.insert(relay)

    try:
        yield bulk.execute()
    except BulkWriteError as err:
        print err.details
