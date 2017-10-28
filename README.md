# Texas Poker



假设有 K 位玩家参与德州扑克游戏，现在知道每位玩家手中的底牌
利用MC模拟得到每位玩家获胜的概率

假设现在有三位玩家A B C 拿到的底牌分别是:

![a](https://github.com/Hehwang/Texas-Poker/blob/master/pokerImg/a.png)

![b](https://github.com/Hehwang/Texas-Poker/blob/master/pokerImg/b.png)

![c](https://github.com/Hehwang/Texas-Poker/blob/master/pokerImg/c.png)

```python
if __name__=="__main__":
    initCards=[[(5,'H'),(5,'S')],[(13,'S'),(1,'C')],[(9,'D'),(12,'D')]]
    a=TexasPoker(initCards) 
    print(a.start(10000))
```

经过10000次发牌模拟：

得到A B C 赢的概率如下

```
[0.2969, 0.3484, 0.3689]
```

所以！下次拿到小对子还是赶紧溜了～～