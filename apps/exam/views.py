from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.db.models import Count


def index(request):
    if 'user_id' in request.session:
        return redirect('/success')
    return render(request, "index/index.html")
# Create your views here.
def register(request):
    #because its short :P
    req = request.POST
    PostData = {
        'name': req['name'],
        'email': req['email'],
        'password': req['password'],
        'conf_password': req['conf_password']
    }
    #if there is no error returned
    if not User.objects.register(PostData):
        #then store new_user into a session so we could use it on the success page
        new_user_id = User.objects.create_user(PostData)
        request.session['user_id'] = new_user_id
        #then send it to the success page
        return redirect('/success')
    #else if we got the errors as array, then display it and then redirect to the regi page
    for error in User.objects.register(PostData):
        messages.error(request, error)
    request.session['loginErr'] = False
    return redirect('/')
def login(request):
    req = request.POST
    PostData = {
        'email': req['email'],
        'password': req['password']
    }
    if not User.objects.login(PostData):
        user_id = User.objects.get(email=PostData['email']).id
        request.session['user_id'] = user_id
        return redirect('/success')
    for error in User.objects.login(PostData):
        messages.error(request, error)
    request.session['loginErr'] = True
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
def success(request):
    if 'user_id' in request.session:
        user = User.objects.get(id = request.session['user_id'])
        items = Item.objects.all().order_by('-created_at')

        # print 'Items: ' + str(items)
        # for item in items:
        #     print item.content
        #     print item.added_by
        #     print item.wish_list
        #
        # wish_list = item.wish_list
        # print item.wish_list

        context = {
            'user': user,
            'items': items,
            # 'wish_list': items.wish_list
        }
        return render(request, "index/success.html", context)

def add(request):
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'user':user
    }
    return render(request, "index/add.html", context)

def add_new(request):
    PostData = {
        'item': request.POST['item'],
        'added_by': User.objects.get(id=request.session['user_id']),
    }
    errors = Item.objects.validation(PostData)
    if not errors:

        item_id = Item.objects.create_item(PostData) # This create method returns the id of the Item object it creates
        item = Item.objects.get(id=item_id)
        # print item
        user = User.objects.get(id=request.session['user_id'])
        item.wish_list.add(user) # This adds user to wish_list queryset
        print  item.wish_list
        return redirect('/success')

    for error in errors:
        messages.error(request, error)
    return redirect('/add')
def show_item(request, id):
    user = User.objects.get(id=request.session['user_id'])
    item = Item.objects.get(id=id),
    context = {
        'user': user,
        'items': item
    }
    return render(request, "index/show_item.html", context)
def add_to_my_list(request, id):
    PostData = {
        'item': id, # in this lane, i passed the id of the item that i want to add to the wish_list
        'user': request.session['user_id'], # passes user_id as usual
        'wish_list': User.objects.get(id=request.session['user_id']), # this line is to get the id of the user who got multi objects of the wish_list

    }
    Item.objects.add_to_my_list(PostData)
    return redirect('/success')
def destroy(request, id):
    user = User.objects.get(id=request.session['user_id'])
    Item.objects.get(id=id).wish_list.remove(user) # This removes user from wish_list queryset
    return redirect('/success')
