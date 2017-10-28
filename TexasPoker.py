# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 12:10:12 2017

@author: gleam
"""
# 作业：
# 假设有 K 位玩家参与德州扑克游戏，现在知道每位玩家手中的底牌
# 利用MC模拟得到每位玩家获胜的概率
class TexasPoker():   
    def __init__(self,initCards):
        # example: initCards=[[(3,'H'),(8,'S')],[(12,'S'),(8,'C')],[(5,'D'),(11,'D')]]
        # H S C D 分别代表四种花色
        self.initCards=initCards
        self.k=len(initCards)
        self.existCards=set()
        self.entireCards=None
        
    # 通过五张牌得到牌型 rank 1-9分别代表 高牌、对子、...、四条、同花顺
    # 同时返回一个tuple用于牌型rank相同时牌面的比较
    # example: [(3,'H'),(8,'S'),(12,'S'),(8,'C'),(5,'D')] => [2,(8,12,5,3)] 8代表对子牌面，12，5，3代表高牌牌面
    # modified by hh 2017/10/28
    def cardType(self,cardList):
        ## example: cardList=[(3,'H'),(8,'S'),(12,'S'),(8,'C'),(5,'D')]       
        cardList=sorted(cardList,key=lambda x:x[0])  
        numList=list(map(lambda x:x[0],cardList))       
        suitList=list(map(lambda x:x[1],cardList))
        ### find pairs in cardlist
        pairCount=0        
        for i in range(len(numList)):
            for j in range(i+1,len(numList)):
                if numList[i]==numList[j]:
                    pairCount+=1
        freqDict={}
        for i in range(len(numList)):
            if numList[i] in freqDict:
                freqDict[numList[i]]+=1 
            else:
                freqDict[numList[i]]=1      
        freqDict2={1:[],2:[],3:[],4:[]}
        for i in freqDict:
            freqDict2[freqDict[i]].append(i)
        ranktuple=[]
        for i in [4,3,2,1]:
            tmp=sorted(freqDict2[i],reverse=True)
            if tmp and tmp[-1]==1:
                tmp=[14]+tmp[:-1]
            ranktuple+=tmp     
        ranktuple=tuple(ranktuple)    
        pairCountRank={1:2,2:3,3:4,4:7,6:7} 
        if pairCount>0:
            if pairCount not in pairCountRank:
                #print(pairCount,cardList)
                print("  ******  error   ******  ")
                pass
            else:
                rank=[pairCountRank[pairCount],ranktuple]
        else:
            ### Nopair or Straight or Flush             
            Flush=True if len(set(suitList))==1 else False        
            Straight=True if (numList[-1]-numList[0]==5 or numList==[1,10,11,12,13]) else False
            if not(Flush or Straight):
                rank=[1,ranktuple]
            elif Flush and Straight:
                if numList==[1,10,11,12,13]:
                    ranktuple=14
                else:
                    ranktuple=numList[-1]
                rank=[9,ranktuple]
            elif Straight:     
                if numList==[1,10,11,12,13]:
                    ranktuple=14
                else:
                    ranktuple=numList[-1]
                rank=[5,ranktuple]            
            else:
                rank=[6,ranktuple] 
        return rank
        
    # 通过每位玩家有上的底牌，得到已经发出的牌 和 还在发牌员手里的牌
    # 用于MC模拟的初值
    # by hh 2017/10/28  
    def cardsInit(self):
        for i in self.initCards:
            for j in range(2):
                self.existCards.add(i[j])
        entireCards=[]
        for i in range(1,14):
            for j in ['S','H','C','D']:
                if (i,j) not in self.existCards:
                    entireCards.append((i,j)) 
        self.entireCards=entireCards    
        
    # 比较两手牌的大小，返回一个字符串
    # by hh 2017/10/28          
    def compareTwoHands(self,rank1,rank2):
        if rank1[0]>rank2[0]:
            return 'greater'
        elif rank1[0]<rank2[0]:
            return 'less'
        else:
            if rank1[1]>rank2[1]:
                return 'greater'
            elif rank1[1]<rank2[1]:
                return 'less'
            else:
                return 'equal'
                
    # 每位玩家拥有两张底牌 +五张公共牌,从七张牌中挑选出最大的牌型
    # by hh 2017/10/28                 
    def findBestHand(self,cardList):
        ###cardList contains 7 cards 
        BestHand=self.cardType(cardList[:5])
        for i in range(len(cardList)):
            for j in range(i+1,len(cardList)):
                tmp=self.cardType(cardList[:i]+cardList[i+1:j]+cardList[j+1:])
                if self.compareTwoHands(tmp,BestHand)=='greater':
                    BestHand=tmp
        return BestHand

    # 进行 SIM 次模拟, 得到每位玩家获胜的概率
    # 这里假设平局也算赢
    # by hh 2017/10/28     
    def simulate(self,SIM):
        import random
        count=[0]*self.k
        for i in range(SIM):
            cur5Cards=random.sample(self.entireCards,5)
            BestHand=self.findBestHand(self.initCards[0]+cur5Cards)
            BestPeo=[0]
            for j in range(1,self.k):
                tmp=self.findBestHand(self.initCards[j]+cur5Cards)
                if self.compareTwoHands(tmp,BestHand)=='greater':
                    BestHand=tmp
                    BestPeo=[j]
                elif self.compareTwoHands(tmp,BestHand)=='equal':
                    BestPeo.append(j)
            for i in BestPeo:
                count[i]+=1
        return list(map(lambda x:x/SIM,count))
    
    def start(self,SIM):
        self.cardsInit()        
        return self.simulate(SIM)

if __name__=="__main__":
    initCards=[[(5,'H'),(5,'S')],[(13,'S'),(1,'C')],[(9,'D'),(12,'D')]]
    a=TexasPoker(initCards) 
    print(a.start(1000))     