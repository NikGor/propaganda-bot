import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import argparse
import sys


# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def analyze_news_with_chatgpt(news_text):
    best_parameters = {
        "manipulations": """List of manipulations: 
        Appeal to Authority: This technique strengthens a claim by citing a source considered authoritative, regardless of its actual expertise in the relevant field.
      Conversation Killer: This technique uses clichés or phrases to discourage further discussion or critical thinking, often masquerading as wisdom to shut down debate.
      Doubt: This technique undermines someone's credibility or an entity's quality by questioning their character or actions, rather than addressing the argument directly.
      Appeal to Values: This technique reinforces an argument by associating it with widely respected values, using these values as authoritative support.    Slogans: A brief and striking phrase that may include labeling and stereotyping. Slogans tend to act as emotional appeals.
      Straw Man: This technique misrepresents an opponent's argument with a distorted or exaggerated version, then refutes this weaker version, creating the illusion of defeating the original argument.
      Whataboutism: A technique that attempts to discredit an opponent’s position by charging them with hypocrisy""",
        "output_format": """Create a valid JSON array of sentences with manipulations that you have found in the text:
        'Appeal_to_Authority': [list of sentences],
          'Conversation_Killer': [list of sentences],
          'Doubt': [list of sentences],
          'Appeal_to_Values': [list of sentences],
          'Straw_Man': [list of sentences],
          'Whataboutism': [list of sentences]""",
        "model": "gpt-3.5-turbo"
    }

    prompt = f"""You are a helpful journalistic assistant assessing the level of propagandistic manipulation. You need to analyze news text on manipulations techniques.
News text: "{news_text}"
List of manipulations: "{best_parameters['manipulations']}"
Create a valid JSON array of sentences with manipulations that you have found in the text: "{best_parameters['output_format']}"
If there is no manipulations in the text you need to return empty JSON file."""

    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        messages=[
                    {"role": "user", "content": prompt},
                ]
            )
        output = response.choices[0].message.content

        # try:
        #     output = json.loads(result_text)
        # except json.JSONDecodeError:
        #     output = result_text
    except openai.OpenAIError as e:
        output = {"error": str(e)}

    return output


def main():
    parser = argparse.ArgumentParser(description="Analyze news text for propagandistic manipulation using OpenAI's GPT.")
    parser.add_argument("news_text", type=str, help="The news text to analyze.")

    args = parser.parse_args()

    result = analyze_news_with_chatgpt(args.news_text)
    # Instead of printing, write the JSON output to stdout, making it easier to capture in a script.
    sys.stdout.write(result)

