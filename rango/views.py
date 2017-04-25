from django.shortcuts import render

# Create your views here.
from rango.models import Category, Subject, Campus, User, Answers, CategoryUserLikes
from rango.forms import CategoryForm, TestUeditorModelForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from rango.bing_search import run_query
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Q


def index(request):
    category_list = Category.objects.extra(
            select={
                'answer_count': 'select count(*) from rango_answers where rango_answers.category_id = rango_category.id'
            },
        ).order_by('-answer_count')[0:13]
    subject_list = Subject.objects.extra(
            select={
                'category_count': 'select count(*) from rango_category where rango_category.subject_id = rango_subject.id'
            },
        ).order_by('-category_count')[0:13]
    campus_list = Campus.objects.order_by('-views')[:3]
    context_dict = {'categories': category_list, 'subjects': subject_list, 'campuss': campus_list}
    response = render(request,'rango/index.html', context_dict)
    return response

def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    return render(request, 'rango/about.html', {'visits': count})
'''
def category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        #subject = Subject.objects.get(category=category)

        #context_dict['subject_title'] = subject.title
        context_dict['category'] = category

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)
'''	

def campus(request, campus_name_slug):
	context_dict = {}
	try:
		campus = Campus.objects.get(slug=campus_name_slug)
		subject_list = Subject.objects.filter(Q(campus=campus)).extra(
            select={
                'category_count': 'select count(*) from rango_category where rango_category.subject_id = rango_subject.id'
            },
        ).order_by('-category_count')[0:30]
		context_dict['subjects'] = subject_list
		context_dict['campus_name_ch'] = campus.name_ch
		context_dict['campus'] = campus
	except Subject.DoesNotExist:
		pass

	return render(request, 'rango/campus.html', context_dict)

def subject(request, subject_name_slug):
    context_dict = {}

    if "order" in request.GET:
        order = int(request.GET['order'])
    else:
        order = 0

    if "keyword" in request.GET:
        keyword = request.GET['keyword']
    else:
        keyword = ''

    try:
        subject = Subject.objects.get(slug=subject_name_slug)
        cats = Category.objects.filter(Q(subject=subject)).extra(
                select={
                    'answer_count': 'select count(*) from rango_answers where rango_answers.category_id = rango_category.id'
                },
            )
        
        cats = cats.order_by('-answer_count')
        context_dict['subject_title_ch'] = subject.title_ch
        context_dict['subject_name_slug'] = subject_name_slug
        context_dict['subject'] = subject
        context_dict['categories'] = cats
        context_dict['order'] = order
    except Subject.DoesNotExist:
        pass
    return render(request, 'rango/subject.html', context_dict)

def add_category(request, subject_name_slug):

    try:
        sub = Subject.objects.get(slug=subject_name_slug)
    except Subject.DoesNotExist:
                sub = None

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            if sub:
                category = form.save(commit=False)
                category.subject = sub
                category.views = 0
                category.likes = 0
                category.save()
                # probably better to use a redirect here.
                return subject(request, subject_name_slug)
        else:
            print form.errors
    else:
        form = CategoryForm()

    context_dict = {'form':form, 'subject': sub}

    return render(request, 'rango/add_category.html', context_dict)
'''
def get_category_list(max_results=0, cat_search_keyword=''):
    cat_list = []
    if cat_search_keyword:
        cat_list = list(Category.objects.filter(name__contains=cat_search_keyword))
        cat_list += list(Category.objects.filter(no__contains=cat_search_keyword))
        cat_list = list(set(cat_list))
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]

    return cat_list


def suggest_category(request):
    cats = []
    cat_search_keyword = ''
    if request.method == 'GET':
        cat_search_keyword = request.GET['suggestion']
        cat_search_keyword = cat_search_keyword.rstrip()

        if cat_search_keyword != '' and cat_search_keyword is not None:
            cats = get_category_list(0, cat_search_keyword)
            context_dict = {'cats': cats}
        else:
            subs = Subject.objects.all().filter(~Q(slug="both"))
            context_dict = {'subs': subs}

        return render(request, 'rango/cats_li.html', context_dict)	

def track_url(request):
    category_id = None
    if request.method == 'GET':
        if 'category_id' in request.GET:
            category_id = request.GET['category_id']
            try:
                category = Category.objects.get(id=category_id)
                category.views = category.views + 1
                category.save()
            except:
                pass

    return HttpResponseRedirect(category.slug)
'''	
	
@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes =  likes
            cat.save()
    return HttpResponse(likes)
	
def get_category(request, cat_name_slug):
    context_dict = {}
    return_code = 1

    if request.method == 'POST':
        editor_form = TestUeditorModelForm(request.POST)

        if editor_form.is_valid():
            content = editor_form.save(commit=True)
            content.save()

            cat = Category.objects.get(slug=cat_name_slug)
            user = request.user
            content = request.POST.get('content')
            current_time = timezone.now()

            answer = Answers(
                category=cat,
                author=user,
                content=content,
                post_date=current_time,
                edit_date=current_time
            )
            answer.save()
            return HttpResponseRedirect('/rango/category/' + cat_name_slug)
        else:
            print "form.errors", editor_form.errors
            return_code = -1
    else:
        editor_form = TestUeditorModelForm()
        return_code = 0

    try:
        user = request.user
        if user.is_authenticated():
            user_id = user.id
        else:
            user_id = -1

        category = Category.objects.get(slug=cat_name_slug)
        answers = Answers.objects.filter(category=category).extra(
            select={
                'is_liked': 'select count(*) from rango_answeruserlikes where rango_answers.id = rango_answeruserlikes.answer_id and rango_answeruserlikes.user_id = ' + str(user_id)
            },
        ).extra(
            select={
                'is_disliked': 'select count(*) from rango_answeruserdislikes where rango_answers.id = rango_answeruserdislikes.answer_id and rango_answeruserdislikes.user_id = ' + str(user_id)
            },
        ).order_by("-likes")

        if user.is_authenticated():
            is_liked = CategoryUserLikes.objects.filter(category=category).filter(user=request.user)
        else:
            is_liked = None

        # like persons.
        is_answered = False
        for answer in answers:
            if answer.author == user:
                is_answered = True
            answer.user_id = answer.author.id
       
        context_dict['answers'] = answers
        context_dict['category'] = category
        context_dict['cat_name_slug'] = cat_name_slug
        context_dict['editor'] = editor_form
        context_dict['is_liked'] = is_liked
        context_dict['is_answered'] = is_answered
        context_dict['subject'] = category.subject
        context_dict['return_code'] = return_code

    except Category.DoesNotExist:
        context_dict = {}

    return render(request, 'rango/category.html', context_dict)
	
@login_required
def edit_answer(request, cat_name_slug, answer_id):
    answer = Answers.objects.get(id=int(answer_id))
    if answer.author == request.user:
        if request.method == 'POST':
            form = TestUeditorModelForm(request.POST)

            if form.is_valid():
                answer = Answers.objects.get(id=int(answer_id))
                content = request.POST.get('content')
                current_time = timezone.now()
                answer.content = content
                answer.edit_date = current_time
                answer.save()
                return HttpResponseRedirect('/rango/category/'+cat_name_slug)
        else:
            form = TestUeditorModelForm(
                initial={
                    'content': answer.content,
                }
            )
        context = {"form": form, "answer_id": answer_id, "cat_name_slug": cat_name_slug}
        return render(request, 'rango/edit-description.html', context)
    else:
        return HttpResponse("<h1>Don't do it, stupid!</h1>")
		
@login_required
def delete_answer(request):
    answer_id = None
    if request.method == 'GET':
        answer_id = request.GET['answer_id']
    return_code = -1
    if answer_id:
        answer = Answers.objects.get(id=int(answer_id))

        answer.delete()
        return_code = 1

    date = {"return_code": return_code}
    return JsonResponse(date)
	
def answer_up(request):
    likes_count = 0
    return_code = -1
    date = {}
    

    if request.method == 'GET':
        answer_id = request.GET['answer_id']
        if answer_id:
            user = request.user
            answer = Answers.objects.get(id=int(answer_id))
            current_time = timezone.now()

            answer_like = AnswerUserLikes(
                answer=answer,
                user=user,
                time=current_time
            )
            answer_like.save()

            user_dislike = AnswerUserDislikes.objects.filter(answer=answer).filter(user=user)
            if user_dislike.count() > 0:
                user_dislike.delete()

            likes = AnswerUserLikes.objects.filter(answer=answer)
            dislikes = AnswerUserDislikes.objects.filter(answer=answer)
            likes_count = likes.count() - dislikes.count()

            answer.likes = likes_count
            answer.save()

            return_code = 1
            print likes_count

    date["return_code"] = return_code
    date["likes_count"] = likes_count
    date["likes_person"] = get_answer_like_users(answer)
    return JsonResponse(date)
	
def answer_up_off(request):
    likes_count = 0
    return_code = -1
    date = {}

    if request.method == 'GET':
        answer_id = request.GET['answer_id']
        if answer_id:
            user = request.user
            answer = Answers.objects.get(id=int(answer_id))

            dislikes = AnswerUserDislikes.objects.filter(answer=answer)
            likes = AnswerUserLikes.objects.filter(answer=answer)

            user_likes = AnswerUserLikes.objects.filter(answer=answer).filter(user=user)
            user_likes.delete()

            likes_count = likes.count() - dislikes.count()
            answer.likes = likes_count
            answer.save()

            return_code = 1

    date["return_code"] = return_code
    date["likes_count"] = likes_count
    date["likes_person"] = get_answer_like_users(answer)

    return JsonResponse(date)
	
def answer_down(request):
    likes_count = 0
    return_code = -1
    date = {}

    if request.method == 'GET':
        answer_id = request.GET['answer_id']
        if answer_id:
            user = request.user
            answer = Answers.objects.get(id=int(answer_id))
            current_time = timezone.now()

            answer_dislike = AnswerUserDislikes(
                answer=answer,
                user=user,
                time=current_time
            )
            answer_dislike.save()

            user_like = AnswerUserLikes.objects.filter(answer=answer).filter(user=user)
            if user_like.count() > 0:
                user_like.delete()

            likes = AnswerUserLikes.objects.filter(answer=answer)
            dislikes = AnswerUserDislikes.objects.filter(answer=answer)
            likes_count = likes.count() - dislikes.count()

            answer.likes = likes_count
            answer.save()

            return_code = 1

    date["return_code"] = return_code
    date["likes_count"] = likes_count
    date["likes_person"] = get_answer_like_users(answer)

    return JsonResponse(date)


def answer_down_off(request):
    likes_count = 0
    return_code = -1
    date = {}

    if request.method == 'GET':
        answer_id = request.GET['answer_id']
        if answer_id:
            user = request.user
            answer = Answers.objects.get(id=int(answer_id))

            dislikes = AnswerUserDislikes.objects.filter(answer=answer)
            likes = AnswerUserLikes.objects.filter(answer=answer)

            user_dislikes = AnswerUserDislikes.objects.filter(answer=answer).filter(user=user)
            user_dislikes.delete()

            likes_count = likes.count() - dislikes.count()
            answer.likes = likes_count
            answer.save()

            return_code = 1

    date["return_code"] = return_code
    date["likes_count"] = likes_count
    date["likes_person"] = get_answer_like_users(answer)

    return JsonResponse(date)