# these are standard functions to create questions for
from random import randrange, choice
from copy import deepcopy
import numpy as np

def valid_yn() -> bool:
    while True:
        v=input().lower()
        if (v=='y' or v=="yes"):
            return True
        elif (v=='n' or v=="no"):
            return False
        print("Invalid input")

def valid_intype(t: type):
    while True:
        v=input()
        try:
            return t(v)
        except:
            print("Invalid input")

def attempt_convert(s):
    if (type(s) != str):
        return s
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            return s

def cs_set(s):
    st=['']
    for i in s:
        if i in ",;|:.":
            st.append('')
        else:
            st[-1]+=i
    return set([i.strip() for i in st if len(i)])

def lowered(st):
    return {i.lower() if type(i)==str else i for i in st}

def input_matches(ans, correction=True):
    dt=type(ans)
    if dt==set:
        x=cs_set(input())
        if (lowered(x)==lowered(ans)):
            print("✅")
        elif correction:
            print(f"Correct answer: {ans}")
            print("Is your answer close enough? [Y/N]")
            print("✅" if valid_yn() else "❌")
        else:
            print(f"❌\nCorrect answer: {ans}")
        return
    x=valid_intype(dt)
    if dt==int:
        print("✅" if ans==x else f"❌\nCorrect answer: {ans}")
    elif dt==float:
        print("✅" if abs(1-ans/x)<1e-6 else f"❌\nCorrect answer: {ans}")
    elif dt==str and x.lower()==ans.lower():
        print("✅")
    elif correction:
        print("Correct answer:",ans)
        print("Is your answer close enough? [Y/N]")
        print("✅" if valid_yn() else "❌")
    else:
        print(f"❌\nCorrect answer: {ans}")

def load_prop_table(file_name):
    f=open(file_name,'r')
    val=f.read().split('\n')
    f.close()
    val=[[j.strip() for j in i.split(';')] for i in val]
    for i in range(1,len(val[0])):
        match val[1][i]:
            case "set":
                for j in range(2,len(val)):
                    val[j][i]=cs_set(val[j][i])
            case "int":
                for j in range(2,len(val)):
                    val[j][i]=int(val[j][i])
            case "float":
                for j in range(2,len(val)):
                    val[j][i]=float(val[j][i])
            case "bool":
                for j in range(2,len(val)):
                    val[j][i]="ny"[int(val[j][i])]
    return [i for i in val if len(i)]

def load_weights(file_name):
    f=open(file_name,'r')
    wg=f.read().split('\n')
    f.close()
    wg=list(map(float,[j.strip() for i in wg for j in i.split(';') if len(j.strip())]))
    sm=sum(wg)
    return [i/sm for i in wg]

def to_bool(s):
    return s in ('1','true','True')

# asks about a random property of an object
class key_prop_gen():
    def __init__(self, file_name, **kw): # first line is titles, second is type of answer
        self.v=load_prop_table(file_name+".txt")
        self.ni=len(self.v)-2
        self.np=len(self.v[0])-1
        self.nq=self.ni*self.np
        self.p=load_weights(file_name+"-weights.txt")
        self.correction=(not "correction" in kw or to_bool(kw["correction"]))
    def next_q(self):
        ci=np.random.choice(self.nq,p=self.p)
        ri,rp=ci//self.np+2,ci%self.np+1
        match self.v[1][rp]:
            case "bool":
                print(f"Is the {self.v[0][0]} {self.v[ri][0]} {self.v[0][rp]}? (Y/N)")
            case "set":
                print(f"What are the {self.v[0][rp]} of the {self.v[0][0]} {self.v[ri][0]}? ({len(self.v[ri][rp])})")
            case _:
                print(f"What is the {self.v[0][rp]} of the {self.v[0][0]} {self.v[ri][0]}? ({self.v[1][rp]})")
        input_matches(self.v[ri][rp], correction=self.correction)
            
# given a property, ask about all the objects that fall into it
class prop_keys_gen():
    def __init__(self, file_name): # first line is titles, second is type opf property
        vals=load_prop_table(file_name+".txt")
        self.np=len(vals[0])-1
        self.ni=len(vals)-2
        self.vt=vals[0][0]
        self.pp=vals[0][1:]
        self.tp=vals[1][1:]
        self.qs=[{}]*self.np
        for i in range(self.np):
            for j in range(2,self.ni+2):
                if (vals[j][i+1] in self.qs[i]):
                    self.qs[j][vals[j][i+1]].append(vals[j][0])
                else:
                    self.qs[j][vals[j][i+1]]=[vals[j]]
            self.qs[j][vals[j][i+1]]=set(self.qs[j][vals[j][i+1]])
        self.nq=0
        for i in self.qs:
            self.nq+=len(i)
    def next_q(self):
        ri=randrange(0,self.np)
        rq=choice(self.qs[ri].keys())
        print(f"What {self.vt}(s) have {self.pp} equal to {rq}? ({len(self.qs[ri][rq])} answers)")
        input_matches(self.qs[rq])