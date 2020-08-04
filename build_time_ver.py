from connection import get_ceph_builds
import time
import datetime
import matplotlib.pylab as plt
import numpy as np
from pylab import text

current = get_ceph_builds()

# Initialize dictionary
build_dict = {}
ver_dict = {}


# Convert completion_time
def convert_to_unix(time_stamp):
    p = '%Y-%m-%d %H:%M:%S.%f'
    epoch = time.mktime(datetime.datetime.strptime(str(time_stamp), p).timetuple())
    return epoch


def output_time(epoch_s, epoch_c):
    epoch_start = convert_to_unix(epoch_s)
    print("start_time       = ", epoch_start)

    epoch_complete = convert_to_unix(epoch_c)
    print("completion_time  = ", epoch_complete)

    epoch_duration = float(epoch_complete) - float(epoch_start)
    print("build_duration   = ", epoch_duration, "\n")
    return epoch_duration


for row in current:
    print("id               = ", row['id'])
    build_id = row['id']
    # print("pkg_id           = ", row['pkg_id'])
    print("version          = ", row['version'])
    version = row['version']
    print("release          = ", row['release'])

    # Time Stamps
    # print("start_time  = ", row['start_time'])
    # print("completion_time  = ", row['completion_time], "\n")

    # Data has start_time
    if row['start_time'] is not None:
        epoch_duration = output_time(row['start_time'], row['completion_time'])

    # Data does not have start_time, therefore will use creation_time instead
    elif row['start_time'] is None:
        # print("No start_time time stamp, replacing with creation_time")
        epoch_duration = output_time(row['creation_time'], row['completion_time'])

    # Merging versions
    ver_main = version.split('.', 1)[0]
    ver_dict.setdefault(ver_main, []).append(epoch_duration)

# Check key, value pair for ver_dict
print("Show Build Per Version: ")
for key, value in ver_dict.items():
    print(key, len([item for item in value if item]))


def scatter(dict):
    ord_dict = dict.items()
    ord_list = list(map(list, ord_dict))
    x, y = zip(*ord_list)
    for x_ls, y_ls in zip(x, y):
        plt.scatter([x_ls] * len(y_ls), y_ls)
    plt.show()

# Scatter Plot - Build Duration by Version
# scatter(ver_dict)


def boxplot(dict):
    ord_dict = dict.items()
    x, y = [*zip(*ord_dict)]
    x = dict.keys()
    y = dict.values()

    # Format graph
    plt.figure(figsize=(10, 8))
    plt.grid(True)
    # plt.title('Build Time Analysis')
    plt.xlabel('version')
    plt.ylabel('build_duration (seconds)')
    bp_dict = plt.boxplot(y, showfliers=False)      # Remove outliers
    # plt.boxplot(y)                                # Include outliers

    # Median Values
    median_lst = []
    delta_lst = [0]
    current = 0

    for line in bp_dict['medians']:
        j, k = line.get_xydata()[0]
        median = text(j, k, '%.1f' % k, va='baseline')
        med_val = float(str(median).split(',')[1])
        median_lst.append(med_val)
        if current == 0:   # base case: there's only 1 median so delta cannot be calculated, thus insert 0
            text(j, k, '            (0)' % k, va='baseline')
        else:
            # delta = previous - current values
            delta_lst = list(np.diff(median_lst))
            text(j, k, f'            ({delta_lst[current - 1]})' % k, va='baseline')
        current += 1

    print("Median Values of Build Time of Each Versions: ", median_lst)
    print("Deltas:                                       ", delta_lst)
    plt.xticks(range(1, len(x) + 1), x)
    plt.show()


# Box Plot - Build Duration by Version
boxplot(ver_dict)
