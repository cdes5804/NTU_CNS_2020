#!/usr/bin/env python2
import re
from time import time
import sys

def menu():
    print '=============================='
    print '     CNS Grading Server       '
    print '=============================='
    print '     1. New student           '
    print '     2. HW grading            '
    print '     3. Check scores          '
    print '     4. Reset all scores      '
    print '     5. Exit                  '
    print '=============================='

def new_student(info, scores):
    print 'index of new student: {}'.format(len(info))
    print 'Student name: '
    name = raw_input('> ').strip()
    if not re.match(r'^[a-zA-Z]+(([\,\.\-][a-zA-Z])?[a-zA-Z]*)*$', name):
        print 'wrong name format'
        return
    print 'Student ID: '
    ID = raw_input('> ').strip()
    if not re.match(r'^[a-zA-Z][0-9]{2}[1-9ABEabe][0-9]{5}$', ID):
        print 'wrong id format'
        return
    print 'Student email: '
    email = raw_input('> ').strip()
    if not re.match(r'^[^@]+@(\w\.)+\w+$', email):
        print 'wrong email format'
        return

    new_entry = (name, ID, email)
    if new_entry not in info:
        info.append(new_entry)
        scores.append(dict())

def get_input(input_str):
    print input_str
    try:
        val = int(raw_input('> ').strip())
    except:
        return None
    return val

def grading(scores):
    idx = get_input('index of the student:')
    if idx == None or idx < 0 or idx >= len(scores):
        print 'Something is wrong'
        return

    hwID = get_input('homework id:')
    if hwID == None:
        print 'Something is wrong'
        return

    if (hwID not in scores[idx]) and (len(scores[idx]) > (1<<15)):
        print 'Too many homeworks QQ'
        return

    score = get_input('score:')
    if score == None or score < 0 or score > 100:
        print 'Something is wrong'
        return
    scores[idx][hwID] = score

def check_score(info, scores):
    idx = get_input('index of the student:')
    if idx == None or idx < 0 or idx >= len(scores):
        print 'Something is wrong'
        return

    hwID = get_input('homework id:')
    if hwID == None or hwID not in scores[idx]:
        print 'Something is wrong'
        return
    print 'student name: {}\nstudent id: {}\nstudent email: {}\nhomework id: {}\nscore: {}'.format(info[idx][0], info[idx][1], info[idx][2], hwID, scores[idx][hwID])

def reset_score(scores):
    idx = get_input('index of the student:')
    if idx == None or idx < 0 or idx >= len(scores):
        print 'Something is wrong'
        return

    all_hw = scores[idx].keys()
    for hw in all_hw:
        scores[idx][hw] = 0

def main():
    info = []
    scores = []
    while True:
        t = time()
        menu()
        cmd = raw_input('> ').strip()
        if cmd == '1':
            new_student(info, scores)
        elif cmd == '2':
            grading(scores)
        elif cmd == '3':
            check_score(info, scores)
        elif cmd == '4':
            reset_score(scores)
        elif cmd == '5':
            exit(0)
        else:
            print 'Unknown command'
        print >> sys.stderr, time() - t


if __name__ == '__main__':
    main()
