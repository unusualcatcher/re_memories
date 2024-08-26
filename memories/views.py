from django.shortcuts import render, redirect
from .models import Memory
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from sentence_transformers import SentenceTransformer, util
from django.db.models import Q
from chat.models import ChatGroup
from django.urls import reverse
import warnings
import datetime
import random
import string

warnings.filterwarnings("ignore", category=FutureWarning)

model = SentenceTransformer('all-MiniLM-L6-v2')


def generate_random_string(length=10):
    """Generate a random string of letters with the given length."""
    letters = string.ascii_letters  # Includes both uppercase and lowercase letters
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string

def chat_exists(user1, user2):
    # Check if a chat group exists with the two users
    return ChatGroup.objects.filter(
        (Q(member1=user1) & Q(member2=user2)) |
        (Q(member1=user2) & Q(member2=user1))
    ).exists()

def compute_similarity(sentence1: str, sentence2: str) -> float:
    embeddings1 = model.encode(sentence1, convert_to_tensor=True)
    embeddings2 = model.encode(sentence2, convert_to_tensor=True)
    similarity_score = util.pytorch_cos_sim(embeddings1, embeddings2).item()
    print(f"Similarity between '{sentence1[:50]}' ANDDDDDDDDDD '{sentence2[:50]}': {similarity_score}")
    return similarity_score


def memory_choose(request):
    if request.user.is_authenticated:
        memories = Memory.objects.filter(author=request.user)
        
        if request.method == 'POST':
            memory_index = request.POST.get('memory')
            if memory_index is None:
                messages.error(request, 'No memory selected.')
                return redirect('choose_memory')

            try:
                memory_index = int(memory_index)
                memory = memories[memory_index]
            except (IndexError, ValueError):
                messages.error(request, 'Invalid memory index.')
                return redirect('choose_memory')
            
            print('Selected memory:', memory.title)
            
            cosine_similarities = {}
            users = User.objects.exclude(id=request.user.id)  # Exclude current user from the search
            
            for user in users:
                user_cosine_similarities = []
                user_memories = Memory.objects.filter(author=user)
                
                for user_memory in user_memories:
                    cosine_similarity = compute_similarity(memory.content, user_memory.content)
                    user_cosine_similarities.append(cosine_similarity)
                
                if user_cosine_similarities:
                    most_similar_index = user_cosine_similarities.index(max(user_cosine_similarities))
                    most_similar = user_memories[most_similar_index]
                    cosine_similarities[most_similar] = user_cosine_similarities[most_similar_index]
            
            print('Cosine similarities:', cosine_similarities)
            
            if not cosine_similarities:
                return render(request, 'memories/error_page.html', {'error':'No memories found.',
                                        'title':'No memories found'})
            

            max_similarity = max(cosine_similarities.values())

            if max_similarity < 0.55:
                return render(request, 'memories/error_page.html', {'error':'No memories found.',
                                        'title':'No memories found'})
            
            best_match = max(cosine_similarities.items(), key=lambda x: x[1])
            matched_memory = best_match[0]
            print('Matched memory title:',matched_memory.title)
            print('Matched memory cosine similarity:', best_match[1])
            matched_memory_author = matched_memory.author
            
            while True:
                if chat_exists(request.user, matched_memory_author):
                    cosine_similarities.pop(matched_memory, None)
                    if not cosine_similarities:
                        messages.info(request, 'No new chats available.')
                        return redirect('choose_memory')
                    best_match = max(cosine_similarities.items(), key=lambda x: x[1])
                    matched_memory = best_match[0]
                    matched_memory_author = matched_memory.author
                else:
                    break
            
            random_string = generate_random_string()
            new_chat = ChatGroup.objects.create(
                group_name=random_string,
                member1=request.user,
                member2=matched_memory_author
            )
            
            print('Chat created between:', new_chat.member1.username, 'and', new_chat.member2.username)
            
            url = reverse('chatroom', args=[new_chat.group_name])
            return redirect(url)
        
        else:
            return render(request, 'memories/choose.html', {'memories': memories})
    
    else:
        messages.success(request, 'You need to log in before starting a chat!')
        return redirect('login')

def home(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            memories = Memory.objects.filter(author=request.user)
            if len(memories) < 1:
                messages.success(request, 'You need to add some memories to start chatting!')
                return redirect('create')
            else:
                return redirect('choose_memory')
        else:
            messages.success(request, 'You need to log in to start chatting!')
            return redirect('login')
    else:
        return render(request, 'memories/index.html')

def dashboard(request):
    if request.user.is_authenticated:
    # Ensure that the current user is retrieved as a single User instance
        current_user = User.objects.get(username=request.user.username)
        
        # Use the single User instance to filter the Memory objects
        memories = Memory.objects.filter(author=current_user)
        
        return render(request, 'memories/dashboard.html', {'memories': memories})
    else:
        return redirect('login')

def create_memory(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('memory')
        time = request.POST.get('current_time')
        print(time)
        print('type:', type(time))
        datetime_obj = datetime.datetime.strptime(time, r"%m/%d/%Y, %H:%M:%S %p")
        print(datetime_obj)
        print('type obj:', type(datetime_obj))
        Memory.objects.create(
            title=title,
            content=content,
            author=request.user,
            date_posted=datetime_obj
        )
        
        return redirect('profile')  
    
    return render(request, 'memories/create_memory.html')
