import settings
from tornadoes import ESConnection
from tornado.httpclient import AsyncHTTPClient
from tornado import gen, escape

AsyncHTTPClient.configure(None, max_clients=settings.ASYNC_HTTP_MAX_CLIENT)


class ES:
    url = None
    index = None
    es = None

    def __init__(self, index=settings.DB_NAME):
        self.es = ESConnection()
        self.es.httprequest_kwargs['headers'] = {'Connection': 'keep-alive'}
        self.index = index

    @gen.coroutine
    def search(self, mapping, query, extra_params):
        fields = settings.RELAY_ES_FIELDS
        return_data = list()

        if query:
            query = " AND ".join(query.split())
        else:
            query = "*"

        time_q = extra_params['time']
        query += self.__parse_extra(extra_params)

        if mapping == "bridges":
            fields = settings.BRIDGE_ES_FIELDS

        body_query = {"_source": fields,
                      "query": {
                          "filtered": {
                              "query": {
                                  "query_string": {
                                      "query": query
                                  }
                              },
                              "filter":{
                                  "range": {
                                      time_q['type']: {
                                          "gte": time_q['range'][0] + " 00:00:00",
                                          "lte": time_q['range'][1] + " 23:59:59"
                                      }
                                  }
                              }
                          }
                      }}

        if settings.DEBUG:
            print body_query

        result = yield self.es.search(index=self.index, type=mapping, source=body_query, size=settings.ES_RESULT_SIZE)
        result = escape.json_decode(result.body)

        if 'hits' in result and 'hits' in result['hits']:
            for hit in result['hits']['hits']:
                return_data.append(hit['_source'])
        else:
            raise Exception(result['error'])

        raise gen.Return(return_data)

    def __parse_extra(self, extra):
        query = ""

        if 'country' in extra:
            new_country = list()
            geo_split = extra['country'].split(',')
            for geo in geo_split:
                new_country.append("geo:" + geo)

            query = "{0} AND (".format(query) + " OR ".join(new_country) + ")"

        if 'flags' in extra:
            flags_split = extra['flags'].split(',')
            for flag in flags_split:
                query = "{0} AND flags:{1}".format(query, flag.title())

        return query
