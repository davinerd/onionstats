from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
import settings as ts
import utils
from engines.es import ES
from tornado import gen, escape
import traceback



class BaseHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.render("error.html", status_code=status_code)


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("index.html")


class APIBaseHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'text/json')
        self.finish({'code': 1, 'result': [], 'message': self._reason})


class APIHandler(APIBaseHandler):
    @gen.coroutine
    def post(self, node_type):
        ret = {'code': 0, 'result': [], 'message': ''}
        es_index = "relays"
        columns = ts.RELAY_FIELDS
        extras = dict()

        if 'bridges' not in node_type and 'relays' not in node_type:
            ret['code'] = 1
            ret['message'] = "Invalid node type"
            self.write(ret)
            return

        try:
            body_data = escape.json_decode(self.request.body)
        except Exception:
            body_data = None

        if body_data:
            time_type = body_data['vtime']
        else:
            time_type = self.get_argument('vtime', None)

        if time_type is None:
            time_type = "first_seen"
        elif time_type not in ["first_seen", "last_seen", "last_restarted"]:
            ret['code'] = 1
            ret['message'] = "Invalid time type"
            self.write(ret)
            return

        if body_data:
            daterange = body_data['time']
            query = body_data['query']
        else:
            daterange = self.get_argument('time', None)
            query = self.get_argument('query', None)

        if not daterange:
            ret['code'] = 1
            ret['message'] = "Invalid POST data"
            self.write(ret)
            return

        # the date is in format m/d/yyyy - m/d/yyyy
        daterange = "".join(daterange.split())
        daterange = daterange.split('-')
        if not utils.validate_daterange(daterange):
            ret['code'] = 1
            ret['message'] = "Invalid time range"
            self.write(ret)
            return

        daterange[0] = utils.convert_date(daterange[0])
        daterange[1] = utils.convert_date(daterange[1])

        extras['time'] = {'type': time_type, 'range': daterange}

        if query and not utils.validate_query(query):
            ret['code'] = 1
            ret['message'] = "Invalid query"
            self.write(ret)
            return

        if body_data:
            country = body_data['country']
            flags = body_data['flags']
        else:
            country = self.get_argument('country', None)
            flags = self.get_argument('flags', None)

        if country is not None and country.strip():
            # sanitize input to avoid weird values
            if utils.check_extras(country):
                extras['country'] = country

        if flags is not None and flags.strip():
            # sanitize input to avoid weird values
            if utils.check_extras(flags):
                extras['flags'] = flags

        if node_type == "bridges":
            es_index = "bridges"
            columns = ts.BRIDGE_FIELDS

        try:
            results = yield self.application.es_instance.search(es_index, query, extras)
        except Exception as e:
            print traceback.format_exc()
            ret['code'] = 1
            ret['message'] = "Invalid query"
            self.write(ret)
            return

        for entry in results:
            entry['ip_address'] = utils.extract_ipv4(entry)
            entry['bandwidth'] = utils.calculate_bandwidth(entry, "advertised_bandwidth")

        ret['result'] = {"data": results, "columns": columns}
        self.write(ret)


class SyntaxHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("syntax.html")


class HelpHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("help.html")


class ErrorHandler(BaseHandler):
    pass


class Application(Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/api/(\w+)/nodes", APIHandler),
            (r"/syntax", SyntaxHandler),
            (r"/help", HelpHandler),
            (r"/(.*)", ErrorHandler)
        ]
        settings = {
            "template_path": ts.TEMPLATE_PATH,
            "static_path": ts.STATIC_PATH,
            "debug": ts.DEBUG
        }
        super(Application, self).__init__(handlers, **settings)

        # just in case elasticsearch is not reachable
        try:
            self.es_instance = ES()
        except Exception as e:
            print traceback.format_exc()
            exit(1)


if __name__ == '__main__':
    app = Application()
    app.listen(ts.LISTENING_PORT)
    print "OnionStats listening on {0}".format(ts.LISTENING_PORT)
    IOLoop.current().start()
