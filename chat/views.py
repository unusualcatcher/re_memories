# from django.shortcuts import render
# import datetime
# from .models import *

# def chatroom(request):
#     if request.method == 'POST':
#         author = request.user
#         time = request.POST.get('current_time')
#         datetime_obj = datetime.datetime.strptime(time, r"%m/%d/%Y, %H:%M:%S %p")
#         content = request.POST.get('new-message')
#         chat = ChatGroup.objects.filter(group_name='chat1').first()
#         new_message = GroupMessage.objects.create(author=author, created=datetime_obj, body=content, group=chat)
#         new_message.save()
#         messages = GroupMessage.objects.all()
#         context = {
#             'messages':messages,
#             'user':request.user
#         }
#         return render(request, 'chat/chatroom.html', context)
#     else:
#         messages = GroupMessage.objects.all()
#         context = {
#             'messages':messages,
#             'user':request.user
#         }
#         return render(request, 'chat/chatroom.html', context)
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import ChatGroup
from collections import defaultdict


def user_chats(request):
    if request.user.is_authenticated:
        user = request.user  # Assuming you have the user object

        # Fetch all chat groups the user is part of
        chat_groups = ChatGroup.objects.filter(member1=user) | ChatGroup.objects.filter(member2=user)

        # Create a list of tuples with each tuple containing the chat group and its members
        chat_data = [(chat_group, [chat_group.member1, chat_group.member2]) for chat_group in chat_groups]

        # Pass `chat_data` to the template
        return render(request, 'chat/user_chats.html', {'chat_data': chat_data, 'current_user': user})


def chatroom(request, group_name):
    if request.user.is_authenticated:
        chat = ChatGroup.objects.filter(group_name=group_name).first()
        members = (chat.member1, chat.member2)
        if request.user not in members:
            return redirect('home')
        else:
            for member in members:
                if member != request.user:
                    other_user = member
            return render(request, 'chat/chatroom.html', 
                          {'group_name': group_name, 'other_user':other_user, 'user':request.user})
    else:
        messages.success(request, 'You need to log in before starting a chat!')
        return redirect('login')
    return render(request, 'chat/chatroom.html', {'group_name': group_name})
