from flask import Flask, request, jsonify, render_template
from rapidfuzz import process, fuzz
import os
import string

app = Flask(__name__)

# Predefined Q&A dictionary
custom_qna_raw = {
    "tell me about kalki fashion": (
        "Born in Mumbai, India in 2007, KALKI evokes the very spirit of the city it was founded in. "
        "An upstart, innovative, and dynamic brand – KALKI – offers the best of contemporary, ethnic Indian fashion "
        "and fusion-wear styles. Staying true to the brand’s unique promise of premium and wearable fashion, "
        "KALKI unveils fresh collections and all-new designs throughout the fashion calendar. "
        "KALKI’s design and aesthetic sensibility seek inspiration from all walks of life—be it the beauty of nature "
        "and heritage in art, architecture and culture, intricate creations, and the modern world to the home-bound "
        "handloom traditions of India."
    ),
    "kalkis vision": (
        "To be a company that is a benchmark in the Indian fashion industry for its offerings and experiences."
    ),
    "kalkis mission": (
        "To be a preferred company of choice in Indian fashion globally for its delightful customer service, and "
        "quality product offerings by constantly evolving using innovation and design."
    ),
    "kalkis founders": (
        "Chairman: Mr Shravan Gupta, CEO: Mr Saurabh Gupta, Directors: Mr Shishir Gupta and Mr Nishit Gupta."
    ),
    "who is the hr head": (
        "Ms Fatema Merchant, contact no: +91 7738057566 and email: fatemamerchant@kalkifashion.com"
    ),
    "hr head": (
        "Ms Fatema Merchant, contact no: +91 7738057566 and email: fatemamerchant@kalkifashion.com"
    ),
    "what do you do": (
        "We offer a wide range of premium ethnic and fusion fashion collections inspired by Indian heritage and modern trends."
    ),
    "when will the appraisal process begin": (
        "The appraisal schedule will be communicated shortly."
    ),
    "when will the salary be credited": (
        "Salaries are generally credited in the first week of every month. However, there may be occasional delays due to unforeseen circumstances."
    ),
    "when will the referral bonus be credited": (
        "The referral amount will be processed once the referred candidate completes 3 months of employment."
    ),
    "my designation has been changed when will it reflect in keka": (
        "Designation changes take some time to reflect in the system. Please allow a few days for the update."
    ),
    "when will my pf amount be credited to my account": (
        "Provident Fund (PF) amounts are typically credited within 15 days of the salary being processed."
    ),
    "when will my regularization be completed": (
        "Regularization will be completed once your reporting manager initiates and approves the process."
    ),
    "what about my attendance regularisation?": (
        "Regularization will be completed once your reporting manager initiates and approves the process."
    ),
    "attendance regularisation": (
        "Regularization will be completed once your reporting manager initiates and approves the process."
    ),
    "what is the breakdown of my salary": (
        "Salary bifurcation may vary based on factors such as unpaid leave or extra days worked. Please refer to your salary slip for details."
    ),
    "when will i receive my appointment letter": (
        "These documents are in the system, but there has been difficulty retrieving them. The concerned team is working on it."
    ),
    "when will i receive my confirmation letter": (
        "These documents are in the system, but there has been difficulty retrieving them. The concerned team is working on it."
    ),
    "when will i receive my increment letter": (
        "These documents are in the system, but there has been difficulty retrieving them. The concerned team is working on it."
    ),
    "what will be my referral bonus amount": (
        "The referral bonus amount depends on the referred candidate’s salary package."
    ),
    "how much has been deducted from my salary": (
        "Please check the Loss of Pay (LOP) sheet shared with your reporting manager for the deduction details."
    ),
    "what is my salary deduction": (
        "Please check the Loss of Pay (LOP) sheet shared with your reporting manager for the deduction details."
    ),
    "how much is my incentive": (
        "Incentive details can be found in the LOP sheet sent to your manager."
    ),
    "who are the directors?": (
        "Directors: Mr Shishir Gupta and Mr Nishit Gupta."
    ),
    "the teamlease app is not opening what should i do": (
        "Please contact the TeamLease representative. Their contact number is available with your manager."
    ),
    "when will i receive my id card": (
        "Please coordinate with Ms Netra Puralkar- netra@kalkifashion.in for ID card issuance."
    ),
    "what is this chatbot for": (
        "This chatbot handles common HR queries like salary, documents, PF, attendance, and more - so you don’t need to contact HR for routine concerns."
    ),
    "has my form 16 been uploaded in keka": (
        '<a href="https://app.keka.com/account/login" target="_blank">Yes, Form 16 has been uploaded in Keka. You can access it through your employee portal.</a>'
    ),
    "kalki website": (
        '<a href="https://in.kalkifashion.com/" target="_blank">Click here to visit the Kalki Fashion website</a>'
    ),
    "keka portal": (
        '<a href="https://app.keka.com/account/login" target="_blank">Click here to log in to the Keka portal</a>'
    ),
}

# Greeting, WhatsUp, Goodbye sets
greeting_phrases = {
    "hi", "hello", "hey", "hiya", "yo", "good morning", "good afternoon", "good evening",
    "heyy", "help", "need help", "hii", "helloo", "need assistance", "assistance"
}

whatsup_phrases = {
    "whats up", "what's up", "wyd", "what are you doing?", "how are you?", "how are u"
}

goodbye_phrases = {
    "bye", "goodbye", "see you", "see you later", "talk to you later", "thanks",
    "thank you", "thank u", "thankss", "hehe", "adios", "sayonara"
}

fallback_response = "I'm sorry, I didn't understand that."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    raw_input = data.get("message", "")
    if not raw_input.strip():
        return jsonify({"response": "Please type something."})

    user_input = raw_input.lower().strip()
    user_input = user_input.translate(str.maketrans('', '', string.punctuation))

    if user_input in whatsup_phrases:
        return jsonify({"response": "Nothing much, how can I assist you today?"})
    if user_input in greeting_phrases:
        return jsonify({"response": "Hello! How can I assist you today?"})
    if user_input in goodbye_phrases:
        return jsonify({"response": "Let me know if you have any other questions :)"})

    if user_input in custom_qna_raw:
        return jsonify({"response": custom_qna_raw[user_input]})

    best_match, score, _ = process.extractOne(
        user_input, list(custom_qna_raw.keys()), scorer=fuzz.token_set_ratio
    )

    if score >= 70:
        return jsonify({"response": custom_qna_raw[best_match]})
    else:
        return jsonify({"response": fallback_response})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
