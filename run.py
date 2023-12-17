import pathlib
from flask import Flask, request, jsonify
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

app = Flask(__name__)



class TextFunction:
    def __init__(self):
        genai.configure(api_key='AIzaSyAVZxHJmx9cJRVHw26hrl0nzgl8pi4_Mlc')
        self.model = genai.GenerativeModel('gemini-pro')
        self.messages = []


    def forward(self, text):
      self.messages = [{'role':'user',
                   'parts': ["Physics teacher and gave answer when user ask."]}]
      response = self.model.generate_content(self.messages)
      self.messages.append({'role':'model',
                       'parts':[response.text]})
      self.messages.append({'role':'user',
                 'parts':[f"{text}"]})
      response = self.model.generate_content(self.messages)
      X = self.to_markdown(response.text)
      return X.data

    def to_markdown(self, text):
      text = text.replace('•', '  *')
      return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



text_function = TextFunction()


@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    user_input = data.get("input", " ")
    result = text_function.forward(user_input)
    return jsonify({'result': str(result)})

if __name__ == '__main__':
    app.run(debug=True, port=2000)
