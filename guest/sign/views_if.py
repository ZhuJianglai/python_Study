
# p132-138
import time
from django.http import JsonResponse
from sign.models import Event, Guest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
doc = open("test.log", "a+")

# 添加发布会接口
def add_event(request):
    eid = request.POST.get( 'eid', '' )  # 发布会id
    name = request.POST.get( 'name', '' )  # 发布标题
    limit = request.POST.get( 'limit', '' )  # 限制人数
    status = request.POST.get( 'status', '' )  # 状态
    address = request.POST.get( 'address', '' )  # 地址
    strat_time = request.POST.get( 'start_time', '' )  # 发布会时间
    if eid == '' or name == '' or limit == '' or address == '' or strat_time == '':
        return JsonResponse( {'status': 10021, 'message': 'parameter error'} )
    result = Event.objects.filter( id=eid )
    if result:
        return JsonResponse( {'status': 1022, 'message': 'event id already exists'} )

    result = Event.objects.filter( name=name )
    if result:
        return JsonResponse( {'status': 10023, 'message': 'event name already exists'} )
    if status == '':
        status = 1
        try:
            Event.objects.create( id=id, name=name, limit=limit, address=address, status=int( status ),
                                  strat_time=strat_time )
        except ValidationError as e:
            error = 'start_time format error.It must be in YYYY-MM-DD HH:MM:SS format.'
            return JsonResponse( {'status': 10024, 'message': error} )

        return JsonResponse( {'status': 200, 'message': 'add event success'} )


# 查询发布会接口
def get_event_list(request):
    eid = request.GET.get('eid', '')  # 发布会id
    name = request.GET.get('name', '')  # 发布会名称
    print(type(eid),file=doc)
    print('eid:' + eid + ',name:' + name, file=doc)
    if eid == '' and name == '':
        return JsonResponse( {'status': 10021, 'message': 'parameter error'} )

    if eid != '':
        event = {}
        try:
            result = Event.objects.get( id=eid )
            print(str(eid) + str(result),file=doc)
        except ObjectDoesNotExist:
            return JsonResponse( {'status': 10022, 'message': 'query result is empty'} )
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse( {'status': 200, 'message': 'success', 'datas': event} )
    if name != '':
        datas = []
        result = Event.objects.filter( name__contains=name )
        if result:
            for r in result:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append( event )
                return JsonResponse( {'status': 200, 'message': 'success', 'datas': datas} )
            else:
                return JsonResponse( {'status': 200, 'message': 'query result is empty'} )


# 添加嘉宾接口
def add_guest(request):
    eid = request.POST.get( 'eid', '' )
    realname = request.POST.get( 'realname', '' )
    phone = request.POST.get( 'phone', '' )
    email = request.POST.get( 'email', '' )
    if eid == '' or realname == '' or phone == '':
        return JsonResponse( {'status': 10021, 'message': 'patameter error'} )
    result = Event.objects.filter( eid=eid )
    if not result:
        return JsonResponse( {'status': 10022, 'message': 'event id null'} )

    result = Event.objects.get( id=eid ).status
    if not result:
        return JsonResponse( {'status': 10023, 'message': 'event status is not available'} )

    event_limit = Event.objects.get( id=eid ).limit  # 发布人数的限制
    guest_limit = Guest.objects.filter( event_id=eid )
    if len( guest_limit ) >= event_limit:
        return JsonResponse( {'status': 10024, 'message': 'enent number is full'} )
    event_time = Event.objects.get( id=eid ).start_time
    etime = str( event_time ).split( '.' )[0]
    timeArray = time.strptime( etime, '%Y-%m-%d %H:%M:%S' )
    e_time = int( time.mktime( (timeArray) ) )

    now_time = str( time.time() )
    ntime = now_time.split( '.' )[0]
    n_time = int( ntime )

    if n_time >= e_time:
        return JsonResponse( {'status': 10025, 'message': 'event has started'} )
    try:
        Guest.objects.create( realname=realname, phone=int( phone ), email=email, sign=0, event_id=int( eid ) )
    except IndentationError:
        return JsonResponse( {'status': 10026, 'message': 'the event guest phone number repeat'} )
    return JsonResponse( {'status': 200, 'message': 'add guest succes'} )


# 嘉宾查询接口
def get_guest_list(request):
    eid = request.GET.get( 'eid', '' )  # 关联发布会id
    phone = request.GET.get( 'phone, ' )  # 嘉宾手机号
    if eid == '':
        return JsonResponse( {'status': 10021, 'message': 'eid cannot be empty'} )
    if eid != '' and phone == '':
        datas = []
        results = Guest.objects.filter( event_id=eid)
        if results:
            for r in results:
                guest = {}
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sign'] = r.sign
                datas.append(guest)
            return JsonResponse( {'status': 200, 'message': 'succes', 'data': datas})
        else:
            return JsonResponse( {'status': 10022, 'message': 'query result is empty'})

    if eid != '' and phone != '':
        guest = {}
        try:
            result = Guest.objects.get( phone=phone, event_id=eid )
        except ObjectDoesNotExist:
            return JsonResponse( {'status': 10022, 'message': 'query result is empty'} )
        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sign'] = result.sign
            return JsonResponse({'status': 200, 'message': 'success', 'data': guest} )


# 发布会签到接口
def user_sign(request):
    eid = request.POST.get( 'eid', '' )
    phone = request.POST.get( 'phone', '' )

    if eid == '' or phone == '':
        return JsonResponse( {'status': 10021, 'message': 'parameter error'} )

    result = Event.objects.filter( id=eid )
    if not result:
        return JsonResponse( {'status': 10022, 'message': 'event id null'} )
    result = Event.objects.filter( id=eid ).status
    if not result:
        return JsonResponse( {'status': 10023, 'message': 'event status is not available'} )
    event_time = Event.objects.get( id=eid ).start_time  # 发布时间
    etime = str( event_time ).split( "." )[0]
    timeArray = time.strptime( etime, '%Y-%m-%%d %H:%M:%S' )
    e_time = int( time.mktime( timeArray ) )

    now_time = str( time.time() )
    ntime = now_time.split( '.' )[0]
    n_time = int( ntime )

    if n_time >= e_time:
        return JsonResponse( {'status': 10024, 'message': 'event has started'} )
    result = Guest.objects.filter( phone=phone )
    if not result:
        return JsonResponse( {'status': 10025, 'message': 'user phone null'} )
    result = Guest.objects.filter( event_id=eid, phone=phone )
    if not result:
        return JsonResponse( {'status': 10026, 'message': 'user did not participate in the conference'} )
    result = Guest.ojbects.get( event_id=eid, phone=phone ).sign
    if result:
        return JsonResponse( {'status': 10027, 'message': 'user has sign in'} )
    else:
        Guest.objects.filter( event_id=eid, phone=phone ).update( sign='1' )
        return JsonResponse( {'status': 200, 'status': 'sign success'} )
