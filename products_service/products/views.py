from django.middleware.csrf import get_token
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .schema import schema
import json


def resolve(request):
    # if query in request
    if request.GET.get("query"):
        q = request.GET.get("query")
        # execute query
        queryset = schema.execute(q)
        if queryset.data:
            # response object
            response = JsonResponse(queryset.data)
            return response
    elif request.method == "POST":
        mutation = request.POST.get("mutation")
        print(mutation)
        # execute mutation
        queryset = schema.execute(mutation)
        response = JsonResponse(queryset.data, safe=False)
        return response

    # no found
    response = HttpResponse(request, get_token(request))
    response.status_code = 404
    return response













