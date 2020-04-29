# /usr/bin/python 3.6  
# -*-coding:utf-8*-


'''
Utility Functions to Refer

Usage in other scripts:

import utils
utils.function_name(args)
'''

import os
import pandas as pd
import re
import numpy as np
from datetime import datetime, timedelta
import collections
import calendar


###################################
## multiprocess examples
## Author: Jing Wang 

# import multiprocess
# # avoid runtime error 
# multiprocessing.freeze_support()
# # count cpus 
# cpus = multiprocessing.cpu_count()

def str2unicode(x):
	'''
	arg: chinese charater with string format such as '东莞'

	output: chinese charater with unicode format
	'''
	x = x.decode("utf-8")
	return x


def multiThread():
	# build multi-process object
	p = multiprocessing.Pool(processes=cpus)
	results = []

	# loop
	for _ in range(1000):
		## build arguments
		arg = None
		res = p.apply_async(func=func, args=(arg,))

		## save output
		results.append(res)

	# close processor
	p.close()
	p.join()

	# to get results
	for r in results:
		'''
		write your own codes

		r.get() return the result 
		'''
		print(r.get())


####################################
# outlier remove 
# Author: Jing Wang
def removeOutlier(data):
	'''
	Outlier Detect Reference Link:
	http://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm

	Use Modified Z-score and all data


	Args:
	data (arrary like)

	Return:
	result (list)

	Raise:
	None
	'''
	data = np.array(data).reshape((len(data), 1))

	mad = np.median(np.abs(data - np.median(data)))

	if mad == 0:
		return data

	mZScore = 0.6745 * (data - np.median(data)) / mad

	# remove threshold
	threshold = 3.5

	result = data[np.abs(mZScore) <= threshold].tolist()

	return result


def getPath():
	'''
	return current path, data input path, and data output path

	Return:
	curPath (str): current path of this script
	dataInputPath (str): input data path
	dataOutputPath (str): output data path

	Raise:
	url does not exist
	'''
	curPath = os.getcwd()
	upPath = os.path.dirname(curPath)

	## need to have url data//input and data//output

	try:
		dataInputPath = os.path.join(upPath, 'data', 'input')
	except:
		raise Exception('No url data/input!')
	try:
		dataOutputPath = os.path.join(upPath, 'data', 'output')
		isExists = os.path.exists(dataOutputPath)

		if not isExists:
			os.mkdir(dataOutputPath)
	except:
		raise Exception('No url data/output')
	return curPath, dataInputPath, dataOutputPath, upPath


def isContainChinese(x):
	'''
	check a string if it has Chinese characters

	Args:
	x (str or unicode or float or integer format)

	Return:
	boolean

	Raise:
	None
	'''

	if not isinstance(x, str) and not isinstance(x, unicode):
		x = str(x)
	matcher = re.findall(r"[\u4e00-\u9fff]+", x)
	if len(matcher) == 0:
		return False
	else:
		return True


def str2Datetime(x):
	'''
	string format to datetime

	Args:
	x (str): e.g, '2017-12-01 08:00:00'

	Return:
	x (datetime): e.g, datetime.datetime(2017, 12, 1, 8, 0, 0)

	Raise:
	type error
	or format error
	'''

	if isinstance(x, datetime):
		return x

	if not isinstance(x, str):
		raise Exception('Please check type of x {} is string'.format(x))

	try:
		return datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
	except:
		raise Exception('''Please check format of x {} is
		 like '2017-10-01 08:00:00' '''.format(x))


def str2Date(x):
	'''
	string format to datetime date

	Args:
	x (str or datetime)

	Return:
	x (datetime)

	Raise:
	Type or Format error
	'''
	if isinstance(x, datetime):
		return x

	if not isinstance(x, str):
		raise Exception('Please check type of x {} is string'.format(x))

	try:
		return datetime.strptime(x, "%Y-%m-%d")
	except:
		raise Exception('''Please check format of x {} is
		 like '2017-10-01' '''.format(x))


def datetime2Str(x):
	'''
	datetime format to string

	Args:
	x (datetime)

	Return:
	string

	Raise:
	format error
	'''
	if not isinstance(x, datetime):
		raise Exception('''Please check type of x {} 
			is datetime or pandas.datetime'''.format(x))
	else:
		try:
			## if x is pandas datetime format using the following line
			x = x.to_pydatetime()
		except:
			x = x
	try:
		return datetime.strftime(x, "%Y-%m-%d %H:%M:%S")
	except:
		raise Exception('''Please check {} contain year, month, 
			day, hour, minute and second'''.format(x))


def date2Str(x):
	'''
	date to string

	Args:
	x (datetime)

	Return:
	string

	Raise:
	format error
	'''
	if not isinstance(x, datetime):
		raise Exception('''Please check type of x {} 
			is datetime or pandas.datetime'''.format(x))
	else:
		try:
			## if x is pandas datetime format using the following line
			x = x.to_pydatetime()
		except:
			x = x
	try:
		return datetime.strftime(x, "%Y-%m-%d")
	except:
		raise Exception('''Please check {} contain year, month, 
			day'''.format(x))


def isWeekDay(x):
	'''
	check if x is weekday or weekend

	Args:
	x (str): e.g. '2017-10-29'

	Return:
	boolean: True for weekday, False for weekend

	Raise:
	Type Error
	'''

	try:
		x = str2Date(x)
	except:
		raise TypeError

	weekno = x.weekday()
	if weekno < 5:
		return True
	else:
		return False


def add_days_to_date(date, days):
	"""

	:param date:
	:param days:
	:return: add days to date
	"""
	if isinstance(date, str):
		date = str2Date(date)
	added_date = date + timedelta(days=days)
	return date2Str(added_date)


def percent_format(x):
	"""

	:param x: float format number
	:return: percent format number
	"""
	return '{}%'.format(np.round(x * 100, 2))


def length_of_list(nums):
	"""

	:param nums: a list of num
	:return: length of max successive sub-list which are all less than 30
	"""
	len_nums = len(nums)
	if len_nums == 0:
		return 0

	dp = [0 for i in range(len_nums)]
	for i in range(len_nums):
		if nums[i] <= 30:
			dp[i] = 1
			for num in nums[i + 1:]:
				if num <= 30:
					dp[i] = dp[i] + 1
				else:
					break
	return max(dp)


def mostCommon(x):
	'''
	return most occurrence of elements in x

	Args:
	x (array like)

	Return:
	(most_common_element, occurrence)

	Raise:
	empty check
	'''

	# check empty
	if len(x) == 0:
		raise Exception('Empty Arguments!')
	return collections.Counter(x).most_common(1)[0]


def getTotalDaysOfMonth(year, month):
	'''
	get total days of a specific month

	Args:
	year (int): e.g 2017
	month (int): e.g 1

	Return:
	totDays (int)

	Raise:
	None
	'''

	dayOfWeek, totDays = calendar.monthrange(year, month)
	return totDays


def validateEmpid(emp):
	'''
	validate employee id
	if the length of employee id does not have 8 digits,
	fill it to 8

	Args:
	emp (int or float or str): employee id

	Return:
	result (str): valid employee id
	'''
	emp = str(emp)
	if len(emp) == 0 or emp == 'nan':
		return ''
	emp = str(int(float(emp)))
	result = emp
	if len(emp) < 8:
		diff_0 = 8 - len(emp)
		result = str(0) * diff_0 + emp
	return result


def checkColumns(df, cols):
	'''
	check if df contains all required columns data

	Args:
	df (pd.DataFrame): data frame
	cols (list): required columns

	Raise:
	Column does not exist
	'''
	for c in cols:
		if c not in df.columns.tolist():
			raise Exception('No column named {}'.format(c))


def week_NO(date):
	'''
	Args: string format of date: 2018-04-01

	output: this date belongs to which week of the month
	'''

	year = int(str(date).split('-')[0])
	month = int(str(date).split('-')[1])
	date = datetime.strptime(date, '%Y-%m-%d')

	if month != 1:
		last_month = month - 1
		totDays = calendar.monthrange(year, last_month)[1]

		last_day = str(year) + '-' + str(last_month) + '-' + str(totDays)
		last_day = datetime.strptime(last_day, '%Y-%m-%d')

		# information about last day of the former month
		L_weekday_no = last_day.weekday() + 1
		L_week_no = int(last_day.strftime('%W'))

		if L_weekday_no != 7:
			week_no = int(date.strftime('%W')) - L_week_no + 1
		else:
			week_no = int(date.strftime('%W')) - L_week_no

	else:
		week_no = time(str(date), '%W')

	return week_no


def week_day(date):
	'''
	Args: string format of date: 2018-04-01

	output: the week day number of this date
	'''

	date = datetime.strptime(date, '%Y-%m-%d')
	return date.weekday() + 1


def date_formation(Year, Month, week, day):
	'''
	Args:
	Year, Month: in which year and month
	week: no. of week in the whole month
	day: no. of weekday in that week

	output: string format date
	'''

	first_day = str(Year) + '-' + str(Month) + '-' + '01'
	F_week_no = week_NO(first_day)

	first_day = datetime.strptime(first_day, '%Y-%m-%d')
	F_weekday = first_day.weekday() + 1

	day_interval = (week - F_week_no) * 7 + (day - F_weekday) + 1

	date = str(Year) + '-' + date_normalization(Month) + '-' + date_normalization(day_interval)
	return date


def all_index(list, element):
	'''
	Args: a list, an element contains in this list

	output: all indice of the element in list
	'''
	return [i for (i, j) in enumerate(list) if j == element]


def get_dates(Year, Month):
	'''
	Args: Year and Month of target month

	Return:
	dates (list)
	'''
	_, total_days = calendar.monthrange(Year, Month)
	dates = []
	for i in range(1, total_days + 1):
		m = date_normalization(Month)
		d = date_normalization(i)
		dt = str(Year) + '-' + m + '-' + d
		dates.append(dt)
	return dates


def date_normalization(d):
	'''
	normalize date format

	Args:
	d (int): month or day

	Return:
	res (str): with two chars
	'''
	if d < 10:
		res = str(0) + str(d)
	else:
		res = str(d)
	return res


def shift_parse(classname):
	'''
	parse shifts based on classname

	Args:
	classname (str)

	Return:
	res (list): [department code, day type, shift name, start time, end time]
	'''

	m = re.match(r"(^\d{3,4}[A-Z]+)(\d+)(\d{2}[DP])(\d{4})(\d{4})", classname)
	dept_code = m.group(1)
	day_type = m.group(2)
	shift_name = m.group(3)
	start = m.group(4)
	start = start[:2] + ':' + start[2:]
	end = m.group(5)
	end = end[:2] + ':' + end[2:]

	return [dept_code, day_type, shift_name, start, end]


def FromDateList(beginDate, endDate):
	'''
	Args: string format date like '2018-05-01'

	output: date_list between beginDate and endDate
	'''

	date_list = [datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
	return date_list


def time_slot(StartTime, EndTime, TimePeriod):
	'''
	Args:
	StartTime, EndTime: string format time like '08:00:00'
	TimePerios: int format of minute between two elements of output list

	output: list format of time(elements are of string format)
	'''

	ST = datetime.strptime(StartTime, '%H:%M:%S')
	ET = datetime.strptime(EndTime, '%H:%M:%S')

	time_list = [ST]

	while time_list[-1] - ET != timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0,
										  weeks=0):
		temp_time = time_list[-1] + timedelta(minutes=TimePeriod)
		time_list.append(temp_time)

	time_list = map(lambda x: str(x).split(' ')[1], time_list)
	return time_list


def get_month_start_date(schedule_start_date, number):
	"""

	:param schedule_start_date: string format date
	:param number: number of months put forwards to
	:return: string format date of month's first date
	"""
	year = int(schedule_start_date.split('-')[0])
	month = int(schedule_start_date.split('-')[1])
	new_month = month - number
	if new_month == 0:
		new_month = 12
		new_year = year - 1
	else:
		new_year = year if new_month > 0 else year - int(np.ceil(np.abs(new_month) / 12))
		new_month = new_month if new_month > 0 else new_month + int(np.ceil(np.abs(new_month) / 12) * 12)
	new_month = '%02d' % new_month
	return str(new_year) + '-' + new_month + '-01'
