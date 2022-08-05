from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.conf import settings
from rest_framework.decorators import action
import json
import requests
# Create your views here.
class MicrocourseViewSet(viewsets.ModelViewSet):
	
	queryset = ''
	serializer_class = ''

	def getData(self):
		f = open(f'{settings.STATICFILES_DIRS[0]}/ACUE-microcourselist.json')
		return json.load(f)

	@action(methods=['get'], detail=False, url_path='list', url_name='MicrocourseViewSet.getlist')	
	def get_list(self, request):
		try:
			response = self.getData()
			message = ''
			return Response(
				{
					'status':'success', 
					'message': message,
					'data': response
				},
				status = status.HTTP_200_OK)
		except Exception as e:
			message = 'Errors occurred while processing the request'
			return Response(
				{
					'status':'error', 
					'message': message,
					'data': []
				},
				status = status.HTTP_400_BAD_REQUEST)
