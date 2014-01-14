import pdb
import datetime
from tempfile import mkstemp
from shutil import move
from os import remove, close

from django.contrib import messages

from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext

from notifications.models import Notification

def mark_read(receiver_id, timestamp):
    """
    Marks a notification of receiver_id and timestamp as read
    """
    pathname = 'notifications/notification_logs/' + str(receiver_id) + '.txt'
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(pathname)
    for line in old_file:
        if timestamp in line:
            unline = line.split('~')
            unline[5] = '0'
            reline = "~".join(unline)
            new_file.write(reline)
        else:
            new_file.write(line)
    new_file.close()
    close(fh)
    old_file.close()
    remove(pathname)
    move(abs_path, pathname)

def view_notifications(request):
    """
    Displays the first 10 most recent notifications a user has and
    initializes the counter variable to 2 so that view_more displays 
    notifications in multiples of 10.
    """
    n_list = get_latest_notifications(request.user.id, 10)
    context = RequestContext(request, {
            'notification_list': n_list,
            'counter': 2,
    })
    if n_list == None:
        messages.error(request, 'There are no messages in your inbox!')
    else:
        for n in n_list:
            if n.not_type == 1 or n.not_type == 3:
                pass
            else:
                mark_read(n.receiver_id, str(n.timestamp))

    return render(request, 'notifications/view.html', context)

def view_more(request, counter):
    """
    Displays more than 10 notifications, in multiples of 10
    """
    n_list = get_latest_notifications(request.user.id, int(counter)*10)
    counter = int(counter) + 1
    context = RequestContext(request, {
            'notification_list': n_list,
            'counter': counter
    })

    for n in n_list:
        if n.not_type == 1 or n.not_type == 3:
            pass
        else:
            mark_read(n.receiver_id, str(n.timestamp))


    return render(request, 'notifications/view.html', context)

def get_latest_notifications(receiver_id, numberof):
    """
    Gets the most recent 'numberof' notifications for a specified receiver_id
    based on timestamp 
    """
    pathname = 'notifications/notification_logs/' + str(receiver_id) + '.txt'
    notification_list = []
    i = 0
    try:
        with open(pathname, 'r') as f:
            for line in f:
                if i >= numberof:
                    return notification_list

                ids = line.split('~')

                n = Notification(int(ids[0]), int(ids[1]), int(ids[2]), ids[3], ids[4], int(ids[5]), ids[6], \
                    ids[7], ids[8], ids[9], ids[10], ids[11], ids[12])
                notification_list.append(n)

                i+=1
            notification_list.reverse()
            return notification_list

    except IOError:
        return None

def count_unread(receiver_id):
    """
    Counts the number of unread notifications for user with receiver_id
    """
    pathname = 'notifications/notification_logs/' + str(receiver_id) + '.txt'
    notification_list = []
    unread = 0
    try:
        with open(pathname, 'r') as f:
            for line in f:

                ids = line.split('~')

                if ids[5] == '1':
                    unread += 1


            return unread

    except IOError:
        return None

def log_notification(notification):
    """
    Logs a notification to a text file
    Text file will follow naming convention '<user_id>.txt' eg '0.txt' and '1.txt'
    """
    pathname = 'notifications/notification_logs/' + str(notification.receiver_id) + '.txt'
    try:
        with open(pathname, 'a') as f:
            not_type = str(notification.not_type)
            r_id = str(notification.receiver_id)
            s_id = str(notification.sender_id)
            t_id = str(notification.tool_id)
            sh_id = str(notification.shed_id)
            message = str(notification.message)
            timestamp = str(notification.timestamp)
            return_date = str(notification.return_date)
            read = str(notification.read)

            r_string = str(notification.receiver_string)
            s_string = str(notification.sender_string)
            t_string = str(notification.tool_string)
            sh_string = str(notification.shed_string)

            write_string = not_type + '~' + r_id + '~' + s_id + '~' + t_id \
                           + '~' + sh_id + '~' + read + '~' + timestamp \
                           + '~' + return_date + '~' + r_string + '~' \
                           + s_string + '~' + t_string + '~' + sh_string + '~' + \
                           message + '\n'
            f.write(write_string)


    except IOError:
        return HttpResponse('File IO error')

