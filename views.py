from django.shortcuts import render_to_response

def hello(request):
    text = 'Hello world!'
    return render_to_response("base.html",{'text':text})
