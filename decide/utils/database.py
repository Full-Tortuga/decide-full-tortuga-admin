from django.db import connection
from rest_framework.response import Response
from rest_framework.status import *


def bulk_delete(ids, table):
    ids = [i for i in ids.split(",") if str.isdigit(i)]
    if len(ids) > 0:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM ' + table + ' WHERE id IN (%s)' % ', '.join(ids))
        return Response({}, status=HTTP_200_OK)
    else:
        return Response({'Error': 'El formato de la lista de ids no es correcto'}, status=HTTP_400_BAD_REQUEST)
