# -*- coding: utf-8 -*-

import json

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import status


from quizy.models import Page, Variant
from quizy.serializers import (PageSerializer, VariantSerializer)


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    model = Page
    lookup_field = 'id'
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    queryset = Page.objects.all()

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        if not pk:
            res = {"code": 400, "message": "Bad Requset"}
            return Response(json.dumps(res), status=status.HTTP_200_OK)

        if request.method == "PUT":
            req = json.loads(request.body.decode("utf-8"))
            is_dirty = False
            text = req.get("text")
            type = req.get("type")
            number = req.get("number")
            page = Page.objects.get(pk=pk)
            if page.text != text:
                page.text = text
                is_dirty = True
            if page.type != type:
                page.type = type
                is_dirty = True
            if page.number != number:
                page.number = number
                is_dirty = True
            if is_dirty is True:
                page.save()

            raw_variants = req.get("variants", [])
            for v in raw_variants:
                is_dirty = False
                text = v.get("text")
                reflexy = v.get("reflexy")
                raw_right_answer = v.get("right_answer")
                right_answer = False
                if raw_right_answer:
                    if raw_right_answer is True or raw_right_answer == "true":
                        right_answer = True
                    else:
                        right_answer = False

                raw_pair_object = v.get("pair_object")
                if raw_pair_object:
                    pair_id = raw_pair_object.get("id")
                    pair_text = raw_pair_object.get("text")
                    if pair_id:
                        variant_pair = page.variants.get(pk=pair_id)
                        if variant_pair.text != pair_text:
                            variant_pair.text = pair_text
                            variant_pair.save()

                id = v.get("id")
                if id:
                    variant = page.variants.get(pk=id)
                    if variant.text != text:
                        variant.text = text
                        is_dirty = True
                    if variant.reflexy != reflexy:
                        variant.reflexy = reflexy
                        is_dirty = True
                    if variant.right_answer != right_answer:
                        variant.right_answer = right_answer
                        is_dirty = True
                    if is_dirty is True:
                        variant.save()

        serializer = PageSerializer(instance=page)
        return Response(serializer.data)

    def create(self, request):
        if request.method == "POST":
            if request.body:
                req = json.loads(request.body.decode("utf-8"))

                if type(req) is dict:
                    text = req.get("text")
                    type_page = req.get("type")
                    number = req.get("number")
                    page = Page.objects.create(text=text, type=type_page, number=number)
                    raw_variants = req.get("variants", [])
                    for v in raw_variants:
                        text = v.get("text")
                        right_answer = v.get("right_answer")
                        page.variants.create(text=text, right_answer=right_answer)

                    serializer = PageSerializer(instance=page)
                    return Response(serializer.data)
                # сохраняем только номера
                if type(req) is list:
                    is_dirty = False
                    for q in req:
                        id = q.get('id')
                        if id:
                            page, created = Page.objects.get_or_create(pk=id)
                            if page.number != q.get('number'):
                                page.number = int(q.get('number'))
                                is_dirty = True
                            if is_dirty is True:
                                page.save()
                    return Response("OK", status=status.HTTP_200_OK)
            else:
                print "!!! create page"
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def new_variant(self, request, *args, **kwargs):
        page_id = kwargs.get('id')
        if not page_id:
            res = {"code": 400, "message": "Bad Requset"}
            return Response(json.dumps(res), status=status.HTTP_200_OK)

        page = Page.objects.get(pk=page_id)
        text = request.data.get("text")

        raw_right_answer = request.data.get("right_answer", False)
        if raw_right_answer == "true":
            right_answer = True
        else:
            right_answer = False

        pair_type = request.data.get("pair_type")

        variant = page.variants.create(text=text, right_answer=right_answer)
        if pair_type:
            variant.pair_type = pair_type
            variant.save()

        raw_pair = request.data.get("pair")
        if raw_pair:
            pair = page.variants.get(id=raw_pair)
            if not pair:
                res = {"code": 400, "message": "Incorrect variant id"}
                return Response(json.dumps(res), status=status.HTTP_400_BAD_REQUEST)
            variant.pair = pair
            variant.save()

        serializer = VariantSerializer(instance=variant)
        return Response(serializer.data)

    @detail_route(methods=['delete'], url_path='remove_variant/(?P<variant_id>\d+)')
    def remove_variant(self, request, *args, **kwargs):
        page_id = kwargs.get('id')
        variant_id = kwargs.get('variant_id')

        if not page_id:
            res = {"code": 400, "message": "Incorrect page id"}
            return Response(json.dumps(res), status=status.HTTP_400_BAD_REQUEST)

        if not variant_id:
            res = {"code": 400, "message": "Incorrect variant id"}
            return Response(json.dumps(res), status=status.HTTP_400_BAD_REQUEST)

        variant = Variant.objects.get(pk=variant_id)

        if str(variant.page.id) != str(page_id):
            res = {"code": 400, "message": "Incorrect page id"}
            return Response(json.dumps(res), status=status.HTTP_400_BAD_REQUEST)

        variant.delete()
        return Response("OK")
