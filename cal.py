from receive import data

flag=[]      #标记墩等级
for i in range(8):
    flag.append(0)

"""比较单牌大小
    return 1: a>b
    return 0:a==b
    return -1:a<b
"""
def singleCardCompare(a,b):
    if a!=b and (a!=1 and b!=1):
        if a>b:
            return 1
        else:
            return -1
    elif a!=b and (a==1 or b==1):
        if a==1:
            return 1
        else:
            return -1
    elif a==b:
        return 0


    
def isshunzi(bucket):   #顺子
    cnt=0
    for j,i in bucket.items():
        if i!=0:
            cnt = cnt + 1
            if cnt>=5 :
                return True
    if cnt==4:
        if bucket[0]!=0:
            return True
    return False

def isduizi(bucket): #对子
    for i in bucket.values():
        if i==2:
            return True
    return False

def isthua(huabucket):  #同花
    cnt=0
    for i in huabucket.values():
        if i>=5:
            return True
        cnt= cnt+1
    cnt=-1
    return False

def isbomb(bucket):     #炸弹
    for i in bucket.values():
        if i==4:
            return True
    return False

def ishulu(bucket):   #葫芦
    flag=0
    for i in bucket.values():
        if i == 2:
            flag=1
            break
    for i in bucket.values():
        if i == 3 and flag ==1:
            return True
    return False
            

#对牌进行加工处理
def sortCard(card,num):
    val = [0,'A','2','3','4','5','6','7','8','9','10','J','Q','K']
    order=[]
    for j in range(num,1,-1):
        smallest = card[0]
        for i in range(1,j):
            if val.index(smallest[1:])<=val.index(card[i][1:]):
                pass
            else:
                smallest=card[i]
        card.remove(smallest)
        order.append(smallest)
    order.append(card[0])    #排序后的扑克牌
    return order

def main():
    newdata=data
    newdata=str(data,encoding="utf-8")
    newdata=newdata.split(":")
    #分割用户名
    userid=newdata[3].split(",")[0]
    #分割扑克牌，保存为大小为13的卡牌列表
    card=newdata[4].split("\"")[1].split()

    bucket={'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0}    #牌桶记录点数一致牌有多少张
    val = [0,'A','2','3','4','5','6','7','8','9','10','J','Q','K']
    huabucket={'$':[],'&':[],'*':[],'#':[]}    #花色桶记录花色一致的有多少张牌
    hua=['$','&','*','#']
    newcard=[]
    newindex=13
    order=sortCard(card,newindex)
    fbucket = bucket
    for x in order:
        fbucket[x[1:]] = fbucket[x[1:]] + 1
        huabucket[x[0]].append(x[1:])
    
    for i in huabucket.keys():
        if len(huabucket[i])>=5 and isshunzi(huabucket[i])==True:    #同花顺
            flag[0]=1
            thua=list(set(huabucket[i]))
            arr=[]
            for j in thua:
                arr.append(val.index(j))
            for j in len(arr):
                if arr[j]==1:
                    newcard.append(i+'10')
                    order.remove(i+'10')
                    newcard.append(i+'J')
                    order.remove(i+'J')
                    newcard.append(i+'Q')
                    order.remove(i+'Q')
                    newcard.append(i+'K')
                    order.remove(i+'K')
                    newcard.append(i+'A')
                    order.remove(i+'A')
                    newindex = newindex-5
                    break
            if j==len(arr)-1:
                a = max(arr)
                for k in range(a,a-5,-1):
                    newcard.append(i+val[arr[k]])
                    order.remove(i+val[arr[k]])
                newindex = newindex-5

    order=sortCard(order,newindex)
    tbucket = bucket
    thuabucket = huabucket
    for x in order:
        tbucket[x[1:]] = tbucket[x[1:]] + 1
        thuabucket[x[0]].append(x[1:])
    if 1:
        if isbomb(tbucket)==True:   #炸弹
            flag[1]=2
            arr=[]
            for i,j in tbucket.items():
                if i==4:
                    arr.append(val.index(j))
            arr.sort()
            if len(arr)!=0 and arr[0]==1:        #AAAA
                for i in range(4):
                    newcard.append('$A')
                    order.remove('$A')
                    newcard.append('*A')
                    order.remove('*A')
                    newcard.append('&A')
                    order.remove('&A')
                    newcard.append('#A')
                    order.remove('#A')
                newindex = newindex -4
            else:
                for i in range(4):
                    newcard.append('$'+val[max(arr)])
                    order.remove('$'+val[max(arr)])
                    newcard.append('*'+val[max(arr)])
                    order.remove('*'+val[max(arr)])
                    newcard.append('&'+val[max(arr)])
                    order.remove('&'+val[max(arr)])
                    newcard.append('#'+val[max(arr)])
                    order.remove('#'+val[max(arr)])
                newindex = newindex -4
            
    if flag[0]==1 and flag[1]==1:
        order = sortCard(order,4)
        thbucket = bucket
        for x in order:
            thbucket[x[1:]] = thbucket[x[1:]] + 1
        arr=[]
        for i in range(4):
            arr.append(val.index(order[1:]))
        arr.sort()
        if isduizi(thbucket) and arr[0]==arr[1] and arr[2]==arr[3]:    #同花顺炸弹对子
            if singleCardCompare(arr[0],arr[2])==1: 
                for i in order:
                    if i[1:]==val[arr[2]]:
                        newcard.append(i)
                        order.remove(i)
                        newindex = newindex +1
                        break
                for i in range(3):
                    newcard.append(order[i])
                    newindex = newindex +1
                return userid,newcard
            elif singleCardCompare(arr[0],arr[2])==-1:
                for i in order:
                    if i[1:]==val[arr[0]]:
                        newcard.append(i)
                        order.remove(i)
                        newindex = newindex +1
                        break
                for i in range(3):
                    newcard.append(order[i])
                    newindex = newindex +1
                return userid,newcard
        elif isduizi(thubuket) :
            for i,j in thubucket.items():
                if j==2:
                    num=val.index(i)
                    break
            for j in range(len(arr)):
                if arr[j]!=num:
                    for i in order:
                        if i[1:]==val[arr[j]]:
                            newcard.append(i)
                            order.remove(i)
                            newindex = newindex +1
                            break
            for i in order:
                newcard.append(order[i])
                order.remove(i)
                newindex = newindex +1
            return userid,newcard
        else:                  #同花顺炸弹乌龙
            if arr[0]==1:
                for i in range(1,4):
                    newcard.append(order[i])
                newcard,append(order[0])
            else:
                for i in range(4):
                    newcard.append(order[i])
            return userid,newcard
        
    order=sortCard(order,newindex)
    fibucket = bucket
    for x in order:
        fibucket[x[1:]] = fibucket[x[1:]] + 1
    if ishulu(thbucket)==True and flag[0]==1:
        flag[2]=1
        arr=[]
        for i,j in fibucket.items():
            if j==3:
                hua=[]
                for k in order :
                    if j==k[1:] :
                        hua.append(k[0])
                for k in range(3):
                    newcard.append(hua[i]+i)
                    order.remove(hua[i]+i)
                    newindex = newindex +1
            if j==2 :    #aefaf
                arr.append(i)
        if flag[0]==1 :    #同花顺葫芦+对子/乌龙   |炸弹葫芦+对子/乌龙
            if len(arr)==1 :  #同花顺葫芦乌龙
                for i in order:
                    if i[1:]==arr[0]:
                        for k in range(2):
                            newcard.append(i)
                            order.append(i)
                            newindex = newindex +1
                for i in range(3):
                    newcard.append(order[i])
                    newindex = newindex +1
                return userid,newcard
            elif  len(arr)>=2: #同花顺葫芦对子
                if singleCardCompare(val.index(arr[0]),val.index(arr[1]))==1:
                    for i in order:
                        if i[1:]==arr[1]:
                            newcard.append(i)
                            order.remove(i)
                            newindex = newindex+1
                    for i in range(3):
                        newcard.append(order[i])
                        newindex = newindex +1
                    return userid, newcard
                elif singleCardCompare(val.index(arr[0]),val.index(arr[1]))==-1:
                    for i in order:
                        if i[1:]==arr[0]:
                            newcard.append(i)
                            order.remove(i)
                            newindex = newindex+1
                    for i in range(3):
                        newcard.append(order[i])
                        newindex = newindex +1
                    return userid, newcard
    elif ishulu(thbucket)==True and flag[1]==1:     #炸弹葫芦+对子/乌龙
        flag[2]=1
        arr=[]
        for i,j in fibucket.items():
             if j==2:
                arr.append(i)
        order=sortCard(order,newindex)
        sbucket = bucket
        for x in order:
            sbucket[x[1:]] = sbucket[x[1:]] + 1
        if len(arr)==3:                             #炸弹葫芦对子
            if singleCardCompare(val.index(arr[0]),val.index(arr[1]))==1:
                for i in order:
                    if i[1:]==arr[1]:
                        newcard.append(i)
                        order.remove(i)
                        newindex = newindex+1
                hua=[]
                for i,j in sbucket.items():
                    if j==3:
                        hua.append(i)
                for k in order :
                    if j==k[1:] :
                        hua.append(k[0])
                for k in range(3):
                    newcard.append(hua[i]+i)
                    order.remove(hua[i]+i)
                    newindex = newindex +1
                if singleCardCompare(val.index(arr[0]),val.index(arr[2]))==1:
                    for i in order:
                        if i[1:]==arr[2]:
                            newcard.append(i)
                            order.remove(i)
                            newindex = newindex +1
                    for i in order:
                        newcard.append(i)
                        order.remove(i)
                    return userid,newcard
                else :
                    for i in order:
                        if i[1:]==arr[0]:
                            newcard.append(i)
                            order.remove(i)
                            newindex = newindex +1
                    for i in order:
                        newcard.append(i)
                        order.remove(i)
                    return userid,newcard
            elif singleCardCompare(val.index(arr[0]),val.index(arr[1]))==-1:
                for i in order:
                    if i[1:]==arr[0]:
                        newcard.append(i)
                        order.remove(i)
                        newindex = newindex+1
                hua=[]
                for i,j in sbucket.items():
                    if j==3:
                        hua.append(i)
                for k in order :
                    if j==k[1:] :
                        hua.append(k[0])
                for k in range(3):
                    newcard.append(hua[i]+i)
                    order.remove(hua[i]+i)
                    newindex = newindex +1
                if singleCardCompare(val.index(arr[1]),val.index(arr[2]))==1:
                    for i in order:
                        if i[1:]==arr[2]:
                            newcard.append(i)
                            order.remove(i)
                            newindex = newindex +1
                    for i in order:
                        newcard.append(i)
                        order.remove(i)
                    return userid,newcard
                else :
                    for i in order:
                        if i[1:]==arr[1]:
                            newcard.append(i)
                            order.remove(i)
                            newindex = newindex +1
                    for i in order:
                        newcard.append(i)
                        order.remove(i)
                    return userid,newcard
        elif len(arr)==2:
            for i,j in sbucket.items():
                if j!=2:
                    for i in order:
                        if i[1:]==i:
                            newcard.append(i)
                            order.remove(i)
                            newindex = newindex+1
                            break
            hua=[]
            for i,j in sbucket.items():
                if j==3:
                    hua.append(i)
            for k in order :
                if j==k[1:] :
                    hua.append(k[0])
            for k in range(3):
                newcard.append(hua[i]+i)
                order.remove(hua[i]+i)
                newindex = newindex +1
            if singleCardCompare(val.index(arr[0]),val.index(arr[1]))==1:
                for i in order:
                    if i[1:]==arr[1]:
                        newcard.append(i)
                        order.remove(i)
                        newindex = newindex +1
                for i in order:
                    newcard.append(i)
                    order.remove(i)
                return userid,newcard
            else:
                for i in order:
                    if i[1:]==arr[0]:
                        newcard.append(i)
                        order.remove(i)
                        newindex = newindex +1
                for i in order:
                    newcard.append(i)
                    order.remove(i)
                return userid,newcard
        elif len(arr)==1:
            for i in order :
                if i[1:]==arr[0]:
                    dui=i
                    order.remove(i)
                    newindex = newindex +2
                    break
            order=sortCard(order,4)
            if order[0][1:]!='A':
                newcard.append(order[0])
                order.remove(order[0])
            else :
                newcard.append(order[1])
                order.remove(order[1])
            hua=[]
            for i,j in sbucket.items():
                if j==3:
                    hua.append(i)
            for k in order :
                if j==k[1:] :
                    hua.append(k[0])
            for k in range(3):
                newcard.append(hua[i]+i)
                order.remove(hua[i]+i)
                newindex = newindex +1
            newcard.append(dui)
            for i in order:
                newcard.append(i)
                newindex = newindex +1
            return userid,newcard


    order=sortCard(order,newindex)
    ubucket = bucket
    uhuabucket = huabucket
    for x in order:
        ubucket[x[1:]] = ubucket[x[1:]] + 1
        uhuabucket[x[0]].append(x[1:])

            
            
        
                    
"""        elif len(huabucket[i])>=5:    #同花
                order=sortCard(order,newindex)     #重新对剩下的牌进行排序
                tbucket = bucket                       #重新建立点数桶
                for x in order:
                    tbucket[x[1:]] = tbucket[x[1:]] + 1
                if isbomb(tbucket)==True:
                    flag[1]=2
                    break
                elif ishulu(tbucket)==True:
                    flag[2]=2
                    break
                else:
                    flag[3]=1
                    arr=[]
                    for k in range(len(huabucket[i])):
                        arr.append(val.index(k))
                    arr.sort()
                    if(arr[0]==1):
                        newcard.append(i+"A")
                        order.remove(i+"A")
                    else:
                        newcard.append(i+val[max(arr)])
                        order.remove(i+val[max(arr)])
                    for k in range(1,5):
                        newcard.append(i+val[arr[k]])
                        order.remove(i+val[arr[k]])
                    newindex = newindex-5 """
        


main()


