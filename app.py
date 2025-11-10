from dotenv import load_dotenv
from groq import Groq
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr


load_dotenv(override=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.name = "Harsh Chauhan"
        
        # Try to load from environment variables (Secrets) first, fallback to files for local dev
        self.linkedin = os.getenv("LINKEDIN_TEXT")
        if not self.linkedin:
            # Fallback: read from file (for local development)
            try:
                reader = PdfReader("me/linkedin.pdf")
                self.linkedin = ""
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        self.linkedin += text
            except:
                self.linkedin = ""
        
        self.resume = os.getenv("RESUME_TEXT")
        if not self.resume:
            # Fallback: read from file (for local development)
            try:
                reader1 = PdfReader("me/resume.pdf")
                self.resume = ""
                for page in reader1.pages:
                    text = page.extract_text()
                    if text:
                        self.resume += text
            except:
                self.resume = ""
        
        self.summary = os.getenv("SUMMARY_TEXT")
        if not self.summary:
            # Fallback: read from file (for local development)
            try:
                with open("me/summary.txt", "r", encoding="utf-8") as f:
                    self.summary = f.read()
            except:
                self.summary = ""


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def clean_message(self, message):
        """Remove unsupported properties from message for Groq API"""
        if isinstance(message, dict):
            cleaned = {"role": message.get("role"), "content": message.get("content")}
            if "tool_calls" in message:
                cleaned["tool_calls"] = message["tool_calls"]
            return cleaned
        return message
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background, LinkedIn profile and Resume which you can use to answer questions. Please do not share my mobile number with the user.\
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n## Resume:\n{self.resume}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        cleaned_messages = [self.clean_message(msg) for msg in messages]
        done = False
        while not done:
            response = self.groq.chat.completions.create(model="openai/gpt-oss-20b", messages=cleaned_messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                assistant_message = response.choices[0].message
                tool_calls = assistant_message.tool_calls
                results = self.handle_tool_call(tool_calls)
                assistant_msg_dict = {"role": "assistant", "content": assistant_message.content}
                if tool_calls:
                    assistant_msg_dict["tool_calls"] = [{"id": tc.id, "type": tc.type, "function": {"name": tc.function.name, "arguments": tc.function.arguments}} for tc in tool_calls]
                cleaned_messages.append(assistant_msg_dict)
                cleaned_messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(
        me.chat,
        type="messages",
        title=f"{me.name} | Portfolio Assistant",
        description=f"""
        ### 👋 Welcome!
        
        I'm **{me.name}**, your AI assistant for exploring my professional journey, expertise, and experience.
        
        💼 **What you can discover:**
        - Professional background & career journey  
        - Technical skills & expertise  
        - Projects & achievements  
        - Collaboration opportunities
        
        💬 **Get started:** Type your question below or click any example to begin!
        """,
        examples=[
            "What are your key skills and expertise?",
            "Tell me about your recent projects",
            "What sets you apart professionally?",
            "How can I get in touch with you?"
        ],
        theme=gr.themes.Soft(),
        fill_height=True
    ).launch()
    