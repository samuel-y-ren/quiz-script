import sys
from standard_q import key_prop_gen, prop_keys_gen
from configparser import ConfigParser
import numpy as np
gen_key={"key-prop":key_prop_gen, "prop-keys":prop_keys_gen}
num_questions=10
if len(sys.argv)>1:
    num_questions=sys.argv[1]
configs=ConfigParser()
configs.read("configs.txt") 
categories=dict(configs["CATEGORIES"].items()).keys()
generators=[gen_key[configs["GENERATORS"][i]](configs["CATEGORIES"][i]) for i in categories]
weights=[]
if configs["SETTINGS"]["weighting"] in ("size", "auto"):
    weights=[i.nq for i in generators]
else:
    weights=[1 for i in generators]
t=sum(weights)
weights=[i/t for i in weights]
for i in range(num_questions):
    np.random.choice(generators,p=weights).next_q()