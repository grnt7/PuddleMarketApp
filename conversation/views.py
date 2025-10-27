from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item

from .forms import ConversationMessageForm
from .models import Conversation
# Create your views here.

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    # 1. Prevent contacting self
    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    # 2. Check for existing conversation
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        # ⚠️ FIX 1: Redirect to existing conversation
        existing_conversation = conversations.first()
        return redirect('conversation:detail', pk=existing_conversation.pk)

    # 3. Handle POST request (form submission)
    if request.method == "POST":
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            # Create new Conversation object
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            # Create the first message
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)
        
    # 4. Handle GET request OR invalid form from POST
    # ⚠️ FIX 2: Explicitly return render for the GET request / invalid POST
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        'form': form,
        'item': item,
    })

@login_required
def inbox(request):
        conversations = Conversation.objects.filter(members__in=[request.user.id])
        return render(request, 'conversation/inbox.html', {
            'conversations': conversations,
        })

@login_required
def detail(request, pk):
    # Retrieve the Conversation, ensuring the current user is a member
    # Using get_object_or_404 is safer than .get() for production code.
    conversation = get_object_or_404(Conversation.objects.filter(members__in=[request.user.id]), pk=pk)

    # Initialize form variable to None before the POST check (or define it later)
    # This prevents the NameError for GET requests.
    form = None
    
    if request.method == "POST":
        # 1. Instantiate the form with POST data
        form = ConversationMessageForm(request.POST) 
        
        if form.is_valid():
            # 2. Save the message
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            # 3. Save the conversation to update the 'modified_at' timestamp (if configured)
            conversation.save() 

            # 4. Redirect to prevent resubmission
            return redirect('conversation:detail', pk=pk)
        
        # 🛑 REMOVE THE 'ELSE' BLOCK! 
        # If the form is INVALID, we want the code to fall through to the final 
        # 'return render' statement. The 'form' variable is already defined and
        # holds the user's input and the validation errors, which the template needs.
        
    # If the request is a GET, or if the POST was invalid and fell through, 
    # we need to ensure a valid form instance is passed to the template.
    
    # 5. FIX FOR GET REQUEST: If 'form' is still None (i.e., it was a GET request), 
    #    initialize a fresh, empty form.
    if form is None:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation, 
        'form': form, # 'form' is guaranteed to be defined here!
    })