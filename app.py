import os
import chainlit as cl
from groq import Groq

# Groq Client එක (API Key එක Environment Variable එකෙන් ගනී)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# AI එකට පෞරුෂයක් ලබා දීම (System Prompt)
SYSTEM_PROMPT = "You are Alpha AI, a sophisticated, helpful, and ultra-fast assistant. You provide clear and concise answers."

@cl.on_chat_start
async def start():
    # Chat පටන් ගන්නා විට පෙන්වන Avatar එක සහ පණිවිඩය
    await cl.Avatar(
        name="Alpha AI",
        url="https://api.dicebear.com/7.x/bottts/svg?seed=Alpha"
    ).send()
    
    # චැට් හිස්ට්‍රිය තබා ගැනීමට ලිස්ට් එකක් සකස් කිරීම
    cl.user_session.set("message_history", [{"role": "system", "content": SYSTEM_PROMPT}])
    
    await cl.Message(content="🌟 **Alpha AI සක්‍රියයි.** මම ඔබට අද කොහොමද උදව් කරන්නේ?").send()

@cl.on_message
async def main(message: cl.Message):
    # කලින් කතා කරපු දේවල් ලබා ගැනීම
    history = cl.user_session.get("message_history")
    history.append({"role": "user", "content": message.content})

    # හිස් Message එකක් සකස් කිරීම (Streaming සඳහා)
    msg = cl.Message(content="", author="Alpha AI")
    
    # Groq හරහා පිළිතුර ලබා ගැනීම
    response = client.chat.completions.create(
        model="llama3-70b-8192", # සුපිරිම වේගයක් සහ බුද්ධියක් තියෙන මොඩල් එක
        messages=history,
        stream=True,
    )

    full_answer = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            token = chunk.choices[0].delta.content
            full_answer += token
            await msg.stream_token(token)

    # පිළිතුර සම්පූර්ණ වූ පසු හිස්ට්‍රියට එකතු කිරීම
    history.append({"role": "assistant", "content": full_answer})
    cl.user_session.set("message_history", history)
    
    await msg.send()
