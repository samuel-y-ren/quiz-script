# these are standard functions to create questions for
from random import randrange, choice
from copy import deepcopy

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
        
def input_matches(ans):
    dt=type(ans)
    x=valid_intype(dt)
    if dt==int:
        print("✅" if dt==x else "❌")
    elif dt==float:
        print("✅" if abs(1-dt/x)<1e-6 else "❌")
    elif dt==str:
        print("✅")
        return
    print("Correct answer:",ans)
    print("Is your answer close enough? [Y/N]")
    print("✅" if valid_yn() else "❌")
        
# unique keys map to definitions
# gives definition and asks for key
class def_key_gen():
    def __init__(self, vals, atp="definition"):
        self.atp=atp
        self.nq=len(vals)-1
        self.v=deepcopy(vals)
        for i in range(1,self.nq+1):
            assert type(self.v[i][1] in (str, int, float))
            self.v[i][1]=attempt_convert(self.v[i][1])
        self.ri=-1
    def next_q(self):
        self.ri=randrange(0,self.l)
        cv=self.v[self.ri]
        print(f"What is the {self.atp} of {cv[0]}?")
        input_matches(cv[1])

class key_def_gen():
    def __init__(self, vals):
        self.nq=len(vals)
        self.v=vals
        for i in range(self.nq):
            assert type(self.v[i][1] in (str, int, float))
            self.v[i][1]=attempt_convert(self.v[i][1])
            self.v[i][0]=self.v[i][0].lower()
        self.ri=-1
    def next_q(self):
        self.ri=randrange(0,self.l)
        cv=self.v[self.ri]
        if (type(cv[1])==str):
            print("What fits the description: "+cv[1]+'?')
        else:
            print("What has the value of: "+cv[0]+'?')
        input_matches(cv[0])

# asks about a random property of an object
class key_prop_gen():
    def __init__(self, vals): # first line is titles, second is type of answer
        self.v=vals
        self.ni=len(vals)-2
        self.np=len(vals[0])-1
        self.nq=self.ni*self.nq
        for i in range(1,self.np+1):
            if self.v[1][i]=="str":
                for j in range(2,self.ni+2):
                    self.v[i][j]=self.v[i][j].lower()
    def next_q(self):
        ri=randrange(2,self.ni+2)
        rp=randrange(1,self.np+1)
        print(f"Is the {self.v[0][0]} {self.v[ri][0]} {self.v[0][rp]}?" + ("(Y/N)" if self.v[1][rp]=="bool" else self.v[1][rp]))
        input_matches(self.v[ri][rp])
            
# given a property, ask about all the objects that fall into it
class prop_keys_gen():
    def __init__(self, vals): # first line is titles, second is type opf property
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
        x=input()
        st=[]
        for i in x:
            if i in ",;|:.":
                st.append('')
            else:
                st[-1]+=i
        st=[i.strip() for i in st if len(i)]
        if (set(i)==self.qs[rq]):
            print("✅")
        else:
            print(f"Correct answer: {self.qs[rq]}")
            print("Is your answer close enough? [Y/N]")
            print("✅" if valid_yn() else "❌")
