from tornado import gen
from engines.onion import OnionGetter
from engines import db
from tornado.ioloop import IOLoop

nodes = None


def get_torz():
    global  nodes
    print "gettorz"
    mn = OnionGetter()
    nodes = mn.get_nodes()




@gen.coroutine
def insert_relays():
    print "insert rel"
    yield db.insert_relays(nodes['relays'])



@gen.coroutine
def insert_bridges():
    print "insert br"
    yield db.insert_bridges(nodes['bridges'])



def main():
    get_torz()
    IOLoop.current().run_sync(insert_bridges)
    IOLoop.current().run_sync(insert_relays)


main()


