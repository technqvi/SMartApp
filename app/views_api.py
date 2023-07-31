from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from django.db import connection
import pandas as pd


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'Overview API': '/',
        'List Compoany': '/company',
        'List Site Grade': '/site_grade',

    }

    return Response(api_urls)


@api_view(['GET'])
def list_company_by_sitemanger(request):

    # get site_manager_id  from request.user.id
    with connection.cursor() as cursor:
        sql = """
        select id,company_name from app_company where is_customer='true'
        """

        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        companyList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        df = pd.DataFrame(data=companyList)
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_dict.html
    if df.empty == False:

        data = df.to_dict()
        data=df.to_dict('records')
        #data = df.to_dict('dict')
        #data=df.to_dict('series')
        # data = df.to_dict('index')

        return Response(data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

