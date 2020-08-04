import psycopg2 as pp
import psycopg2.extras as ppx
import time, datetime

conn = pp.connect(dbname='public', host='virtualdb.engineering.redhat.com', port=5433)
cur = conn.cursor(cursor_factory=ppx.DictCursor)
# Some builds do not have a start_time, so we will also query the
# creation_time from the events table.
postgreSQL_select_Query = """SELECT brew.build.*,brew.events.time 
                                AS creation_time FROM brew.build 
                                INNER JOIN brew.events ON brew.build.create_event=brew.events.id 
                                WHERE brew.build.pkg_id=34590 and brew.build.state = 1
                                ORDER BY brew.events.id;"""

cur.execute(postgreSQL_select_Query)

# Selecting rows from brew.build table using cursor.fetchall
current = cur.fetchall()

for row in current:
    # Data has start_time
    print("id               = ", row['id'])
    print("pkg_id           = ", row['pkg_id'])
    print("version          = ", row['version'])
    print("release          = ", row['release'])
    
    # print("start_time  = ", row[11])
    # print("completion_time  = ", row[6], "\n")
    
    # Convert time stamp to unix time
    p = '%Y-%m-%d %H:%M:%S.%f'
    temp_c = str(row['completion_time'])
    epoch_complete = time.mktime(datetime.datetime.strptime(temp_c, p).timetuple())

    if row['start_time'] is not None:
        temp_s = str(row['start_time'])
        epoch_start = time.mktime(datetime.datetime.strptime(temp_s, p).timetuple())
        print("start_time       = ", epoch_start)
        
        print("completion_time  = ", epoch_complete)
        
    # Calculate time duration, delta
        print("build_duration   = ", float(epoch_complete) - float(epoch_start), "\n")

    elif row['start_time'] is None:
        print("No start_time time stamp, replacing with creation_time")
        # print("creation_time = ", item[15], "\n")

        temp_t = str(row['creation_time'])
        epoch_creation = time.mktime(datetime.datetime.strptime(temp_t, p).timetuple())
        print("start_time    = ", epoch_creation)

        print("completion_time  = ", epoch_complete)
        
    # Calculate time duration, delta
        print("build_duration   = ", float(epoch_complete) - float(epoch_creation), "\n")

# Print ones without start_time seperately from the rest
# for row in current:
#     # Data has start_time
#     print("id               = ", row[0])
#     print("pkg_id           = ", row[1])
#     print("version          = ", row[2])
#     print("release          = ", row[3])
#     # print("start_time  = ", row[11])
#     # print("completion_time  = ", row[6], "\n")

#     if row[11] is not None:
#     # Convert time stamp to unix time
#         p = '%Y-%m-%d %H:%M:%S.%f'

#         temp_s = str(row[11])
#         epoch_start = time.mktime(datetime.datetime.strptime(temp_s, p).timetuple())
#         print("start_time       = ", epoch_start)

#         temp_c = str(row[6])
#         epoch_complete = time.mktime(datetime.datetime.strptime(temp_c, p).timetuple())
#         print("completion_time  = ", epoch_complete)
        
#     # Calculate time duration, delta
#         print("build_duration   = ", float(epoch_complete) - float(epoch_start), "\n")

# for item in current:
#     # Data is missing start_time, instead use creation_time
#     if item[11] is None:
#         print("id               = ", item[0])
#         print("pkg_id           = ", item[1])
#         print("version          = ", item[2])
#         print("release          = ", item[3])
#         print("No start_time time stamp")
#         # print("creation_time = ", item[15], "\n")
        
#         # Convert time stamp to unix time
#         p = '%Y-%m-%d %H:%M:%S.%f'

#         temp_t = str(item[15])
#         epoch_creation = time.mktime(datetime.datetime.strptime(temp_t, p).timetuple())
#         print("creation_time    = ", epoch_creation)

#         temp_c = str(item[6])
#         epoch_complete = time.mktime(datetime.datetime.strptime(temp_c, p).timetuple())
#         print("completion_time  = ", epoch_complete)
        
#     # Calculate time duration, delta
#         print("build_duration   = ", float(epoch_complete) - float(epoch_creation), "\n")