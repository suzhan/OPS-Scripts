import requests
import json
import csv

# 批量修改gitlab用户等级

# 10 => Guest access 
# 20 => Reporter access 
# 30 => Developer access 
# 40 => Maintainer access 
# 50 => Owner access # Only valid for groups

urlId = 'http://locahost/api/v3/groups?private_token={token}&per_page=100000'
projectId = requests.get(urlId)
idData=json.loads(projectId.text)
# print(idData)
dict={}
dict1={}

def getProjectMember(projectId):
    print(projectId)
    urlMember = 'http://locahost/api/v3/groups/'+ str(projectId) + '/members?private_token={token}&per_page=100000'
    print(urlMember)
    projectMember=requests.get(urlMember)
    membersData=json.loads(projectMember.text)
    for j in membersData:
        dict[j["name"]] = j["id"]
        dict1[j["name"]]=j["access_level"]

    #print(dict)
    #print(dict1)

def modifyUserLevel(projectId):
    getProjectMember(projectId)
    for name in dict1:
        if name != 'Administrator':
            if dict1[name] == 30:
                urlPut='http://locahost/api/v3/groups/'+ str(projectId) +'/members/'+ str(dict[name]) +'?access_level=40&private_token={token}'
                print(urlPut)
                put=requests.put(urlPut)
                writer = csv.writer(csvfile)
                data=[]
                data.append(name)
                writer.writerows(data)

csvfile = open('/tmp/git.csv','w',encoding='utf8')
for projectId in idData:
    modifyUserLevel(projectId["id"])
csvfile.close()
