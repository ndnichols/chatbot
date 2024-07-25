import streamlit as st
from openai import OpenAI

ENTITIES = """
# Georgi of Tarnovo
Bulgarian Soldier

Description:
A soldier of the Bulgarian empire, tall and muscular, in his mid-30s. He has a scar running down his left cheek. His military tunic is patched in several places, showing signs of many battles.

Bio:
Georgi is gruff and straightforward, often speaking in a blunt and direct manner. He has a deep sense of honor and loyalty to his comrades, which can sometimes conflict with his current situation as a prisoner. He’s always analyzing his surroundings, looking for tactical advantages—even in casual conversations.

Captured by Viator Mesopotamites Komnenos and interrogated by The Court of the Rose.

# Manuel Kamytzes
Master of Cavalry, Protostrator

Description:
A battle scarred soldier. While pushing 50, he dyes his hair a youthful red and keeps his face clean shaven. He stands out on the battlefield. His horsemanship is unmatched. He is missing a few fingers.

# Wolf
Bio:
Real name is Photios Krivich from Sozopolis.

# Tsar Kaloyan
Tsar of Bulgaria

Bio:

The Byzantine Emperor Alexios III Angelos made Ivanko the commander of Philippopolis (now Plovdiv in Bulgaria). Ivanko seized two fortresses in the Rhodopi Mountains from Kaloyan, but by 1198 he had made an alliance with him. Cumans and Vlachs from the lands to the north of the river Danube broke into the Byzantine Empire in the spring and autumn of 1199. Choniates, who recorded these events, did not mention that Kaloyan cooperated with the invaders, so it is likely that they crossed Bulgaria without his authorization. Kaloyan captured Braničevo, Velbuzhd (now Kyustendil in Bulgaria), Skopje and Prizren from the Byzantines, most probably in that year, according to historian Alexandru Madgearu.

Innocent III’s envoy arrived in Bulgaria in late December 1199, bringing a letter from the Pope to Kaloyan. Innocent stated that he was informed that Kaloyan’s forefathers had come “from the City of Rome”. Kaloyan’s answer, written in Old Church Slavonic, has not been preserved, but its content can be reconstructed based on his later correspondence with the Holy See. Kaloyan styled himself “Emperor of the Bulgarians and Vlachs”, and asserted that he was the legitimate successor of the rulers of the First Bulgarian Empire. He demanded an imperial crown from the Pope and expressed his wish to put the Bulgarian Orthodox Church under the pope’s jurisdiction.

The Byzantines captured Ivanko and occupied his lands in 1200. Kaloyan and his Cuman allies launched a new campaign against Byzantine territories in March 1201. He destroyed Constantia (now Simeonovgrad in Bulgaria) and captured Varna. He also supported the rebellion of Dobromir Chrysos and Manuel Kamytzes against Alexios III, but they were both defeated. Roman Mstislavich, prince of Halych and Volhynia, invaded the Cumans’ territories, forcing them to return to their homeland in 1201. After the Cuman’s retreat, Kaloyan concluded a peace treaty with Alexios III and withdrew his troops from Thrace in late 1201 or in 1202. According to Kaloyan’s letter to the Pope, Alexios III was also willing to send an imperial crown to him and to acknowledge the autocephalous (or autonomous) status of the Bulgarian Church.

# Kumankata
Cuman Raider, Alleged Bride of Kaloyan


Khatun Aymälikä of Clan Terteroba, The Moon Queen, leads the largest tribe of Cumans in Bulgaria. Kumankata means the Cuman woman, the nom de guerre by which she is traditionally known. She claims ancestry from both Vseslav of Polots and Khan Otrok. She is technically the wife of Tsar Kaloyan, but she is not one to wear a crown and other noble fripperies. Instead, she leads raiding parties into the Empire with her tribesmen. Her aim is to ensure the Empire is kept off balance so that her husband can consolidate power.

In 1197 she led a particularly devastating raid into Thrace and Macedonia. Her forces raided a large religious festival near Zorolus in a town called Kouperion. They burned a monastery and carried off many treasures, including an icon of St. George in gold leaf, cinnabar, and lapis lazuli before being thrown back by the forces of Manuel Kantakouzenos out of Bizye. She retains the icon, though she does not appear to be a practicing Christian save when her attendance at court demands it.

Her raiding party consists of about 100 warriors, a similar amount of noncombatants, and herds of cattle and goats protected by Komondor dogs. Their camp is mobile, called a Cuman tower. It moves when the local pastures are exhausted or when Byzantine troops encroach.

She has two children, a daughter and a son.

# The Elect
Faithful Bogomils and peasant hangers on in the vicinity of Develtos. The follow the ostensible leadership of Offal. They became a force thanks to Michael Ephesius manipulating them into attacking Aniketos Kantakouzenos during the ordination of Offal as Develtos’s priest.

# Viator Mesopotamites Komnenos
Count, Accomplished General and Slavetrader

Bio:
Count (Komes) Viator Komnenos of House Komnenos. Viator once lead a banda of 100 light cavalry koursores (corsairs) that suffered terrible losses during the imperial defeat at the Battle of Baktounion.

While an accomplished cavalry raider, Komes Viator distinguished himself primarily in the capture and sale of slaves. Slavery is a lucrative trade for the empire, and even losing military campaigns can still turn a profit for the officers in the acquisition of chattel. Komes Viator enriched himself and his house by this trade, and his leading a banda of outriders provided him ample opportunity for plunder. He set up a trade network leading from Bulgaria through Thrace to Constantinople that could be co-opted for material gain. Manuel Kamytzes attested to the character of the Komes. Plunder was how most soldier enriched themselves and was not looked down upon.

He offered his services to Euphrosyne Doukaina Kamatera in bringing order to Develtos. If she was satisfied with his service, he hoped she would bestow a formal title upon him.
"""

SYNOPSIS = """
Viator escorted the retinue to the Kaleto’s undercroft where they met three prisoners: Dobo of Skafida, a former resident of the Black Sea Coast who lost his family to Archon Krivich’s crackdown. He is a member of The Elect;
Katerina of Aetos, a young passionate member of the Elect who was eager to hurl invectives at her captors;
Georgi of Tarnovo, a Bulgarian soldier. Manuel and Wolf began to speak with Georgi and learned he was sent by Tsar Kaloyan to rescue the Kumankata. The Elect approached his band with an offer of aid. The Bulgarians accepted it, but don’t share their heresy. He was forthcoming with his purpose and eager to avoid torture.
"""

DECISION = """
The reader decides whether Manuel frees Georgi and gives him a horse to report back to the Tsar, or whether to leave Georgi in prison.
"""

STYLE = """
Dark modern fiction
"""

# Show title and description.
st.title("LOOM")
st.write("Blades in the Latin Quarter")

def syncLLMCall(client, role, content):
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    st.session_state.messages.append({
        'role': role,
        'content': content
    })
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ])

    response_text = ""
    for chunk in response:
        if isinstance(chunk, tuple) and chunk[0] == 'choices':
            for choice in chunk[1]:
                response_text += choice.message.content
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    return response_text

def generateFirstDraft(client):
    prompt = f"""
    I want you to generate a short fictional scene that is 600-800 words long and in the style of {STYLE}

    The plot of the scene should follow {SYNOPSIS}

    It should build to a decision for the reader to make at the end. The decision for the reader to make is: {DECISION}

    Here is a bunch of context about the characters and locations in the story that you should use to ground the scene. Assume the reader is generally familiar with the characters already. The context is: {ENTITIES}
    """
    return syncLLMCall(client, 'system', prompt)

def getFeedback(client):
    prompt = """
    Consider that your first draft. Now review the draft and come up with three concrete improvements you could make.
    """
    return syncLLMCall(client, 'system', prompt)

def generateFinalDraft(client):
    prompt = """
    Please rewrite the first draft into a final draft, following your own editorial guidance and making whatever other improvements you see fit.
    """
    return syncLLMCall(client, 'system', prompt)
    
# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    if st.button("Write Scene"):
        if not openai_api_key:
            st.error("Please enter your API key")
        else:
            with st.spinner('Generating first draft...'):
                # Create an OpenAI client.
                client = OpenAI(api_key=openai_api_key)
                first_draft = generateFirstDraft(client)
            with st.expander("First Draft", expanded=False):
                st.markdown(first_draft)
                # st.write('# First Draft')
                # st.write(first_draft)
            with st.spinner('Getting feedback...'):
                feedback = getFeedback(client)
            with st.expander("Editorial Feedback", expanded=False):
                st.markdown(feedback)
                # st.write('# Editorial Feedback')
                # st.write(feedback)
            with st.spinner('Generating final draft...'):
                final_draft = generateFinalDraft(client)
            st.write(final_draft)
