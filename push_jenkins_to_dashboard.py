# -*- coding:utf8 -*-
import urllib
import urllib2
import cookielib
import re
import sys
import os

from datetime import datetime
# from collections import defaultdict
from lxml import etree
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage,QWebSettings
from tempfile import NamedTemporaryFile
import cgi

_AUTH_URL = 'http://10.140.23.32:8090/j_acegi_security_check'
WEB_HOST = 'http://microrec3gci.china.nsn-net.net:8090'
_USER = '*'  # NSN-intra user name
_PASSWORD = '*'  # NSN-intra password
VIEW_URL = ['/view/LRC_CR', '/view/LRC_Robot_CR1-TL42/']
# POST_URL = 'http://10.140.23.32:9080/LRCDashboard/regressionCase/save'
# STAT_URL = 'http://10.140.23.32:9080/LRCDashboard/execution/stat'
POST_URL = 'http://localhost:8080/LRCDashboard/regressionCase/save'
STAT_URL = 'http://localhost:8080/LRCDashboard/execution/stat'
BASE_DIR = 'D:/TA_Case_Log_Root/CR_load_Version'


JOB_PREFIX_LEN = 4
FEATURES_TO_COLLECT = 4
CASE_OWNERS = ['liugeng', 'chenqian', 'zhujing', 'shenxianqing', 'ningfeng', 'wangdali', 'guanguozhu',
               'youxingkai', 'liuxiaoyi', 'chenxuefen', 'lisading', 'shenxueli', 'wangjia', 'jiangwei',
               'chenliang','daixiangying', 'chengshuitian', 'tangjiayi', 'yangchunjian', 'licaihua', 'lvjia',
               'chenyu', 'yihao', 'houyuguo']

# hh:mm:ss.ms -> %.1f min
str_to_min = lambda x: int(x.split(':')[0])*60+int(x.split(':')[1])+float('%.1f' % (float(x.split(':')[2])/60))

# local files that store generated report html
urls = []
remote_urls = []
exec_times = []
test_lines = []
job_names = []
job_features = []


def get_load_info():
    host_load_dict = {}
    # files = os.listdir(BASE_DIR)
    # for f in files:
    #     with open(os.path.join(BASE_DIR,f)) as fds:
    #         host_load_dict[f[:-4]] = fds.read().strip()
    return host_load_dict


host_load_dict = get_load_info()


def _web_page(request_url):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    post_data = urllib.urlencode({  'j_username':_USER,
                                    'j_password': _PASSWORD,
                                    'from':request_url,
                                    'json':'{"j_username": "%s", "j_password": "%s", \
                                    "remember_me": false, "from": "%s"}' % (_USER, _PASSWORD, request_url),
                                    'Submit':'登录'})
    req = urllib2.Request(_AUTH_URL, post_data)
    res = opener.open(req)
    try:
        raw_data = res.read()
    finally:
        res.close()
    return raw_data


def _push_data(url, data):
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(url, encoded_data)
    urllib2.urlopen(request)


class Render(QWebPage):
    def __init__(self, urls, cb):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        s = self.settings()
        s.setAttribute(QWebSettings.AutoLoadImages, False)
        s.setAttribute(QWebSettings.LinksIncludedInFocusChain, False)
        s.clearMemoryCaches()
        self.loadFinished.connect(self._loadFinished)
        self.urls = urls
        self.cb = cb
        self.crawl()
        self.app.exec_()
      
    def crawl(self):
        if self.urls:
            url = self.urls.pop(0)
            self.mainFrame().load(QUrl(url))
        else:
            self.app.quit()
        
    def _loadFinished(self, result):
        frame = self.mainFrame()
        url = str(frame.url().toString())
        html = unicode(frame.toHtml())
        self.cb(html)
        # print html.encode('utf-8')
        print
        os.remove(url.split('/')[-1].split('#')[0])
        self.crawl()


def get_jobs_from_jenkins(view_url):
    feature_jobs = {}
    html = _web_page(view_url)
    page = etree.HTML(html.decode('utf-8'))

    for i in range(FEATURES_TO_COLLECT):
        feature_name = page.xpath(u"//h2")[i].text
        trs = page.xpath(u"//div[@class='pane']/div[position()=%d]/div/table/*" % (i+1))[1:]
        feature_jobs[feature_name] = [tr.attrib['id'][JOB_PREFIX_LEN:] for tr in trs]
    return feature_jobs


def get_cases_in_job(view_url, job, feature):
    print job, feature

    req_job_url = '%s/job/%s/robot' % (view_url, job)
    try:
        robot_test_results = etree.HTML(_web_page(req_job_url).decode('utf-8'))
    except urllib2.HTTPError:
        return
    job_url = robot_test_results.xpath(u"//td[@id='top-panel']/table/tr/td[position()=2]/form")[0].attrib['action'][:-len('search/')]
    if job_url[-7:] != '/robot/':
        return
    exec_time_str = robot_test_results.xpath(u"//div[@style='float:right;']/text()")[0].strip().split()
    exec_time = exec_time_str[2] + exec_time_str[3].split(':')[0]
    re_TL = '^Building remotely on LRC_[^0-9]*([.0-9]+) in workspace'
    test_line = re.search(re_TL,_web_page(job_url.replace('robot', 'consoleText')),re.MULTILINE).group(1)

    try:
        report_page = _web_page(job_url+'report/report.html#totals?all')
    except urllib2.HTTPError:
        return

    with NamedTemporaryFile(mode='w', suffix='.html', dir='.', delete=False) as f:
        f.write(report_page)
        f.flush()
        urls.append(os.path.basename(f.name)+'#totals?all')

    job_names.append(job)
    remote_urls.append(job_url+'report/')
    job_features.append(feature)
    exec_times.append(exec_time)
    test_lines.append(test_line)

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text)]

def scrape(html):
    ru, job, feature, exec_time, test_line = map(lambda x:x.pop(0), [remote_urls, job_names, job_features, exec_times, test_lines])
    report_page = etree.HTML(html)
    case_comments = []
    ts_list = []

    case_names = filter(lambda x: ' . ' not in x, report_page.xpath(u'//td[@class="details-col-name"]/div/a//text()'))
    hrefs = map(lambda x: x.attrib['href'], report_page.xpath(u'//td[@class="details-col-name"]/div/a'))
    candidate_ts = report_page.xpath(u'//td[@class="details-col-times"]/div/text()')[::2]
    case_links = map(lambda x: WEB_HOST+ru+x, hrefs)
    



    # f = open('rpt.html')

    big_str = _web_page(ru+hrefs[0])
    # big_str = f.read()
    starts = ['"*%s"' % cgi.escape(n) for n in case_names]
    # sort names according by sequence in log.html
    starts = [starts[i] for i in sorted(range(len(hrefs)), key=lambda k: natural_keys(hrefs[k]))]
    ends = starts[1:] + ['window.output["stats"]']
    for s,e in zip(starts, ends):
        chunk_str = big_str[big_str.find(s): big_str.find(e)]
        print s, e
        print big_str.find(s), big_str.find(e)
        big_str = big_str[big_str.find(e):]
        match_list = re.findall('"\*\$\{third_level\} = ([^"]+)"', chunk_str, re.S)
        ts_list.append(match_list and match_list[0] or '')
    print case_names
    print ts_list
    print [sorted(hrefs).index(h) for h in hrefs]
    print candidate_ts

    case_ts = [ts_list[i] for i in [sorted(hrefs, key=lambda k:natural_keys(k)).index(h) for h in hrefs]]

    case_tags = report_page.xpath(u'//td[@class="details-col-tags"]/div/text()')
    case_owners = map(lambda x: filter(lambda y: y in CASE_OWNERS, map(lambda z: z.lower().replace(' ',''),x.split(', '))), case_tags)
    case_status = report_page.xpath(u'//td[@class="details-col-status"]/div/span/text()|//td[@class="details-col-status"]/div/text()')

    for i in range(1, len(report_page.xpath(u'//td[@class="details-col-msg"]'))+1):
        case_comments.append(''.join(report_page.xpath(u'//td[@class="details-col-msg"][position()=%d]/descendant::*/text()' % i)))

    case_duration = map(str_to_min, report_page.xpath(u'//td[@class="details-col-elapsed"]/div/text()'))

    for i,t in enumerate(case_ts):
        if not t:
            s1 = candidate_ts[i][:-4].replace(':','-').replace(' ','_')
            case_ts[i] = s1[:4]+'-'+s1[4:6]+'-'+s1[6:]
        else:
            case_status[i] = case_status[i] == 'PASS' and 'PASS/Pending' or case_status[i]

    # post_value = {}
    if not case_owners:
        case_owners = ['-']
    else:
        case_owners = [o if o else '-' for o in case_owners]
    # print len(case_comments), len(case_owners), case_ts
    for n, l, s, d, c, o, t in zip(case_names, case_links, case_status, case_duration, case_comments, case_owners, case_ts):
        print "test_line    ", test_line
        print "feature_name ", feature
        print "job_name     ", job
        print "case_name    ", n
        print "case_owner   ", len(o) and o[0] or '-'
        print "exec_time    ", t
        print "case_status  ", s
        print "case_duration", d
        print 'targetLoad   ', host_load_dict.get(test_line, '-')
        print 'comment      ', len(c)
        print "link         ", l
        print
        # post_value['caseName'] = n
        # post_value['featureName'] = feature
        # post_value['caseOwner'] = len(o) and o[0] or '-'
        # post_value['status'] = s=='PASS' and "PASS" or "FAIL"
        # post_value['runningTL'] = test_line
        # post_value['failureReason'] = c
        # post_value['targetLoad'] = host_load_dict.get(test_line, '-')
        # post_value['lastRunTime'] = t
        # post_value['duration'] = d
        # post_value['link'] = l
        # _push_data(POST_URL, post_value)


# for uv in VIEW_URL:
#     for feature, js in get_jobs_from_jenkins(uv).items():
#        for j in js:
#            get_cases_in_job(uv, j, feature)
           # break


# get_cases_in_job('LRC_CR','LRC_CP_HSUPA_feature_CR_TL42','CP_HSUPA_Feature')

# all pass
get_cases_in_job('/view/LRC_Robot_CR1-TL42','LRC_CP_Legacy_feature_CR_Single_RAN2799_TL42','CP_Legacy_Feature')
# get_cases_in_job('/view/LRC_CR','LRC_CP_Transition_feature_CR_TL42','CP_Transition')
# get_cases_in_job('/view/LRC_Robot_CR1-TL42','LRC_CP_Legacy_feature_CR_Single_RAN2804_TL42','CP_Legacy_Feature')
# get_cases_in_job('LRC_Robot_CR1-TL42','LRC_CP_Legacy_feature_CR_Single_RAN2797_TL42','CP_Legacy_Feature')
# get_cases_in_job('LRC_CR','RAN2976_Softer_Handover_Stability_Cplane_TC96','CP_New_Feature')



# get_cases_in_job('LRC_New_Feature_RAN2976_TC1','abc')
#urls = ['tmpeP2pTb.html#totals?all']#,'tmpoPktou.html#totals?all']
Render(urls, cb=scrape)

# update execution info if today is monday
if not datetime.today().weekday():
    urllib2.urlopen(urllib2.Request(STAT_URL))
