# [Toy Project NYSCEC]
# 0.1.2va, 20.07.31. First launched.
# written by acoustikue(SukJoon Oh)
# 
# Legal stuff:
#   This simple code follows MIT license. 
# 
# MIT License
# Copyright (c) 2020 SukJoon Oh(acoustikue)

import config as cf
import json
import os

# Original source uses MongoDB for course changelogs. 
# For the Github Action, it will use just a simple file
# using json form, with the same structure used in the DB.
# Thus, unnecessary lines were removed from the original NYSCEC2.

# Newly updated
# V3
def generate_notification_item(target):

    notify_this = {
        'name': '',
        'instances': [],
        'posts': []
    }

    db_file_name = '{0}{1}.json'.format(cf.NYSCEC3_DB_BASE, target['name'])
    # print(db_file_name)

    # Check if the json file exists.
    if os.path.exists(db_file_name):
        # Case when exists
        old = 0

        with open(db_file_name, "r") as db_file:
            old = json.load(db_file)

        # print(old)

        notify_this['name'] = target['name']

        # Compare the instances
        for instance in target['instances']:
            if instance in old['instances']: pass
            else:
                notify_this['instances'].append(instance)
                # old['instances'].append(instance)
        
        for post in target['posts']:
            if post in old['posts']: pass
            else:
                notify_this['posts'].append(post)
                # old['posts'].append(instance)

        # When existing information is completely identical with the new one
        if len(notify_this['instances']) == 0 and len(notify_this['posts']) == 0:
            notify_this = None

        else:
            old['instances'].extend(notify_this['instances'])
            old['posts'].extend(notify_this['posts'])

        with open(db_file_name, 'w') as db_file:
            json.dump(old, db_file, indent=4)


    else: # When the file does not exist, then it is the new course.
        with open(db_file_name, 'w') as db_file:
            json.dump(target, db_file, indent=4)

        notify_this = target

    return notify_this


if __name__ == '__main__':
    pass




