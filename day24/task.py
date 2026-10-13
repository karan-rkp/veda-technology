
# ==========================================
# CLI QUIZ APPLICATION
# Python Programming Track - Task 24
# ==========================================

import json
import random
from pathlib import Path

QUESTIONS_FILE = Path(__file__).with_name("quick.json")


# ------------------------------------------
# LOAD QUESTIONS FROM JSON
# ------------------------------------------
def load_questions():
    try:
        with QUESTIONS_FILE.open("r", encoding="utf-8") as file:
            questions = json.load(file)

        if not isinstance(questions, list) or not questions:
            raise ValueError("Question file must contain a non-empty list.")

        for question in questions:
            if not isinstance(question, dict):
                raise ValueError("Each question must be an object.")

            if not all(key in question for key in
                       ("question", "options", "answer")):
                raise ValueError("A question is missing required fields.")

            if not isinstance(question["options"], list) or not question["options"]:
                raise ValueError("Each question must have a list of options.")

            if not isinstance(question["answer"], str):
                raise ValueError("Each answer must be a string.")

            if question["answer"].upper() not in [
                option.upper() for option in question["options"]
            ]:
                raise ValueError("Correct answer must match one of the options.")

        return questions

    except FileNotFoundError:
        print(f"Error: {QUESTIONS_FILE.name} was not found.")
        print("Create the questions.json file in the same folder.")
        return []

    except (json.JSONDecodeError, ValueError) as error:
        print(f"Error in question file: {error}")
        return []

    except OSError as error:
        print(f"Could not read question file: {error}")
        return []


# ------------------------------------------
# DISPLAY QUESTION
# ------------------------------------------
def ask_question(question_data, question_number, total_questions):
    print("\n" + "=" * 50)
    print(f"Question {question_number}/{total_questions}")
    print(question_data["question"])
    print("-" * 50)

    options = question_data["options"]

    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    while True:
        answer = input("\nEnter option number or answer text: ").strip()

        if not answer:
            print("Answer cannot be empty. Try again.")
            continue

        # Allow either option number or answer text
        if answer.isdigit():
            option_number = int(answer)

            if 1 <= option_number <= len(options):
                selected_answer = options[option_number - 1]
                break

            print(f"Enter a number between 1 and {len(options)}.")

        else:
            matched_option = next(
                (option for option in options
                 if option.lower() == answer.lower()),
                None
            )

            if matched_option is not None:
                selected_answer = matched_option
                break

            print("Invalid answer. Select an option shown above.")

    correct_answer = question_data["answer"]

    if selected_answer.lower() == correct_answer.lower():
        print("Correct answer!")
        return True

    print(f"Incorrect! Correct answer: {correct_answer}")
    return False


# ------------------------------------------
# SHOW FINAL RESULT
# ------------------------------------------
def show_result(score, total_questions):
    percentage = (score / total_questions) * 100

    print("\n" + "=" * 50)
    print("             QUIZ RESULT")
    print("=" * 50)
    print(f"Total Questions : {total_questions}")
    print(f"Correct Answers : {score}")
    print(f"Wrong Answers   : {total_questions - score}")
    print(f"Final Score     : {score}/{total_questions}")
    print(f"Percentage      : {percentage:.2f}%")

    if percentage >= 80:
        print("Performance     : Excellent!")
    elif percentage >= 60:
        print("Performance     : Good job!")
    elif percentage >= 40:
        print("Performance     : Keep practicing!")
    else:
        print("Performance     : Practice more and try again!")

    print("=" * 50)


# ------------------------------------------
# MAIN QUIZ
# ------------------------------------------
def start_quiz():
    questions = load_questions()

    if not questions:
        return

    player_name = input("Enter your name: ").strip()

    if not player_name:
        player_name = "Player"

    random.shuffle(questions)

    print("\n" + "=" * 50)
    print("          WELCOME TO PYTHON QUIZ")
    print("=" * 50)
    print(f"Good luck, {player_name}!")
    print(f"Number of questions: {len(questions)}")
    input("\nPress Enter to start the quiz...")

    score = 0

    for number, question in enumerate(questions, start=1):
        if ask_question(question, number, len(questions)):
            score += 1

    print(f"\nWell done, {player_name}!")
    show_result(score, len(questions))


# ------------------------------------------
# PROGRAM ENTRY POINT
# ------------------------------------------
if __name__ == "__main__":
    start_quiz()
