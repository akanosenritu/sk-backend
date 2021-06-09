import json
from idlelib.idle_test.mock_idle import Func

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.aggregates import ArrayAgg, StringAgg
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Value, F, TextField, Sum, Count, Case, When, Q, Subquery, OuterRef
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, views, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from api.filters import EventFilter
from api.models import *
from api.serializers import RegisteredStaffSerializer, ClothesSettingSerializer, GatheringPlaceSettingSerializer, \
    PositionDataSerializer, PositionSerializer, PositionGroupSerializer, EventSerializer, EmployeeSerializer, \
    GenderSerializer, MyUserSerializer, MailSerializer, MailsForEventSerializer, MailTemplateSerializer


class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    

class RegisteredStaffViewSet(viewsets.ModelViewSet):
    queryset = RegisteredStaff.objects.all().order_by("staff_id")
    serializer_class = RegisteredStaffSerializer
    
    @action(detail=False, methods=["get"])
    def is_this_staff_id_available(self, request):
        potential_staff_id = request.query_params.get("staff_id", None)
        if not potential_staff_id:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"staff_id": "staff_id is missing."})
        
        staffs = RegisteredStaff.objects.filter(staff_id=potential_staff_id)
        if staffs:
            return Response(status=status.HTTP_200_OK, data={"is_available": False})
        else:
            return Response(status=status.HTTP_200_OK, data={"is_available": True})
    
    
class ClothesSettingViewSet(viewsets.ModelViewSet):
    queryset = ClothesSetting.objects.all()
    serializer_class = ClothesSettingSerializer
    
    
class GatheringPlaceSettingViewSet(viewsets.ModelViewSet):
    queryset = GatheringPlaceSetting.objects.all()
    serializer_class = GatheringPlaceSettingSerializer


class PositionDataViewSet(viewsets.ModelViewSet):
    queryset = PositionData.objects.all()
    serializer_class = PositionDataSerializer
    
    
class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionGroupViewSet(viewsets.ModelViewSet):
    queryset = PositionGroup.objects.all()
    serializer_class = PositionGroupSerializer
    

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter


@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({"details": "CSRF cookie set."})


class UserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = get_object_or_404(MyUser, pk=request.user.id)
        return JsonResponse(data=MyUserSerializer(user).data)


@require_POST
def login_view(request, *args):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    if username is None or password is None:
        return JsonResponse({
            "error": "Please enter both username and password"
        }, status=400)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            "detail": "Success",
            "isStaff": user.is_staff,
            "username": user.username,
        })
    return JsonResponse(
        {"error": "Invalid credentials"},
        status=400,
    )


@login_required
def is_logged_in(request):
    user = request.user
    return JsonResponse({
        "detail": "success",
        "isStaff": user.is_staff,
        "username": user.username,
    })


@require_POST
@login_required
def logout_view(request):
    logout(request)
    return JsonResponse(
        {"detail": "success"}
    )


class AvailableStaffsView(views.APIView):
    def get(self, request):
        dates = request.query_params.getlist("date", None)
        if not dates:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            dates = [datetime.date.fromisoformat(date) for date in dates]
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        result = dict()
        for date in dates:
            queryset = RegisteredStaff.objects.exclude(position__date=date)
            serializer = RegisteredStaffSerializer(queryset, many=True)
            result[date.isoformat()] = serializer.data
        return Response(result)


class MailViewSet(viewsets.ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
    
    
class MailTemplateViewSet(viewsets.ModelViewSet):
    queryset = MailTemplate.objects.all()
    serializer_class = MailTemplateSerializer


class MailsForEventViewSet(viewsets.ModelViewSet):
    queryset = MailsForEvent.objects.all()
    serializer_class = MailsForEventSerializer


class GetOrCreateMailsForEventOfEventView(views.APIView):
    def get(self, request):
        event_uuid = request.query_params.get("event_uuid", None)
        #  if param "event_uuid" is not supplied, return 400
        if not event_uuid:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"event_uuid": "event_uuid is missing."})
       
        #  get the event and mailsForEvent
        #  if the event doesn't have an associated mailsForEvent, create it
        #  return the mailsForEvent
        event = get_object_or_404(Event.objects.all(), uuid=event_uuid)
        try:
            mailsForEvent = event.mails
        except ObjectDoesNotExist:
            # create a new mailsForEvent
            serializer = MailsForEventSerializer(data={
                "event_uuid": event_uuid,
                "mail_uuids": [],
            })
            serializer.is_valid()
            mailsForEvent = serializer.save()
        return Response(MailsForEventSerializer(mailsForEvent).data)
    
    
class MailSenderView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def is_mail_already_sent(self, staff: RegisteredStaff, event: Event):
        pass
    
    def get(self, request):
        params = request.query_params

        #  extract all necessary information from request
        recipient_staff_uuid = params.get("recipient_staff_uuid", None)
        event_uuid = params.get("event_uuid", None)
        if not recipient_staff_uuid:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"recipient_staff_uuid": "recipient_staff_uuid is missing."}
             )
        if not event_uuid:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"event_uuid": "event_uuid is missing."})

        #  get the registered staff with uuid of "recipient_staff_uuid" and check if the staff has an email address.
        staff = get_object_or_404(RegisteredStaff, pk=recipient_staff_uuid)

        #  get the event with uuid of "event_uuid" and check if the event already has a related mailsForEvent
        event = get_object_or_404(Event, pk=event_uuid)
        try:
            mailsForEvent = event.mails
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"event": "the event doesn't have a related mailsForEvent."}
            )

        #  check if an email has been sent to this staff regarding this event.
        #  return the check result.
        mails = mailsForEvent.mails.all().filter(recipient__uuid=staff.uuid).filter(is_sent=True)
        if mails:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "status": "error",
                    "error": "Another email has already been sent to this staff regarding this event."
                }
            )
        return Response(
            status=status.HTTP_200_OK,
            data={"status": "ok"}
        )
    
    def post(self, request):
        user = get_object_or_404(MyUser, pk=request.user.id)
        data = request.data
        
        #  extract all necessary information from request
        message = data.get("message", None)
        subject = data.get("subject", None)
        from_email = data.get("from_email", None)
        recipient_staff_uuid = data.get("recipient_staff_uuid", None)
        event_uuid = data.get("event_uuid", None)
        
        if not message:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "message is missing."})
        if not subject:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"subject": "subject is missing."})
        if not from_email:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"from_email": "from_email is missing."})
        if not recipient_staff_uuid:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"recipient_staff_uuid": "recipient_staff_uuid is missing."}
             )
        if not event_uuid:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"event_uuid": "event_uuid is missing."})
        
        #  get the registered staff with uuid of "recipient_staff_uuid" and check if the staff has an email address.
        staff = get_object_or_404(RegisteredStaff, pk=recipient_staff_uuid)
        if not staff.email_address:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"staff": "the staff doesn't have an email address."}
            )
        recipient = staff.email_address
        
        #  get the event with uuid of "event_uuid" and check if the event already has a related mailsForEvent
        event = get_object_or_404(Event, pk=event_uuid)
        try:
            mailsForEvent = event.mails
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"event": "the event doesn't have a related mailsForEvent."}
            )
        
        #  check if an email has been sent to this staff regarding this event.
        mails = mailsForEvent.mails.all().filter(recipient__uuid=staff.uuid).filter(is_sent=True)
        if mails:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Another email has already been sent to this staff regarding this event."}
            )
            
        #  if everything is ok, first create a mail object
        mail = Mail.objects.create(
            sender=user,
            recipient=staff,
            content=message
        )
        mail.save()
        
        #  then register it to mailsForEvent
        mailsForEvent.mails.add(mail)
        
        try:
            send_mail(subject, message, from_email, recipient_list=[recipient], fail_silently=False)
            mail.is_sent = True
            mail.sent_at_datetime = timezone.now()
            mail.save()
        except BadHeaderError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"header": "invalid header found."})
        
        return Response(status=status.HTTP_200_OK, data={"success": "mail has been sent."})
