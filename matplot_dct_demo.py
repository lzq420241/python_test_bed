import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from time import strptime
from time import mktime
from datetime import datetime


plt.close('all')
def dct_convert_log_to_dict(dct_log_path):
    log_list = []
    log_dict = {}
    with open(dct_log_path) as log_content:
        #remove first line
        fline = log_content.readlines()[1:]
        listline = [line for line in fline if line.strip()]
    for item in listline:
        category = item.split('\t')
        log_list.append(category)

    log_list_title = log_list[0]
    log_list = log_list[2:-1]
    list_value = zip(*log_list)

    for i in range(len(log_list_title)):
        log_dict[log_list_title[i]] = list_value[i]
    return log_dict

log_path = '/Users/liziqiang/Desktop/130102_000325_BTS_HSCHDATSND_01000_0001.log'
log_dict = dct_convert_log_to_dict(log_path)

#print log_dict.keys()


x = map(lambda x: datetime.strptime(x, '%H:%M:%S.%f'), log_dict['Time'])
#print x


sfn = log_dict['SFN']
if 'Sub-Frame Number' in log_dict.keys():
    sub_frame = log_dict['Sub-Frame Number']
    y1 = map(lambda x: int(x[0])+(int(x[1])+1)*0.2, zip(sfn, sub_frame))
#print y1
y2 = log_dict['HS-PDSCH assignable transmission power#0']

#plt.rc('axes', grid=True)
#plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
textsize = 9
left, width = 0.1, 0.8
rect1 = [left, 0.5, width, 0.4]
rect2 = [left, 0.1, width, 0.4]


fig = plt.figure(facecolor='white')
axescolor = '#f6f6f6' # the axes background color
ax1 = fig.add_axes(rect1, axisbg=axescolor) #left, bottom, width, height 
ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
ax1.get_xaxis().get_major_formatter().set_useOffset(False)
print ax1.get_xlim(), x[0], x[-1]

# locator = mdates.AutoDateLocator()
# locator.intervald[SECONDLY] = [30]
ax1.xaxis.set_major_locator(mdates.SecondLocator(interval=5))
ax1.xaxis.set_minor_locator(mdates.SecondLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
y_max = max(map(float,y2)) + 0.1
y_min = min(map(float,y2)) - 0.1

print y_min, y_max
# ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%S'))
#ax1.set_xlim(x[0], x[-1])
ax2.set_ylim(y_min, y_max)


ax1.plot(x, y1, 'b-')
ax2.plot(x, y2, 'r-')
plt.show()