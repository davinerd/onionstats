import datetime

def validate_daterange(drange):
    if len(drange) < 2:
        return False

    try:
        datetime.datetime.strptime(drange[0], '%m/%d/%Y')
        datetime.datetime.strptime(drange[1], '%m/%d/%Y')
    except ValueError:
        return False

    return True


def convert_date(d):
    # in mongodb we have dates in the YYYY-mm-dd format
    return datetime.datetime.strptime(d, '%m/%d/%Y').strftime('%Y-%m-%d')


def validate_query(query):
    # no free search terms allowed
    if len(query.split(':')) < 2:
        return False

    for q in query.split():
        term = q.split(':')
        if len(term) == 1 and term[0].lower() in ["or", "and"]:
            # not allowed for now
            return False
        # to avoid queries like 'term field:term'
        elif len(term) == 1:
            return False

        # do not accept any special chars - only numbers and letters!
        if not term[0].isalnum() or not term[1].isalnum():
            return False

    return True


# we want to ensure that in the field are present only letters
def check_extras(extra_param):
    extra_array = extra_param.split(',')
    for param in extra_array:
        if not param.isalpha():
            return False

    return True


def extract_ipv4(node):
    dir_address = None
    if 'dir_address' in node and node['dir_address'] is not None:
        dir_address = node['dir_address'].split(':')[0]

    # the first value is the ipv4 while the second is ipv6
    or_address = node['or_addresses'][0].split(':')[0]

    if dir_address is None:
        return or_address

    if dir_address != or_address:
        print "dir_address != or_address..is it even possible?"
        print "dir_address: {0}".format(dir_address)
        print "or_address: {0}".format(or_address)

    # in my test, or_address is never null
    return or_address


def calculate_bandwidth(node, bandwidth_type):
    unit = "MB/s"
    # bandwidth_rate
    index = 0

    if bandwidth_type == "bandwidth_burst":
        index = 1
    elif bandwidth_type == "observed_bandwidth":
        index = 2
    elif bandwidth_type == "advertised_bandwidth":
        index = 3

    # bridges don't have the 'bandwidth' key
    if 'bandwidth' not in node:
        bandwidth = node['advertised_bandwidth'] / 1024
    else:
        bandwidth = node['bandwidth'][index] / 1024

    if bandwidth < 1024:
        unit = "KB/s"
    else:
        bandwidth /= 1024

    return "{0} {1}".format(bandwidth, unit)