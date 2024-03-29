import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
import re

_SYSTEM_INSTRUCTION = """
You are a helpful assistant that reads reddit posts and comments about financial troubles surrounding IVF and extracts / summerises:
    1. The question being asked
    2. The answered provided by the comments
With the goal of understanding all the 
"""

_SHOT_1_INPUT = """
POST:
Charging Husbands Insurance?
We are doing the process for PGT-M reasons and have gone through our first round of IVF and have day 5 blasts. 
To this point everything was being charged to me but I was thinking once an egg is fertilized and an embryo is created, 
everything is half him as well. I could argue that some of the procedures such as fertilization or genetic testing of 
embryos can be charged to his fertility insurance.
But my insurance/finance rep at my clinic never flagged this as an option. I wanted to ask if anyone has had successfully 
charged some post embryo IVF related procedures to thier male partners insurance? If so which ones?
COMMENTS:
1. My clinic was really reluctant to do that. The invoice needs to be generated in the name of the patient who is going to be billed. My clinic told me that they must be informed before the procedure is performed and that we have to submit the invoice to husband's insurance by yourself. I'd ask your clinic exactly what you need to do to bill your husband's insurance. Alternatively, another option is to exhaust your insurance and switch to husband's insurance. You may be able to get more cycles covered this way.
2. I am in the midst of this right now. My clinic refuses to bill anything to insurance that is donor related, and they seem so bewildered by that possibility, which is absurd  - they are a fertility clinic, that's all they do! I think they just don't want to do the work.\n\nSo I am billing it myself. It's a pain, but for tens of thousands of dollars, worth it! We have maxed out my fertility benefits with 3 rounds of own egg IVF and are making progress getting our donor cycle covered under my husband's insurance. Embryology and embryo testing as well. I wish I had known about this earlier, I'd have tried to get some of the embryology and testing costs covered under his insurance in our earlier IVF rounds too. The whole \"you're the girl, so everything IVF related is on you\" thing is so dumb.\n\nThey sure don't make anything easy on us! The main thing I've learned is to always double check and follow up and ask a million questions to make sure! They don't always know what they are talking about, don't always do it right and don't always tell you all the options. So frustrating, but we'll get through it. Good luck!
"""
_SHOT_1_OUTPUT = """Q: Asks if IVF-related procedures post-embryo creation can be billed to the male partner's fertility insurance, given the involvement of both partners.
A: Clinics might resist billing the male partner’s insurance. It may require patients to submit invoices directly to the husband’s insurance. Some manage to switch billing to the husband's insurance for broader coverage."""


llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = ChatPromptTemplate.from_messages([
    ("system", _SYSTEM_INSTRUCTION),
    ("human", _SHOT_1_INPUT),
    ("ai", _SHOT_1_OUTPUT),
    ("human", """
POST: {post}
COMMENTS: {comments}
""")
])

def extract_qa(text):
    question = text.split("\n")[0][3::]
    answer = text.split("\n")[1][3::]
    return dict(question=question, answer=answer)

extract_model = prompt | llm | StrOutputParser() | extract_qa