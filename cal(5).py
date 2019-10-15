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


    
def isshunzi(**bucket):   #顺子
    cnt=0
    for j,i in bucket.items():
        if j=='A':
            continue
        if i!=0:
            cnt = cnt + 1
            if cnt>=5 :
                return True,j
        else :
            cnt=0
    if cnt==4:
        if bucket['A']!=0:
            return True,'A'
    return False,'N'

def isduizi(**bucket): #对子
    for i in bucket.values():
        if i==2:
            return True
    return False

def isthua(**huabucket):  #同花

    for i,j in huabucket.items():
        if len(j)>=5:
            return True

    return False

def isbomb(**bucket):     #炸弹
    for i in bucket.values():
        if i==4:
            return True
    return False

def ishulu(**bucket):   #葫芦
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
        smallbucket = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0}
        for k in huabucket[i]:
            smallbucket[k] = smallbucket[k] + 1
        f1,f2=isshunzi(**smallbucket)
        if len(huabucket[i])>=5 and f1==True:    #同花顺
            flag[0]=1
            thua=list(set(huabucket[i]))
            thua.sort()
            arr=[]
            for j in thua:
                arr.append(val.index(j))
            if f2=='A':
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
            else :
                j = val.index(f2)
                for k in range(j-4,j+1,1):
                    newcard.append(i+val[k])
                for k in range(5):
                    order.remove(newcard[len(newcard)-1-k])
                newindex = newindex-5

    order=sortCard(order,newindex)
    tbucket = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0}
    thuabucket = {'$':[],'&':[],'*':[],'#':[]}
    for x in order:
        tbucket[x[1:]] = tbucket[x[1:]] + 1
        thuabucket[x[0]].append(x[1:])
    if 1:
        if isbomb(**tbucket)==True:   #炸弹
            flag[1]=1
            arr=[]
            for i,j in tbucket.items():
                if j==4:
                    arr.append(val.index(i))
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
        thbucket = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0}
        for x in order:
            thbucket[x[1:]] = thbucket[x[1:]] + 1
        arr=[]
        for i in range(4):
            arr.append(val.index(order[i][1:]))
        arr.sort()
        if isduizi(**thbucket) and arr[0]==arr[1] and arr[2]==arr[3]:    #同花顺炸弹对子
            if singleCardCompare(arr[0],arr[2])==1: 
                for i in order:
                    if i[1:]==val[arr[2]]:
                        newcard.append(i)
                        order.remove(i)
                        newindex = newindex -1
                        break
                for i in range(3):
                    newcard.append(order[i])
                    newindex = newindex -1
                return userid,newcard
            elif singleCardCompare(arr[0],arr[2])==-1:
                for i in order:
                    if i[1:]==val[arr[0]]:
                        newcard.append(i)
                        order.remove(i)
                        newindex = newindex -1
                        break
                for i in range(3):
                    newcard.append(order[i])
                    newindex = newindex -1
                return userid,newcard
        elif isduizi(**thbucket) :
            for i,j in thbucket.items():
                if j==2:
                    num=val.index(i)
                    break
            for j in range(len(arr)):
                if arr[j]!=num:
                    for i in order:
                        if i[1:]==val[arr[j]]:
                            newcard.append(i)
                            order.remove(i)
                            newindex = newindex -1
                            break
            for i in range(2):
                newcard.append(order[0])
                order.remove(order[0])
                newindex = newindex -1
            return userid,newcard
        else:                  #同花顺炸弹乌龙
            if arr[0]==1:
                for i in range(1,4):
                    newcard.append(order[i])
                newcard.append(order[0])
            else:
                for i in range(4):
                    newcard.append(order[i])
            return userid,newcard
        

    order=sortCard(order,newindex)
    fibucket = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0}
    for x in order:
        fibucket[x[1:]] = fibucket[x[1:]] + 1
    if ishulu(**fibucket)==True and flag[0]==1:   #葫芦
        flag[2]=1
        arr=[]
        for i,j in fibucket.items():
            if j==3:
                for k in order:
                    if k[1:]==i:
                        newcard.append(k)
                        newindex = newindex -1
                for k in range(3):
                    order.remove(newcard[len(newcard)-k-1])
            if j==2:
                arr.append(i)

        if flag[0]==1 :    #同花顺葫芦+对子/乌龙   |炸弹葫芦+对子/乌龙
            if len(arr)==1 :  #同花顺葫芦乌龙
                for i in order:
                    if i[1:]==arr[0]:
                        for k in range(2):
                            newcard.append(i)
                            order.remove(i)
                            newindex = newindex -1
                for i in range(3):
                    newcard.append(order[i])
                    newindex = newindex -1
                print('1',newcard)
                return userid,newcard
            elif  len(arr)>=2: #同花顺葫芦对子
                if singleCardCompare(val.index(arr[0]),val.index(arr[1]))==1:
                    for i in order:
                        if i[1:]==arr[1]:
                            newcard.append(i)
                            newindex = newindex - 1
                    for k in range(2):
                        order.remove(newcard[len(newcard)-1-k])
                    for i in range(3):
                        newcard.append(order[i])
                        newindex = newindex -1
                    return userid, newcard
                elif singleCardCompare(val.index(arr[0]),val.index(arr[1]))==-1:
                    for i in order:
                        if i[1:]==arr[0]:
                            newcard.append(i)
                            newindex = newindex - 1
                    for k in range(2):
                        order.remove(newcard[len(newcard)-1-k])
                    for i in range(3):
                        newcard.append(order[i])
                        newindex = newindex -1
                    return userid, newcard
    elif ishulu(**fibucket)==True and flag[1]==1:     #炸弹葫芦+对子/乌龙
        flag[2]=1
        arr=[]
        for i,j in fibucket.items():
             if j==2:
                arr.append(i)
        order=sortCard(order,newindex)
        sbucket = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0}
        for x in order:
            sbucket[x[1:]] = sbucket[x[1:]] + 1
        if len(arr)==3:                             #炸弹葫芦对子
            if singleCardCompare(val.index(arr[0]),val.index(arr[1]))==1:
                for i in order:
                    if i[1:]==arr[1]:
                        newcard.append(i)
                        order.remove(i)
                        newindex = newindex-1
                for i,j in sbucket.items():
                    if j==3:
                        for k in order:
                            if k[1:]==i:
                                newcard.append(k)
                for i in range(3):
                    order.remove(newcard[len(newcard)-1-i])
                    newindex = newindex -1
                if singleCardCompare(val.index(arr[0]),val.index(arr[2]))==1:
                    for i in order:
                        if i[1:]==arr[2]:
                            newcard.append(i)
                            newindex = newindex -1
                    for i in range(2):
                        order.remove(newcard[len(newcard)-1-i])
                    for i in range(3):
                        newcard.append(order[i])
                        newindex = newindex -1
                    return userid,newcard
                else :
                    for i in order:
                        if i[1:]==arr[0]:
                            newcard.append(i)
                            newindex = newindex -1
                    for i in range(2):
                        order.remove(newcard[len(newcard)-1-i])
                    for i in range(3):
                        newcard.append(order[i])
                        newindex = newindex -1
                    return userid,newcard
            elif singleCardCompare(val.index(arr[0]),val.index(arr[1]))==-1:
                for i in order:
                    if i[1:]==arr[0]:
                        newcard.append(i)
                        order.remove(i)
                        newindex = newindex-1
                for i,j in sbucket.items():
                    if j==3:
                        for k in order:
                            if k[1:]==i:
                                newcard.append(k)
                for i in range(3):
                    order.remove(newcard[len(newcard)-1-i])
                    newindex = newindex -1
                if singleCardCompare(val.index(arr[1]),val.index(arr[2]))==1:
                    for i in order:
                        if i[1:]==arr[2]:
                            newcard.append(i)
                            newindex = newindex -1
                    for i in range(2):
                        order.remove(newcard[len(newcard)-1-i])
                    for i in range(3):
                        newcard.append(order[i])
                        newindex = newindex -1
                    return userid,newcard
                else :
                    for i in order:
                        if i[1:]==arr[1]:
                            newcard.append(i)
                            newindex = newindex -1
                    for i in range(2):
                        order.remove(newcard[len(newcard)-1-i])
                    for i in range(3):
                        newcard.append(order[i])
                        newindex = newindex -1
                    return userid,newcard
        elif len(arr)==2:     #炸弹葫芦对子
            for i,j in sbucket.items():    #推入一个和炸弹匹配的单牌
                if j==1:
                    for k in order:
                        if k[1:]==i:
                            newcard.append(k)
                            order.remove(k)
                            newindex = newindex-1
                            break
                    if (len(order)==8):
                        break
            for i,j in sbucket.items():  #推入葫芦
                if j==3:
                    for k in order:
                        if k[1:]==i:
                            newcard.append(k)
            for i in range(3):
                order.remove(newcard[len(newcard)-1-i])
                newindex = newindex -1
            if singleCardCompare(val.index(arr[0]),val.index(arr[1]))==1:
                for i in order:
                    if i[1:]==arr[1]:    #推入和葫芦匹配的对子
                        newcard.append(i)
                        newindex = newindex -1
                for i in range(2):
                    order.remove(newcard[len(newcard)-1-i])
                for i in range(3):
                    newcard.append(order[i])
                    newindex = newindex -1
                return userid,newcard
            else:
                for i in order:
                    if i[1:]==arr[0]:   #推入和葫芦匹配的对子
                        newcard.append(i)
                        newindex = newindex -1
                for i in range(2):
                    order.remove(newcard[len(newcard)-1-i])
                print(order)
                print(newcard)
                for i in range(3):
                    newcard.append(order[i])
                    newindex = newindex -1
                return userid,newcard
            
        elif len(arr)==1:     #炸弹葫芦乌龙
            duizi=[]
            for i in order :
                if i[1:]==arr[0]:
                    duizi.append(i)
            for i in range(2):
                order.remove(duizi[i])
            hulu=[]
            for i,j in sbucket.items():
                if j==3:
                    for k in order:
                        if k[1:]==i:
                            hulu.append(k)
            for i in range(3):
                order.remove(hulu[i])
            order=sortCard(order,4)
            if order[0][1:]!='A':
                newcard.append(order[0])
                order.remove(order[0])
            else :
                newcard.append(order[1])
                order.remove(order[1])
            for i in range(3):   #推入葫芦
                newcard.append(hulu[i])
            for i in range(2):   #推入对子
                newcard.append(duizi[i])
            for i in range(3):
                newcard.append(order[i])
            return userid,newcard
    elif ishulu(**fibucket)==True:  #最高级为葫芦
        for i,j in fibucket.items():
            if j==3:
                for k in order:
                    if k[1:]==i:
                        newcard.append(k)
                break
        for i in range(3):
            order.remove(newcard[len(newcard)-1-i])
            newindex = newindex -1


    order=sortCard(order,newindex)
    bucket = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0}
    huabucket = {'$':[],'&':[],'*':[],'#':[]}
    for x in order:
        bucket[x[1:]] = bucket[x[1:]] + 1
        huabucket[x[0]].append(x[1:])
    if isthua(**huabucket)==True :   
        flag[3]=1
        if flag[0]==1:    #同花顺同花乌龙
            for i,j in huabucket.items():
                if len(j)>=5:
                    for k in range(5):
                        newcard.append(i+j[k])
                    break
            for i in range(5):
                order.remove(newcard[len(newcard)-1-i])
            for i in range(3):
                newcard.append(order[i])
            return userid,newcard
        elif flag[1]==1:      #炸弹同花+对子/乌龙
            tonghua=[]
            for i,j in huabucket.items():
                if len(j)>=5:
                    for k in range(5):
                        tonghua.append(i+j[k])
                    break
            for i in range(5):
                order.remove(tonghua[i])
            bucket = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0}
            for x in order:
                bucket[x[1:]] = bucket[x[1:]] + 1
            arr=[]
            for i,j in bucket.items():
                if j>=2:
                    arr.append(i)
            if isduizi(**bucket)==True:       #炸弹同花对子
                if len(arr)==2:
                    if singleCardCompare(arr[0],arr[1])==1:
                        for i in order:
                            if i[1:]==arr[1]:
                                newcard.append(i)
                                order.remove(i)
                                break;
                        for i in range(5):
                            newcard.append(tonghua[i])
                        for i in range(3):
                            newcard.append(order[i])
                        return userid,newcard
                    if singleCardCompare(arr[0],arr[1])==-1:
                        for i in order:
                            if i[1:]==arr[0]:
                                newcard.append(i)
                                order.remove(i)
                                break;
                        for i in range(5):
                            newcard.append(tonghua[i])
                        for i in range(3):
                            newcard.append(order[i])
                        return userid,newcard
                elif len(arr)==1:  
                    duizi=[]
                    for i in order :
                        if i[1:]==arr[0]:
                            duizi.append(i)
                    for i in range(2):
                        order.remove(duizi[i])
                    newcard.append(order[0])
                    order.append(order[0])
                    for i in range(5):
                        newcard.append(tonghua[i])
                    newcard.append(order[0])
                    for i in range(2):
                        newcard.append(duizi[i])
                    return userid,newcard
            else:     #炸弹同花乌龙
                if order[0][1:]=='A':
                    newcard.append(order[1])
                    order.remove(order[1])
                else :
                    newcard.append(order[0])
                    order.remove(order[0])
                for i in range(5):
                    newcard.append(tonghua[i])
                for i in range(3):
                    newcard.append(order[i])
                return userid,newcard
        elif ishulu(**bucket)==True:   #葫芦同花+对子/乌龙
            bucket = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0}
            for x in order:
                bucket[x[1:]] = bucket[x[1:]] + 1
            arr=[]
            for i,j in bucket.items():
                if j==2:
                    arr.append(i)
            if len(arr)>=1:      #葫芦同花乌龙
                for i in order:
                    if i[1:]==arr[0]:
                        newcard.append(i)
                for i in range(2):
                    order.remove(newcard[len(newcard)-1-i])
                bucket = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0}
                for x in order:
                    bucket[x[1:]] = bucket[x[1:]] + 1
                if isthua(bucket)==True:  #可以构成同花
                    tonghua=[]
                    for i,j in huabucket.items():
                        if len(j)>=5:
                            for k in range(5):
                                newcard.append(i+j[k])
                        break
                    for i in range(5):
                        order.remove(newcard[len(newcard)-1-i])
                    for i in range(3):
                        newcard.append(order[i])
                    print(newcard)
                    return userid,newcard
                else :    #构不成同花
                    for i in range(8):
                        newcard.append(order[i])
                    return uesrid,newcard
        else:                     #最高级为同花
            tonghua=[]
            for i,j in huabucket.items():
                if len(j)>=5:
                    for k in range(5):
                        newcard.append(i+j[k])
                    break
            for i in range(5):
                order.remove(newcard[len(newcard)-1-i])
            bucket = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0}
            for x in order:
                bucket[x[1:]] = bucket[x[1:]] + 1
            f1,f2=isshunzi(**bucket)
            arr=['10','J','Q','K','A']
            if f1==True:   #顺子
                if f2=='A':
                    for i in range(5):
                        for k in order:
                            if k[1:]==arr[5-i]:
                                newcard.append(k)
                                break
                    for i in range(5):
                        order.remove(newcard[len(newcard)-1-i])
                        newindex = newindex -1
                else:
                    num=val.index(f2)
                    for i in range(5):
                        for k in order:
                            if k[1:]==val[num-i]:
                                newcard.append(k)
                                break
                    for i in range(5):
                        order.remove(newcard[len(newcard)-1-i])
                        newindex = newindex -1
                for i in range(3):
                    newcard.append(order[i])
                    return userid,newcard
            else:
                duizi=[]
                brr=[]
                for i,j in bucket.items():
                    if j==2:
                        brr.append(i)
                if len(brr)==1:
                    for k in order:
                        if k[1:]==brr[0]:
                            newcard.append(k)
                    for i in range(2):
                        order.remove(newcard[len(newcard)-1-i])
                    for i in range(len(order)):
                        newcard.append(order[i])
                    return userid,newcard
                elif len(brr)==2:
                    for i in range(2):
                        for k in order:
                            if k[1:]==brr[i]:
                                newcard.append(k)
                    for i in range(4):
                        order.remove(newcard[len(newcard)-1-i])
                    for i in range(len(order)):
                        newcard.append(order[i])
                    return userid,newcard

        bucket = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,'Q':0,'K':0}
        for x in order:
            bucket[x[1:]] = bucket[x[1:]] + 1
        f1,f2=isshunzi(**bucket)
        arr=['10','J','Q','K','A']
        if f1==True:   #顺子
            if f2=='A':
                for i in range(5):
                    for k in order:
                        if k[1:]==arr[5-i]:
                            newcard.append(k)
                            break
                for i in range(5):
                    order.remove(newcard[len(newcard)-1-i])
                    newindex = newindex -1
            else:
                num=val.index(f2)
                for i in range(5):
                    for k in order:
                        if k[1:]==val[num-i]:
                            newcard.append(k)
                            break
                for i in range(5):
                    order.remove(newcard[len(newcard)-1-i])
                    newindex = newindex -1
            for i in range(len(order)):
                newcard.append(order[i])
                return userid,newcard
        else:
            duizi=[]
            brr=[]
            for i,j in bucket.items():
                if j==2:
                    brr.append(i)
            if len(brr)==1:
                for k in order:
                    if k[1:]==brr[0]:
                        newcard.append(k)
                for i in range(2):
                    order.remove(newcard[len(newcard)-1-i])
                for i in range(len(order)):
                    newcard.append(order[i])
                return userid,newcard
            elif len(brr)==2:
                for i in range(2):
                    for k in order:
                        if k[1:]==brr[i]:
                            newcard.append(k)
                for i in range(4):
                    order.remove(newcard[len(newcard)-1-i])
                for i in range(len(order)):
                    newcard.append(order[i])
                return userid,newcard


    order=sortCard(card,newindex)
    return userid,order
                    
                
        

main()

