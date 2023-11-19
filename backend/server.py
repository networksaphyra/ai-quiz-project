from flask import Flask, request
from question_generator import QuestionGenerator
import ai_config
import openai

class RequestHandler:
    def __init__(self):
        self.app = Flask(__name__)
        openai.api_key = ai_config.API_KEY
        self.question_generator = QuestionGenerator()

    def send_generated_questions(self, client_data) -> dict:
        topic = client_data["topic"]
        multiple_choice_num = client_data["multipleChoice"]
        short_answer_num = client_data["shortAnswer"]
        true_or_false_num = client_data["trueOrFalse"]

        ai_config.MULTIPLE_CHOICE_QUESTION_NUM = multiple_choice_num
        ai_config.SHORT_ANSWER_QUESTION_NUM = short_answer_num
        ai_config.TRUE_OR_FALSE_QUESTION_NUM = true_or_false_num

        generated_questions = []
        generated_questions.append(self.question_generator.generate_multiple_choice_question(topic))
        generated_questions.append(self.question_generator.generate_short_answer_question(topic))
        generated_questions.append(self.question_generator.generate_true_or_false_question(topic))
        
        return {'generated_questions': generated_questions}, 200

    def check_short_answer(self, client_data) -> dict:
        pass

    def handle_requests(self) -> dict:
        client_data = request.json
        if client_data["check"]:
            return self.check_short_answer(client_data=client_data)
        else:
            return self.send_generated_questions(client_data=client_data)

    def run_server(self):
        @self.app.route("/members", methods=["POST"])
        def handle_requests_wrapper():
            return self.handle_requests()

        self.app.run(debug=True)

if __name__ == '__main__':
    handler = RequestHandler()
    handler.run_server()
