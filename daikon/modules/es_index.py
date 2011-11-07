import requests
import anyjson
import sys


def index_create(host, port, indexname, shards, replicas):
    data_request = json.dumps({"settings" : { "number_of_shards" : shards,
        "number_of_replicas" : replicas } }, sort_keys=True, indent=4)

    try:
        request = requests.post('http://' + host + ':' + port + '/' +
                indexname, data=data_request)
        if request.error is not None:
            print 'ERROR: Creating Index : "' + indexname + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Creating Index : "' + indexname + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Creating Index : "' + indexname + '"'


def index_delete(host, port, indexname):
    try:
        request = requests.delete('http://' + host + ':' + port + '/' + indexname)
        if request.error is not None:
            print 'ERROR: Deleteing Index : "' + indexname + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Deleting Index : "' + indexname + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Deleting Index : "' + indexname + '"'


def index_list(host, port, extended):
    try:
        request = requests.get('http://' + host + ':' + port +
                '/_cluster/health?level=indices')
        if request.error is not None:
            print 'ERROR: Listing Indexes :', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR:  Listing Indexes -', e
        sys.exit(1)
    else:
        data_result = json.loads(request.content)[u'indices']
        print 'SUCCESS: Listing Indexes'
        for index in data_result:
            print '\t Name:', index
            if extended:
                print '\t\t Status:', data_result[index][u'status']
                print '\t\t Number Of Shards:', data_result[index][u'number_of_shards']
                print '\t\t Number Of Replicas:', data_result[index][u'number_of_replicas']


def index_open(host, port, indexname):
    try:
        request = requests.post('http://' + host + ':' + port + '/' +
                indexname + '/_open')
        if request.error is not None:
            print 'ERROR: Opening Index : "' + indexname + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Opening Index : "' + indexname + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Opening Index : "' + indexname + '"'


def index_close(host, port, indexname):
    try:
        request = requests.post('http://' + host + ':' + port + '/' +
                indexname + '/_close')
        if request.error is not None:
            print 'ERROR: Closing Index : "' + indexname + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Closing Index : "' + indexname + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Closing Index : "' + indexname + '"'


def index_status(host, port, indexname, extended):
    try:
        request = requests.get('http://' + host + ':' + port + '/' +
                indexname + '/_status')
        if request.error is not None:
            print 'ERROR: Fetching Index Status : "' + indexname + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Fetching Index Status : "' + indexname + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Fetching Index Status : "' + indexname + '"\n'
        data_result = json.loads(request.content)

        print '\t Size Status:'
        print '\t\t Primary Size:', data_result[u'indices'][indexname][u'index'][u'primary_size']
        if extended:
            print '\t\t Total Size:', data_result[u'indices'][indexname][u'index'][u'size']

        print '\t Document Status:'
        print '\t\t Number Of Docs (Current):', data_result[u'indices'][indexname][u'docs'][u'num_docs']
        if extended:
            print '\t\t Number Of Docs (Max):', data_result[u'indices'][indexname][u'docs'][u'max_doc']
            print '\t\t Number Of Docs (Deleted):', data_result[u'indices'][indexname][u'docs'][u'deleted_docs']

        print '\t Merge Status:'
        print '\t\t Total Merges:', data_result[u'indices'][indexname][u'merges'][u'total']
        if extended:
            print '\t\t Current Merges:', data_result[u'indices'][indexname][u'merges'][u'current']

        if extended:
            print '\n\t Shard Status:'
            for shard in data_result[u'indices'][indexname][u'shards']:
                print '\n\t\t Number:', shard

                data_shard = data_result[u'indices'][indexname][u'shards'][shard][0]
                print '\t\t\t State:', data_shard[u'routing'][u'state']
                print '\t\t\t Size:', data_shard[u'index'][u'size']
                print '\t\t\t Number Of Docs (Current):', data_shard[u'docs'][u'num_docs']
                print '\t\t\t Number Of Docs (Max):', data_shard[u'docs'][u'max_doc']
                print '\t\t\t Number Of Docs (Deleted):', data_shard[u'docs'][u'deleted_docs']