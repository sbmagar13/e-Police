from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Web_App.models import Fir,general_diary,lookup_table
from police.models import Stationdata
from users.models import PasModel,VoterModel,LcnModel,CtzModel
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse
import unirest
from urllib import quote_plus
import uuid
from django.core.cache import cache
from Web_App.secret import uid,pwd,Mashape_Key
import random
import string
from ipdb import set_trace
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from cgi import escape
from django.core.mail import EmailMessage



OTP = """Your OTP password for Online FIR/GD is {otp}"""
VERIFIED = """Your {report_type} has been successfully registered.
            Your {report_type} reference id is {ref_id}"""

EMAIL = """
Hello {fname},
    Your {report_type} has been successfully registered. Your reference number is {ref_id}.
    A pdf copy of the {report_type} has been attached.
"""




templates={ 'OTP' : OTP, 
            'VERIFIED' :VERIFIED,
            'EMAIL' : EMAIL }


def generate_password(length=8):
    rng = random.SystemRandom()
    return "".join([rng.choice(string.digits) for i in range(length)])

def get_OTP():
    while True:
        newOTP = generate_password()
        if cache.get(newOTP)==None:
            return newOTP

def send_sms(number,template_type,report_type=None,**kargs):
    message = templates[template_type]
    #set_trace()
    otp = None
    if template_type=='OTP':
        otp = get_OTP()
        cache.set(otp,kargs['ref_id'],300)
        cache.set(kargs['ref_id'],otp,300)
        message = message.format(otp=otp )
    elif template_type=='VERIFIED':
        message = message.format(report_type=report_type, ref_id=kargs['ref_id'])
    response = unirest.get(
        url = "https://riddhi_raval-site2sms-v1.p.mashape.com/localhost:49219/forexproj/smspg.aspx",
    params = { 'msg' : quote_plus(message),
                'phone' : number,
                'pwd' : pwd,
                'uid' : uid,
            },
    headers={
    "X-Mashape-Key": Mashape_Key,
    "Accept": "application/json"
    },
    callback= callback_function
    )
    
    return otp

def callback_function(response):
  response.code # The HTTP status code
  response.headers # The HTTP headers
  response.body # The parsed response
  response.raw_body # The unparsed response

#@login_required(login_url='/')
#@is_user
def register_report(request):
    # User Personal Details
    firstname = request.POST.get('fname')
    lastname = request.POST.get('lname')
    mobile = request.POST.get('mob')
    email = request.POST.get('email')
    address = request.POST.get('address')
    dob = request.POST.get('dob')

    # User id proof 
    idtype1 = request.POST.get('type1')
    id1value = request.POST.get('id1')
    idtype2 = request.POST.get('type2')
    id2value = request.POST.get('id2')
    
    # Report details
    optionsRadios = request.POST.get('optionsRadios')
    subject = request.POST.get('subject')
    suspect = request.POST.get('suspect')
    date_string = request.POST.get('occurence')
    location = request.POST.get('location')
    witness = request.POST.get('witness')
    loss = request.POST.get('loss')
    detail = request.POST.get('details')
    
    #print request.POST
    # Validate User
    try:
        if idtype1 == 'VID':
            id1_data = VoterModel.objects.get(vid=id1value)
        elif idtype1 == 'PASSPORT':
            id1_data = PasModel.objects.get(pid=id1value)

        if idtype2 == 'LICENSE':
            id2_data = LcnModel.objects.get(rid=id2value)
        elif idtype2 == 'IDENTITY':
            id2_data = CtzModel.objects.get(aid=id2value)
    except (VoterModel.DoesNotExist,PasModel.DoesNotExist):
        id1_data = None
    except (LcnModel.DoesNotExist,CtzModel.DoesNotExist):
        id2_data = None
    except Exception as e:
        print e
   
    date_of_birth = datetime.strptime(dob,'%Y/%m/%d')
    date_of_birth = timezone.make_aware(date_of_birth,timezone='none')
    ref_id = uuid.uuid4()
    if id1_data is not None and id2_data is not None:
        if id2_data.firstname == firstname and id1_data.firstname == firstname:
            if id2_data.lastname == lastname and id1_data.lastname == lastname:
                if id2_data.dob == date_of_birth.date() and id1_data.dob == date_of_birth.date():
                    try:
                        otp = send_sms(number=mobile,template_type='OTP',report_type=optionsRadios,ref_id=ref_id)
                    except Exception as e:
                        print e            
                
                

    # prepare to insert into db
    
    
    try:
        StationCode = Stationdata.objects.get(StationCode="00000003")     
    except Stationdata.DoesNotExist:
        StationCode='00000000'
    
    time = datetime.strptime(date_string,'%Y/%m/%d %H:%M')
    time = timezone.make_aware(time,timezone=None)
    print time
    if optionsRadios == "GD":
        b = general_diary(ref_id=ref_id, firstname=firstname, lastname=lastname , mobile=mobile, email=email,address=address, 
            DOB=date_of_birth.date(), idType_1=idtype1 , idType_1_value=id1value,idType_2=idtype2,idType_2_value=id2value,
            StationCode=StationCode, Subject=subject, pub_date=timezone.now(),
            Time=time,Place=location,Loss=loss, detail=detail)
    elif optionsRadios == "FIR":
        b = Fir(ref_id=ref_id, firstname=firstname, lastname=lastname , mobile=mobile, email=email,address=address,
            DOB=date_of_birth.date(), idType_1=idtype1 , idType_1_value=id1value,idType_2=idtype2,idType_2_value=id2value,
            StationCode=StationCode, Subject=subject, pub_date=timezone.now(),
            Suspect=suspect, Witness=witness, Time=time,Place=location,Loss=loss, detail=detail)
    
    try:
        b.save()
        hashmap = hashlib.sha224(mobile+str(ref_id)).hexdigest()
        lookup_table(ref_id=ref_id,hashmap=hashmap,type=optionsRadios).save()
        request.session['hash']= hashmap

        return redirect('verifyOtp')
    except Exception as e:
        print e
    return redirect('lodge_new')


def verify_otp(request):
    if not request.POST:
        return render(request,'users/otp.html')
    else: 
        hash_id = request.POST.get('hash')
        otp_post = request.POST.get('otp_code')
        lookup_obj = lookup_table.objects.get(hashmap=hash_id)
        otp_cache = cache.get(lookup_obj.ref_id)

        if lookup_obj.type == "GD":
            report_obj = general_diary.objects.get(ref_id=lookup_obj.ref_id)
        else:
            report_obj = Fir.objects.get(ref_id=lookup_obj.ref_id)
        
        if otp_post == otp_cache:
            report_obj.OTP = True
            report_obj.save()
            send_sms(number=report_obj.mobile,template_type='VERIFIED',report_type=lookup_obj.type,ref_id=lookup_obj.ref_id)
            request.session['reference']="{ref_id}__{type}".format(ref_id=lookup_obj.ref_id,type=lookup_obj.type)
            lookup_obj.delete()

            return redirect('pdf')
        else:
            return HttpResponse("Failed")

def resend(request):
    try:
        hash_id = request.POST.get('hash')
        
        lookup_obj = lookup_table.objects.get(hashmap=hash_id)
        if lookup_obj.type == "GD":
            report_obj = general_diary.objects.get(ref_id=lookup_obj.ref_id)
        else:
            report_obj = Fir.objects.get(ref_id=lookup_obj.ref_id)
        
        otp = send_sms(number=report_obj.mobile, template_type='OTP', report_type=lookup_obj.type, ref_id=lookup_obj.ref_id)
        return HttpResponse('success')
    except Exception as e:
        print e



def success(request):
    #Retrieve data or whatever you need
    data = request.session['reference'].split('__')
    if data[1] == "GD":
        report_obj = general_diary.objects.get(ref_id=data[0])
    else:
        report_obj = Fir.objects.get(ref_id=data[0])
    address_list = report_obj.StationCode.address.split(',')
    
    pdf,response = render_to_pdf(
            'users/pdf_mould.html',
            {
                'pagesize':'A4',
                'report': report_obj,
                'address_list' : address_list,
            }
        )
    body = templates['EMAIL'].format(ref_id=report_obj.ref_id,report_type=data[1],fname=report_obj.firstname)
    email = EmailMessage(subject='Report Confimation', body=body, from_email='sbmagar.sbm99@gmail.com',
            to=[report_obj.email],attachments=[('Report.pdf',pdf,'application/pdf')])
    
    email.attach('Report.pdf',pdf,'application/pdf')
    email.send()
    return response


    """
        return render(request,'users/pdf_mould.html',{
                    'pagesize':'A4',
                    'report': report_obj,
                    'address_list' : address_list,
                })
        """

def render_to_pdf(template_src,context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    
    pdf = pisa.CreatePDF(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue(),HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
