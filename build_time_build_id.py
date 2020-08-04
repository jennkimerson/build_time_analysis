from connection import get_ceph_builds
import time
import datetime
import matplotlib.pylab as plt
import numpy as np

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

    # Update dictionary
    build_dict[build_id] = epoch_duration

# Build Duration by Brew Build ID

build_ord_dict = build_dict.items()
build_ord_list = list(map(list, build_ord_dict))

x, y = zip(*build_ord_dict)     # x = build_id, y = build_duration
x_ls = list(x)
y_ls = list(y)
# y_ls = pd.Series(y)

# Remove Outliers
outliers = []
index_outliers = []
x_r = []
y_r = []


def find_remove_outlier(data, list):
    threshold = 3
    mean = np.mean(data)
    std = np.std(data)

    index = 0
    for y in data:
        index += 1
        z_score = (y - mean) / std
        if np.abs(z_score) > threshold:
            outliers.append(y)
            index_outliers.append(index)
        else:
            y_r.append(y)
    # index_outliers.append(in_out)
    # in_out = in_out[::-1]
    return y_r


# Outliers removed for y
y_r = find_remove_outlier(y, build_ord_list)

# Outlliers removed for x
x_r = []
x_outliers = []
for i in range(len(x)):
    if i not in index_outliers:
        x_r.append(x[i])
    else:
        x_outliers.append(x[i])


def graph(x, y):
    plt.plot(x, y, c='b')
    plt.grid(True)
    plt.xlabel('build_id')
    plt.ylabel('build_duration')
    plt.title('Build Time Analysis')
    # plt.show()


def scatter(x, y):
    plt.scatter(x, y, s=5, c='r')


# Graph build
graph(x, y)
plt.show()

# # Graph with outliers removed and marked
scatter(x_outliers, outliers)
graph(x_r, y_r)     # x = build_id, y = build_duration
plt.show()
