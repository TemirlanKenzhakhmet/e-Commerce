from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from item.models import Item
from .forms import ConversationMessageForm
from .models import Conversation, ConversationMessage

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', slug=item.slug)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new_conv.html', {
        'form': form,
    })

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    })


# ------------------------------------------------------------------------------------------------------------------------------- #


@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    print(conversation.members.count())

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()
            return redirect('conversation:detail-message', pk=conversation_message.id)
        else:
            return render(request, 'conversation/partials/message_form.html', {'form': form})
        

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
    })

@login_required
def new_message(request):
    context = {
        'form': ConversationMessageForm()
    }
    return render(request, 'conversation/partials/message_form.html', context)

@login_required
def detail_message(request, pk):
    message = ConversationMessage.objects.get(pk=pk)
    context = {
        'message': message
    }
    return render(request, 'conversation/partials/message_detail.html', context)

@login_required
def update_message(request, pk):
    message = ConversationMessage.objects.get(pk=pk)
    form = ConversationMessageForm(request.POST or None, instance=message)

    if request.method == 'POST':
        if form.is_valid():
            message = form.save()
            print()
            return redirect('conversation:detail-message', pk=message.id)
    
    context = {
        'form': form, 
        'message': message
    }

    return render(request, 'conversation/partials/message_form.html', context)

@login_required
def delete_message(request, pk):
    message = ConversationMessage.objects.get(pk=pk)
    message.delete()
    return HttpResponse('')