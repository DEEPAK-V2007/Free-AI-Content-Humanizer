from flask import Flask,render_template,request
from groq import Groq
from dotenv import load_dotenv ##pip install python-dotenv
import os

load_dotenv()
api_key= os.getenv("GROQ_API_KEY")##loading apikey from the .env file and tranforing it to api_keys variable

client=Groq(api_key=api_key)##configure and no need for model selection

app= Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/humanize",methods=["POST"])
def humanize():
    ai_text= request.form["AI_text"]
    try:
        firstitr=humanize_text1(ai_text)
        secoitr=humanize_text2(firstitr)
        thirditr=humanize_text3(secoitr)
        return render_template("result.html",original=ai_text,humanized=thirditr)
    except Exception as e:
        return render_template("result.html",original=ai_text,humanized=f"Error: {str(e)}")
@app.route("/retest",methods=["POST"])
def retest():
    ai_text= request.form["original_text"]
    try:
        firstitr=humanize_text1(ai_text)
        secotr=humanize_text2(firstitr)
        thirditr=humanize_text3(secotr)
        return render_template("result.html",original=ai_text,humanized=thirditr)
    
    except Exception as e:
        return render_template("result.html",original=ai_text,humanized=f"Error: {str(e)}")


def humanize_text1(text):
    prompt=f""" Rewrite the following text as a student would write it.

    Strict Rules:
    - Keep it roughly the SAME LENGTH as the original
    - Do NOT add any new information or examples
    - Do NOT repeat any information
    - Use simple plain words a student would use
    - Use contractions like don't, can't, it's naturally
    - Do NOT overuse filler words — use at most ONE per paragraph
    - Keep the same structure as the original
    - Written format only
    - Output only the rewritten text, nothing else
    Text to humanize:{text}
    """
    response=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role":"system",
                "content":"You are a student who rewrites text simply and naturally. You never add extra information. You keep rewrites the same length as the original."
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=1.3,
        max_tokens=4096
    )
        
    return response.choices[0].message.content

def humanize_text2(text):
    prompt=f"""Clean up the following text.

    Strict Rules:
    - Remove any repeated information
    - Remove any unnecessary comparisons or examples
    - Remove any over explanation
    - Keep only the core information from the original
    - Make sure length is similar to what a student would write
    - Simple plain language only
    - Output only the cleaned text, nothing else
    Text to humanize: {text}
    """
    response=client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role":"system",
            "content":"You are an editor who removes unnecessary content and keeps text clean and concise."
        },
        {
            "role":"user",
            "content":prompt
        }
    ],
    temperature=1.2,
    max_tokens=4096
    )

    return response.choices[0].message.content
    
def humanize_text3(text):
    prompt=f"""You are a real college student doing a final edit on your assignment.
    
    Strict Rules:
    1. Keep the SAME LENGTH as the input — do not make it longer
    2. Do not add new information or examples
    3. Write exactly like a real student would:
       - Occasionally miss a comma
       - Use informal short forms like "it's", "they're", "won't", "can't"
       - Sometimes use simpler wrong word instead of correct fancy word
         example: use "make" instead of "produce"
         example: use "use" instead of "utilize"  
         example: use "need" instead of "require"
         example: use "show" instead of "demonstrate"
         example: use "help" instead of "facilitate"
       - Write short simple sentences — max 15 words per sentence
       - Avoid all transition words like however, moreover, additionally
       - Never start with "The" for every sentence — vary the starts
    4. Do NOT use these words at all:
       furthermore, thus, hence, utilize, crucial, pivotal,
       commendable, notably, straightforward, this ensures,
       importantly, in conclusion, in summary, overall,
       it is important to note, additionally, moreover,
       consequently, subsequently, regarding, demonstrate,
       facilitate, implement, leverage, optimize, streamline
    5. Written format only — no questions
    6. Output only the final text nothing else
    Text:
    {text}
    """
    response=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role":"system",
                "content":"You are a real college student editing your assignment. You write simply, imperfectly and naturally. You use short simple sentences. You never sound like AI."
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=1.0,
        max_tokens=4096
    )
    return response.choices[0].message.content

if(__name__=="__main__"):
    app.run(debug=False, host='0.0.0.0', port= 5000)