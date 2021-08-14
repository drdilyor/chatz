import json
from time import sleep

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from chat import models


@login_required
def chat(request: HttpRequest) -> HttpResponse:
    return render(request, 'chat/chat.html')


def to_json(message: models.Message):
    return {
        'id': message.id,  # noqa
        'text': message.text,
        'owner': {
            'username': message.owner.username,
        },
        'created_at': message.created_at,
    }

@login_required
@csrf_exempt
def messages(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        try:
            offset = int(request.GET['offset'])
        except ValueError:
            return HttpResponseBadRequest()
        except KeyError:
            return JsonResponse([
                to_json(i) for i in models.Message.objects.all()
            ], safe=False)
        else:
            # hack
            new_messages = []
            for i in range(15):  # 15 seconds
                new_messages = [to_json(i) for i in
                                models.Message.objects.filter(id__gte=offset)]
                if new_messages:
                    break
                sleep(1)
            return JsonResponse(new_messages, safe=False)
    elif request.method == 'POST':
        body = json.loads(request.body)
        text = body.get('text', '')
        if not text or not isinstance(text, str):
            return HttpResponseBadRequest()

        message = models.Message(
            text=text,
            owner=request.user,  # noqa
        )
        message.save()
        return JsonResponse(to_json(message), safe=False)
    return JsonResponse(None, status=401, safe=False)

