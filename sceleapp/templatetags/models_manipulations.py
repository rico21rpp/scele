from django import template
from sceleapp.models import UserPost, UserReply, ReplyLike, GivenReplyLike, Badge, UserBadge
from django.templatetags.static import static
from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter(name="get_creator")
def get_creator_name(value):
    tags = '<p>' + str(value.creator.get_full_name()) + '</p>'
    return value.creator.get_full_name()

@register.filter(name="get_fullname")
def get_fullname(value):
    return value.get_full_name()

@register.filter(name="get_replies")
def get_replies(value):
    # if value is UserPost:
    if type(value) is UserPost:
        return UserReply.objects.filter(user_post=value)
    return UserReply.objects.filter(host_reply=value)

@register.filter(name="get_replies_size")
def get_replies_size(value):
    replies = get_replies(value)
    replies_size = replies.count()
    if replies_size > 0:
        for reply in replies:
            replies_size += get_replies_size(reply)
    return replies_size

@register.filter(name="get_last_reply")
def get_last_reply(value):
    replies = UserReply.objects.filter(user_post=value)
    last_reply = replies.last()
    deepest = []
    for rep in replies:
        deepest = get_deepest_replies(deepest, rep)
    for reply in deepest:
        if reply.created_at > last_reply.created_at:
            last_reply = reply
    return last_reply

def get_deepest_replies(deepest_replies, rep):
    replies = UserReply.objects.filter(host_reply=rep)
    if replies.count() == 0:
        deepest_replies.append(rep)
    else:
        for reply in replies:
            get_deepest_replies(deepest_replies, reply)
    return deepest_replies

@register.filter(name="get_last_user")
def get_last_activity_user_fullname(value):
    if get_replies_size(value) == 0:
        return value.creator.get_full_name()
    else:
        return get_last_reply(value).creator.get_full_name()

def format_created_at(value):
    created_at = timezone.localtime(value.created_at, timezone.get_fixed_timezone(420))
    formatedDate = created_at.strftime("%B %d, %Y, %H:%M")
    return formatedDate

@register.filter(name="get_last_updated")
def get_last_updated(value):
    if get_replies_size(value) == 0:
        return format_created_at(value) + " WIB"
    else:
        last_reply_created_at = get_last_reply(value)
        return format_created_at(last_reply_created_at) + " WIB"

@register.filter(name="get_replies_tags")
def get_replies_tags(value, active_user):
    tags = ''
    for reply in value:
        tags += get_reply_box(reply, active_user)
    return tags

def add_indent(tags):
    indented_tags = '<div class="indent">' + tags + "</div>"
    return indented_tags

def get_post(reply):
    if reply.user_post:
        return reply.user_post
    else:
        return get_post(reply.host_reply)

def has_liked(user, reply):
    replylike = ReplyLike.objects.get(user_reply=reply)
    try:
        user_has_liked = GivenReplyLike.objects.get(reply_like=replylike, liker=user)
        return True
    except ObjectDoesNotExist:
        return False

def get_reply_box(reply, active_user):
    profile_url = reverse('profile')
    profile_img = static('img/user-icon.png')
    reply_obj = reply.obj
    created_at = timezone.localtime(reply_obj.created_at, timezone.get_fixed_timezone(420))
    formatedDate = created_at.strftime("%B %d, %Y, %H:%M")
    creator = reply_obj.creator
    creator_fulname = creator.get_full_name()
    user_fullname = active_user.get_full_name()
    is_gamified = reply_obj.is_gamified
    parent = reply.parent
    post = get_post(reply_obj)
    reply_url = reverse('addreply', kwargs={'post_id': post.id, 'parent_type': '1', 'parent_id': reply_obj.id})
    edit_reply_url = reverse('edit-reply', kwargs={'id': reply_obj.id})
    try:
        total_likes = ReplyLike.objects.get(user_reply=reply_obj).quantity
        user_has_liked = has_liked(active_user, reply_obj)
    except ObjectDoesNotExist:
        total_likes = 0
        user_has_liked = False
    
    tags = '<div class="box-item" id="' + str(reply.comp_id) + '">' + \
                '<div class="box-item__main-content">'
    
    if creator == active_user:
        tags += '<a class="user-icon-area" href="' + str(profile_url) + '">' + \
                    '<img src="' + str(profile_img) + '" alt="user-icon">' + \
                '</a>'
    else:
        tags += '<img src="' + str(profile_img) + '" alt="user-icon">'

    tags += '<div class="box-item__content">' + \
                '<div id="box-item__content__header">' + \
                    '<p class="font-bold">' + str(reply_obj.subject) + '</p>' + \
                        '<p>by <span>'

    if creator == active_user:
        tags += '<a href="' + str(profile_url) + '">' + user_fullname + '</a>'
    else:
        tags += creator_fulname
    
    tags += '</span> - ' + str(formatedDate) + ' WIB</p></div>' + \
            '<div class="box-item__content__msg">' + str(reply_obj.msg) + '</div></div></div>'

    # footer
    if is_gamified:
        tags += '<div class="box-item__content__footer">'
    else:
        tags += '<div class="box-item__content__footer extra-padding-bottom">'

    if is_gamified:
        if total_likes > 1:
            likes_counter = '<a href="" class="likes-count" data-obj_id="' + str(reply_obj.id) + '" data-toggle="modal" data-target="#likersModal">' + str(total_likes) + ' likes</a>'
        elif total_likes == 1:
            likes_counter = '<a href="" class="likes-count" data-obj_id="' + str(reply_obj.id) + '" data-toggle="modal" data-target="#likersModal">1 like</a>'
        else:
            likes_counter = '<a href="" class="likes-count hidden" data-obj_id="' + str(reply_obj.id) + '" data-toggle="modal" data-target="#likersModal">0 like</a>'
        tags += likes_counter
    
    tags += '<div class="right"><a href="#'

    if type(parent) is UserPost:
        tags += 'post-item'
    else:
        # parent_comp_id = 'rep-' + str(reply.lv - 1) + '-' + str(parent.id)
        parent_comp_id = str(parent.id)
        tags += parent_comp_id
    
    tags += '">Show Parent</a> | '

    if is_gamified:
        if user_has_liked:
            tags += '<a href="" class="btn-like liked" data-obj_id="' + str(reply_obj.id) + '">Unlike</a> | '
        else:
            tags += '<a href="" class="btn-like" data-obj_id="' + str(reply_obj.id) + '">Like</a> | '
    
    if is_updateable(reply_obj) and creator == active_user:
        tags += '<a href="' + str(edit_reply_url) + '" class="btn-edit" data-obj_id="' + str(reply_obj.id) + '">Edit</a> | ' + \
                        '<a href="" class="btn-delete" data-obj_id="' + str(reply_obj.id) + '">Delete</a> | '

    tags += '<a href="' + str(reply_url) + '">Reply</a></div></div></div>'
    
    for i in range(reply.lv):
        tags = add_indent(tags)

    return tags

@register.filter(name="list_size")
def get_list_size(value):
    return len(value)

@register.filter(name="is_updateable")
def is_updateable(value):
    now = timezone.now()
    selisih = now - value.created_at
    max_delta = timedelta(minutes=30)
    return selisih <= max_delta
    


################ NOTIF AREA ################

@register.filter(name="get_formatted_time")
def get_formatted_time(value):
    now = timezone.now()
    minute = timedelta(seconds=60)
    hour = timedelta(minutes=60)
    hours10 = timedelta(hours=10)
    day = timedelta(hours=24)
    days10 = timedelta(days=10)
    selisih = now - value
    selisih_int = 0

    if selisih < minute:
        selisih_int = int(str(selisih)[5:7])
        return '{0} detik yang lalu'.format(selisih_int)
    elif selisih < hour:
        selisih_int = int(str(selisih)[2:4])
        return '{0} menit yang lalu'.format(selisih_int)
    elif selisih < hours10:
        selisih_int = int(str(selisih)[:1])
        return '{0} jam yang lalu'.format(selisih_int)
    elif selisih < day:
        selisih_int = int(str(selisih)[:2])
        return '{0} jam yang lalu'.format(selisih_int)
    elif selisih < days10:
        selisih_int = int(str(selisih)[:1])
        return '{0} hari yang lalu'.format(selisih_int)
    else:
        selisih_int = int(str(selisih)[:2])
        return '{0} hari yang lalu'.format(selisih_int)

@register.filter(name="is_issued_to_me")
def is_issued_to_me(value, active_user):
    user_badges = UserBadge.objects.filter(badge=value)
    if user_badges.count() > 0:
        for user_badge in user_badges:
            if user_badge.owner == active_user:
                return True
    return False