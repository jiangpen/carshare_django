from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader, Context
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from carshare.models import user_info
from carshare.models import travel_record
from carshare.models import au_suburb
from carshare.models import user_message

from django.db import models
from django.core.signing import Signer
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from carshare.mydecorator import logged_already
import logging
import math




#seattle = [47.621800, -122.350326]
#olympia = [47.041917, -122.893766]
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d
    

def get_base_url():
	return "127.0.0.1:8000"
	
	

def show_main_page(request, message=''):
	if request.session.get('member_id', False):
		passed=True
	else:
		passed=False
	allrec = travel_record.objects.order_by("created").reverse()[0:4]
	t = loader.get_template("index.html")
	c = Context({ 'passed': passed ,  'allrec': allrec, 'message': message })

	return t.render(c)

# Create your views here.
def test_view(request):
			allrec = travel_record.objects.order_by("created").reverse()[0:4]
			t = loader.get_template("index.html")
			c = Context({ 'showpage': 6 })
			return HttpResponse(t.render(c))
	
def index(request):
			myoutput=show_main_page(request)
			return HttpResponse(myoutput)

def query_fromto(request):
	if 'querylift' in request.GET:
		myfrom = request.GET['fromwhere']
		myto = request.GET['towhere']
		
		mysurround = request.GET.get('surround', False)

		mysurround = request.GET.get('flexibletime', False)
		from_position_lat=0
		from_position_long=0
		to_position_lat=0
		to_position_long=0
		
		if myfrom.split(',')[-1].isdigit():
			fromobj=au_suburb.objects.filter(postcode=myfrom.split(',')[-1]).first()# get only return 1
			if fromobj:
				myfrom=fromobj.suburb
				from_position_lat=fromobj.lat
				from_position_long=fromobj.lon
			if myto.split(',')[-1].isdigit():
				toobj=au_suburb.objects.filter(postcode=myto.split(',')[-1]).first()# get only return 1
				if toobj:
					myto=toobj.suburb
					to_position_lat=toobj.lat
					to_position_long=toobj.lon
		#import pdb; pdb.set_trace()
		if mysurround:
			allrec = travel_record.objects.filter(Q(from_position_lat__gte=float(from_position_lat)-0.1) ,Q(from_position_lat__lte= float(from_position_lat)+0.1), Q(to_position_lat__gte=float(to_position_lat)-0.1) ,Q(to_position_lat__lte=float(to_position_lat)+0.1))
			
		else:

			allrec = travel_record.objects.filter(Q(from_name__contains=myfrom) , Q(to_name__contains=myto))
		print allrec
		t = loader.get_template("index.html")
		c = Context({ 'allrec': allrec, 'message': 'query finished' })
		return HttpResponse(t.render(c))
	else:
		myoutput=show_main_page(request, 'query failure')
		return HttpResponse(myoutput)

def put_msg(request):
			print "come here"
			if 'e_mail' in request.GET:
				print "1"
				m_email = request.GET.get('e_mail', False)
				m_phone = request.GET.get('e_phone', False)
				m_content=request.GET.get('e_content', False)
				id=request.GET.get('rec_id', False)
				print "2"
				travelrec = travel_record.objects.get(rec_id=id)
				my_id =travelrec.user_id.user_id
				userrec=user_info.objects.get(user_id=my_id)
				print "3"
				insert_rec=	user_message(msg_cont=m_content, msg_email=	m_email, msg_phone=m_phone, user_id=userrec, rec_id=travelrec)
				insert_rec.save()
				print "after save"
				myoutput=show_main_page(request)
				return HttpResponse(myoutput)	
			else:
				myoutput=show_main_page(request)
				return HttpResponse(myoutput)
				
				
@logged_already()
def get_msg(request):
			passed = user_info.objects.get(email=request.session['member_id'] )
			allrec=user_message.objects.filter(user_id=passed) #need handle none exception here
			#import pdb; pdb.set_trace()
			if allrec:
				t = loader.get_template("show_msg.html")
				c = Context({ 'allrec': allrec })
				return HttpResponse(t.render(c))
			else:
				myoutput=show_main_page(request)
				return HttpResponse(myoutput)


	
def start_input(request):
	
			t = loader.get_template("start_now.html")
			c = Context({ 'allrec': 1 })
			return HttpResponse(t.render(c))


def detail(request, id):
			allrec = travel_record.objects.get(rec_id=id)
			t = loader.get_template("detail.html")
			c = Context({ 'allrec': allrec })
			return HttpResponse(t.render(c))			
			
			
@logged_already()	
def deleterec(request, id):
			allrec = travel_record.objects.get(rec_id=id)
			allrec.delete()
			myoutput=show_main_page(request)
			return HttpResponse(myoutput)


@logged_already()	
def updaterec(request, id):
			allrec = travel_record.objects.get(rec_id=id)
			#allrec.delete()
			myoutput=show_main_page(request)
			return HttpResponse(myoutput)
			
				
def showmessageinput(request, id):
	print id
	allrec = travel_record.objects.get(rec_id=id)
	t = loader.get_template("messageinput.html")
	userrec=''
	if request.session.get('member_id', False):
		passed=True
		my_id =allrec.user_id.user_id
		userrec=user_info.objects.get(user_id=my_id)
	else:
		passed=False
	c = Context({ 'passed': passed ,  'allrec': allrec , 'userinfo': userrec})
	return HttpResponse(t.render(c))
	




#@logged_already()
def unittest(request):
	
		t = loader.get_template("ut.html")
		c = Context({ 'allrec': 0 })
		return HttpResponse(t.render(c))
	

def start_now(request):
		if 'dedate' in request.GET:
			m_dedate = request.GET['dedate']
		
			m_seats = request.GET['seats']
			m_fromwhere=request.GET['fromwhere']

			m_towhere=request.GET['towhere']
			m_drived=request.GET['drived']
			from_position_lat=0
			from_position_long=0
			to_position_lat=0
			to_position_long=0
			#import pdb; pdb.set_trace()
			if m_fromwhere.split(',')[-1].isdigit():
				fromobj=au_suburb.objects.filter(postcode=m_fromwhere.split(',')[-1]).first()# get only return 1
				if fromobj:
					m_fromwhere=fromobj.suburb+","+fromobj.state
					from_position_lat=fromobj.lat
					from_position_long=fromobj.lon
			if m_towhere.split(',')[-1].isdigit():
				toobj=au_suburb.objects.filter(postcode=m_towhere.split(',')[-1]).first()# get only return 1
				if toobj:
					m_towhere=toobj.suburb+","+toobj.state
					to_position_lat=toobj.lat
					to_position_long=toobj.lon
			mm=request.session.get('member_id', False)
			if mm:
				passed = user_info.objects.get(email=request.session['member_id'] )
			else:
				passed=user_info.objects.get(email='default@default.com' ) #default
			print "m_drived "+m_drived
			#insert_rec=	travel_record(travel_time=m_dedate, expired=m_ardate, from_name=m_fromwhere, to_name=m_towhere,   num_seat=m_seats, isdriver=m_drived, user_id=passed)
			insert_rec=	travel_record( from_name=m_fromwhere, to_name=m_towhere, from_position_lat=from_position_lat, from_position_long=from_position_long, to_position_lat=to_position_lat, to_position_long=to_position_long, num_seat=m_seats, isdriver=m_drived, user_id=passed)
			insert_rec.save()
			allrec = travel_record.objects.order_by("created").reverse()[0:4]
			t = loader.get_template("index.html")
			c = Context({ 'allrec': allrec })
			return HttpResponse(t.render(c))


@csrf_protect				
def log_in(request):
		passed=False
		
		m_email = request.POST.get('email', False)
		m_passw = request.POST.get('password', False)
		if 	m_email:
			userdata = user_info.objects.filter(email__iexact=m_email).first()
			#import pdb; pdb.set_trace()
			passed=True
			
			if passed and check_password(m_passw , userdata.password):

				request.session['member_id'] = m_email
				allrec = travel_record.objects.filter(user_id=passed).order_by("created").reverse()[0:4]
				t = loader.get_template("index.html")
				c = Context({ 'passed': passed ,  'allrec': allrec, 'message':'login OK!' })
				return HttpResponse(t.render(c))
			else:
				print passed
			
		allrec = travel_record.objects.order_by("created").reverse()[0:4]
		t = loader.get_template("index.html")
		c = Context({ 'passed': passed ,  'allrec': allrec , 'message':'login failure!'})
		return HttpResponse(t.render(c))
				

@logged_already()
def log_off(request):
		try:
			del request.session['member_id']
			t = loader.get_template("index.html")
			c = Context({ 'logout': True })
			return HttpResponse(t.render(c))
		except KeyError:
			pass
			
			


def list_users(request):

    m_user = get_object_or_404(user_info, first_name='jiang')
    first_name = "first_name: %s" % m_user.first_name
    last_name = "last_name: %s" % m_user.last_name
    nick_name = "nick_name: %s" % m_user.nick_name
    city= "city: %s" % m_user.city
    return render_to_response("show.html", locals())
 

def searchregion(request):
		mysuburb = request.GET['q']
		
		if mysuburb.isdigit():
			mysub=au_suburb.objects.filter(postcode__startswith=mysuburb)
		else:
			mysub=au_suburb.objects.filter(suburb__startswith=mysuburb)# get only return 1
		myoutput=''
		for myitem in mysub:
			myoutput=myoutput+myitem.suburb+','+myitem.state+','+str(myitem.postcode)+'\n'
		print myoutput+"run in searchregion"
		return HttpResponse(myoutput)
		
		
@csrf_protect	
def sign_up(request):
		login=''
		
		logger = logging.getLogger(__name__)
		logger.error('RUN 0!--------------------------------------------')
		
		m_email = request.POST.get('email', False)
		m_passw = request.POST.get('passw', False)
		m_passr = request.POST.get('passr', False)
		m_fname=request.POST.get('fname', False)
		m_lname=request.POST.get('lname', False)
			
	  
		#import pdb; pdb.set_trace()
		if(m_email!=False and m_passw==m_passr and  m_passr!= '' and m_email.find('@')>=0):
			
			passed = user_info.objects.filter(email=m_email )
			if passed:
				return render_to_response("index.html", login)
			else:
				
				
				pwd = make_password(m_passw)
				print pwd;
					
				if  check_password(m_passw , pwd):
					print 'passed'
				else:
					print 'not passed'
					
				insert_rec=	user_info(first_name=m_fname, last_name=m_lname, password=pwd, email=m_email, city='chengdu', nick_name='tbd')
				
				insert_rec.save()
				
				request.session['member_id'] = m_email
				myoutput=show_main_page(request, 'sign up Ok')
				return HttpResponse(myoutput)
					
		else:
			print "run 5"
				
			return render_to_response("index.html", login)

		
