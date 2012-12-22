from django.db.models import Q
from django.http import HttpResponse
from django.utils import simplejson as json
from django.core import serializers
import datetime
from django.utils.dateparse import parse_datetime
from django.shortcuts import render_to_response
from art.models import Item
import datetime

def getItems(request):
    response_status = 200
    coll_id = request.GET.get('collection_id')
    user_id = request.GET.get('user_id')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    featured = request.GET.get('featured')
    name = request.GET.get('name')
    created_date_str = request.GET.get('created_date')
    if coll_id or user_id or (lat and lon) or featured or name or created_date_str:
        qset = Q()
        if coll_id:
            qset &= Q(collection__id__exact=coll_id)
        if user_id:
            qset &= Q(user__id__exact=user_id)
        if lat:
            qset &= Q(lat__exact=lat)
            qset &= Q(lon__exact=lon)
        if featured:
            qset &= Q(featured__iexact=featured)
        if name:
            qset &= Q(name__icontains=name)
        if created_date_str:
            created_date = parse_datetime(created_date_str)
            qset &= Q(created_date__year=created_date.year)
            qset &= Q(created_date__month=created_date.month)
            qset &= Q(created_date__day=created_date.day)
        items = Item.objects.filter(qset).select_related()
        response = []
        for item in items:
            itemJson = {
                'id'             : item.id,
                'collection_id'  : item.collection.id,
                'lat'            : item.lat,
                'lon'            : item.lon,
                'user_id'        : item.user.id,
                'featured'       : item.featured,
                'name'           : item.name,
                'caption'        : item.caption,
                'description'    : item.description,
                'created_date'   : str(item.created_date)
                }
            qset = Q(item__id=item.id)
            itemTags = Item_Tag.objects.filter(qset).select_related()
            tagsJson = []
            for itemTag in itemTags:
                tagsJson.append({
                        'tag_id' : itemTag.tag.id,
                        'text'   : itemTag.tag.text
                        })
            itemJson['tags'] = tagsJson
            response.append(itemJson)
    else:
        response = {
            'problem' : 'No parameters specified',
            'details' : ''
            }
        response_status = 400
    return HttpResponse(json.dumps(response), mimetype="application/json", status=response_status)

def getItem(request):
    response_status = 200
    item_id = request.GET.get('id')
    if item_id:
        qset = Q(id__exact=item_id)
        items = Item.objects.filter(qset).select_related()
        if not items:
            response = []
        else:
            item = items[0]
            itemJson = {
                'id'             : item.id,
                'collection_id'  : item.collection.id,
                'lat'            : item.lat,
                'lon'            : item.lon,
                'user_id'        : item.user.id,
                'featured'       : item.featured,
                'name'           : item.name,
                'caption'        : item.caption,
                'description'    : item.description,
                'created_date'   : str(item.created_date)
                }
            qset = Q(item__id=item.id)
            itemTags = Item_Tag.objects.filter(qset).select_related()
            tagsJson = []
            for itemTag in itemTags:
                tagsJson.append({
                        'tag_id' : itemTag.tag.id,
                        'text'   : itemTag.tag.text
                        })
            itemJson['tags'] = tagsJson
            response = itemJson
    else:
        response = {
            'problem' : 'No id specified',
            'details' : ''
            }
        response_status = 400
    return HttpResponse(json.dumps(response), mimetype="application/json", status=response_status)