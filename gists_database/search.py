from .models import Gist

def comparison(operator):
    return {
        'lt': '<',
        'lte': '<=',
        'gt': '>',
        'gte': '>=',
    }[operator]

def search_gists(db_connection, **kwargs):
    
#     if 'github_id' in kwargs:
#         cursor = db_connection.execute('SELECT * FROM gists WHERE github_id = :github_id', kwargs)
#         return [Gist(gist) for gist in cursor]
# #         return cursor.fetchall()
#     if 'created_at' in kwargs:
#         cursor = db_connection.execute('SELECT * FROM gists WHERE datetime(created_at) == datetime(:created_at)', kwargs)
#         return [Gist(gist) for gist in cursor]
# #         return cursor.fetchall()
#     else:
#         cursor = db_connection.execute('SELECT * FROM gists')
#         return cursor.fetchall()

    query = 'SELECT * FROM gists'
    params = {}
    if kwargs:
        filters = []
        for param, value in kwargs.items():
            if param.startswith(('created_at', 'updated_at')):
                if '__' in param:
                    attribute, operator = param.split('__')
                    oper = comparison(operator)
                    filters.append('datetime({}) {} datetime(:{})'.format(attribute, oper, param))
                
                else:
                    attribute = param
                    filters.append('datetime({}) == datetime(:{})'.format(attribute, param))
                params[param] = value

            else:
                filters.append('%s = :%s' % (param, param))
                params[param] = value

        query += ' WHERE '
        query += ' AND '.join(filters)
        cursor = db_connection.execute(query, params)
    else:
        cursor = db_connection.execute(query)

    results = [Gist(gist) for gist in cursor]
    return results 