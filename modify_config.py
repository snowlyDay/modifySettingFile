import sys
import json
import re 


propertiesFilePath = sys.argv[1]
JSONFilePath = sys.argv[2]

with open(propertiesFilePath,'r') as f:
	line =  f.readlines()
f.close


def parseJSONFile(filepath): 
    with open(filepath,'r') as load_f:
        json_data= json.load(load_f)
    for key in json_data:
        val = json_data[key]
        pattern = re.compile(r'_')
        c = pattern.split(key)
        # channel = 360 ..
        channel = c[1]
        # val = {'app_id': 'a','app_key': 'c', 'app_secret': 'e', 'callback_value': 'g', 'test_callback_value': 'kjajshdflaks'}
        # for key in val:
        # 	print(val[key])
        find_PropertiesFile(channel, val)

def processe_special_channel(channel):
	if channel == "xiaomi":
		channel ="mi"
	if channel == "4399":
		channel ="sisan"
	if channel == "360":
		channel ="qihoo"
	return channel


def find_PropertiesFile(channel,val_online):
	channel = processe_special_channel(channel)
	line_No = 0
	for lineData in line:
		line_No=line_No+1
		pattern = re.compile(r'\.')
		strProperties= pattern.split(lineData)
		# print(strProperties)
		# ['baidu', 'app_id=8281280\n']
		# ['baidu', 'app_key=BEAxPoGyMwM77A
		# ['baidu', 'appname=UniBaidu\n']
		# 对比JSON数据和配置文件信息是否是同一个渠道lineData
		if strProperties[0] == channel :
			value_properties = re.compile(r'=').split(strProperties[1])
			for key_online in val_online:
				if key_online == value_properties[0]:
					# print(channel)
					# print("online key")
					# print(key_online)
					# print("online vale")
					# print(val_online[key_online])
					# print("properties key")
					# print(value_properties[0])
					# print("properties value")
					# print(value_properties[1])
					# if val_online[key_online] :
					# 	value_properties[1] = val_online[key_online]
					# print(value_properties[1])
					writeDataToPropertiesFiles(line_No,channel,key_online,value_properties[1], val_online[key_online])
					


# 重新组装数据然后写回到properties文件中
def writeDataToPropertiesFiles(line_No,channel,key, properties_value, online_value ):
	# print(properties_value)
	# print(online_value)
	modified_line=""
	if not online_value == '':
		if properties_value[0] =='\\':
			modified_line = channel+'.'+key+'='+'\\\\.'+online_value+'\n'
		else :
			modified_line = channel+'.'+key+'='+online_value+'\n'
	if not modified_line == "": 
		line[line_No-1] = modified_line




# modify_PropertiesFile("baidu","")
parseJSONFile(JSONFilePath)

with open(propertiesFilePath,'w') as fw:
	fw.writelines(line)
 