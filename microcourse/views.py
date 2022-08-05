from django.core.mail import EmailMessage
from ntpath import join
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.conf import settings
from rest_framework.decorators import action
import json
from datetime import datetime
import threading
import requests
# Create your views here.
class MicrocourseViewSet(viewsets.ModelViewSet):
	
	queryset = ''
	serializer_class = ''

	def getData(self):
		url = settings.URL_OBJECTS
		r = requests.get(url = url, headers={
			'Connection':'keep-alive',
			'Accept':'*/*',
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53"})
		if r.status_code == 200:
			response = r.json()
			return response
		else:
			f = open(f'{settings.STATICFILES_DIRS[0]}/ACUE-microcourselist.json')
			return json.load(f)
	
	def startAt(self,x):
		return x['start_at'] or datetime.min

	def endAt(self,x):
		return x['end_at'] or datetime.min

	@action(methods=['get'], detail=False, url_path='list', url_name='MicrocourseViewSet.getlist')	
	def get_list(self, request):
		try:
			order = self.request.query_params.get('order', None)
			descending = self.request.query_params.get('descending', None)
			response = self.getData()
			if order:
				for obj in response:
					obj['start_at'] = datetime.strptime(obj['start_at'],'%Y-%m-%dT%H:%M:%SZ') if obj['start_at'] != None else None
					obj['end_at'] = datetime.strptime(obj['end_at'],'%Y-%m-%dT%H:%M:%SZ') if obj['end_at'] != None else None
				descending = True if descending else False
				if order == 'start_at' or order == 'end_at':
					if order == 'start_at':
						response = sorted(response, key = self.startAt, reverse = descending)
					else:
						response = sorted(response, key = self.endAt, reverse = descending)
				else:
					response = sorted(response, key = lambda k: k[order], reverse = descending)
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

	@action(methods=['post'], detail=False, url_path='emailreport', url_name='MicrocourseViewSet.emailreport')	
	def emailreport(self, request):
		try:
			email = request.data['email'] if 'email' in request.data else None
			if email:
				data = self.getData()
				content = '''<style type="text/css">
					table, td, th {  
						border: 1px solid #ddd;
						text-align: left;
					}

					table {
						border-collapse: collapse;
						width: 100%;
					}

					th, td {
						padding: 15px;
					}
					</style>'''				
				content = content + '<h3>Available Microcourses list</h3><br/>'
				content= content + '<table style="border: 1px solid black;">'
				content = content + '<tr><th>ID</th><th>Name</th>' + \
					'<th>Course code</th>' + \
					'<th>Workflow state</th>' + \
					'<th>start date</th>' + \
					'<th>end date</th></tr>'
				for obj in data:
					if obj['workflow_state']=='available':						
						content = content + '<tr>'
						content = content + f'<td>{obj["id"]}</td>'
						content = content + f'<td>{obj["name"]}</td>'
						content = content + f'<td>{obj["course_code"]}</td>'
						content = content + f'<td>{obj["workflow_state"]}</td>'
						start_at = '' if obj["start_at"] == None else obj["start_at"]
						content = content + f'<td>{start_at}</td>'
						end_at = '' if obj["end_at"] == None else obj["end_at"]
						content = content + f'<td>{end_at}</td>'
						content = content + '</tr>'
				content = content + '</table>'
				ObjEmail = EmailMessage('Report Available courses', content, to=[email])
				ObjEmail.content_subtype = "html"

				sendEmail = threading.Thread(target = ObjEmail.send)
				sendEmail.start()
				return Response(
					{
						'status':'success', 
						'message': f'We have send a message to {email}',
						'data': []
					},
					status = status.HTTP_200_OK)
			else:
				return Response(
					{
						'status':'error', 
						'message': "data required didn't received",
						'data': []
					},
					status = status.HTTP_400_BAD_REQUEST)				

		except Exception as e:
			print(e)
			message = 'Errors occurred while processing the request'
			return Response(
				{
					'status':'error', 
					'message': message,
					'data': []
				},
				status = status.HTTP_400_BAD_REQUEST)