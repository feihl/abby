from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import requests

# Base URL of the FastAPI app
BASE_URL = 'http://127.0.0.1:8000'  # Replace with the actual URL of your FastAPI app

# Create the main screen manager
screen_manager = ScreenManager()

# Home screen
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Buttons to navigate to each CRUD screen
        layout.add_widget(Button(text="Quizzes CRUD", on_press=self.goto_quizzes))
        layout.add_widget(Button(text="Questions CRUD", on_press=self.goto_questions))
        layout.add_widget(Button(text="Attempts CRUD", on_press=self.goto_attempts))
        layout.add_widget(Button(text="Categories CRUD", on_press=self.goto_categories))
        layout.add_widget(Button(text="Levels CRUD", on_press=self.goto_levels))
        layout.add_widget(Button(text="Topics CRUD", on_press=self.goto_topics))
        
        self.add_widget(layout)

    def goto_quizzes(self, instance):
        screen_manager.current = 'quizzes'

    def goto_questions(self, instance):
        screen_manager.current = 'questions'

    def goto_attempts(self, instance):
        screen_manager.current = 'attempts'

    def goto_categories(self, instance):
        screen_manager.current = 'categories'

    def goto_levels(self, instance):
        screen_manager.current = 'levels'

    def goto_topics(self, instance):
        screen_manager.current = 'topics'

# Quizzes CRUD screen
# Quizzes CRUD screen
class QuizzesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        layout.add_widget(Label(text="Quizzes CRUD"))

        # Input fields for creating and updating quizzes
        self.title_input = TextInput(hint_text='Enter quiz title', multiline=False)
        self.description_input = TextInput(hint_text='Enter quiz description', multiline=False)
        layout.add_widget(Label(text="Title:"))
        layout.add_widget(self.title_input)
        layout.add_widget(Label(text="Description:"))
        layout.add_widget(self.description_input)

        layout.add_widget(Button(text="Create Quiz", on_press=self.create_quiz))
        layout.add_widget(Button(text="Update Quiz", on_press=self.update_quiz))
        layout.add_widget(Button(text="Get Quizzes", on_press=self.get_quizzes))
        layout.add_widget(Button(text="Delete Quiz", on_press=self.delete_quiz))
        layout.add_widget(Button(text="Back to Home", on_press=self.goto_home))
        
        self.add_widget(layout)

    def create_quiz(self, instance):
        title = self.title_input.text
        description = self.description_input.text
        
        # Sending data as JSON in the request body
        response = requests.post(
            f'{BASE_URL}/quizzes/',
            json={'title': title, 'description': description}
        )
        
        print(response.json())

    def get_quizzes(self, instance):
        response = requests.get(f'{BASE_URL}/quizzes/')
        print(response.json())

    def update_quiz(self, instance):
        quiz_id = 1  # Replace with actual quiz ID input or handling
        title = self.title_input.text
        description = self.description_input.text
        response = requests.put(f'{BASE_URL}/quizzes/{quiz_id}', json={'title': title, 'description': description})
        print(response.json())

    def delete_quiz(self, instance):
        quiz_id = 1  # Replace with actual quiz ID input or handling
        response = requests.delete(f'{BASE_URL}/quizzes/{quiz_id}')
        print(response.json())

    def goto_home(self, instance):
        screen_manager.current = 'home'

# Attempts CRUD screen
class AttemptsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Attempts CRUD"))

        # Input fields for creating and viewing attempts
        self.quiz_id_input = TextInput(hint_text='Enter quiz ID', multiline=False)
        self.user_id_input = TextInput(hint_text='Enter user ID', multiline=False)
        self.answers_input = TextInput(hint_text='Enter answers (comma separated)', multiline=False)
        
        layout.add_widget(Label(text="Quiz ID:"))
        layout.add_widget(self.quiz_id_input)
        layout.add_widget(Label(text="User ID:"))
        layout.add_widget(self.user_id_input)
        layout.add_widget(Label(text="Answers (comma separated):"))
        layout.add_widget(self.answers_input)

        layout.add_widget(Button(text="Record Attempt", on_press=self.create_attempt))
        layout.add_widget(Button(text="Get Attempt", on_press=self.get_attempt))
        layout.add_widget(Button(text="Back to Home", on_press=self.goto_home))
        
        self.add_widget(layout)

    def create_attempt(self, instance):
        quiz_id = int(self.quiz_id_input.text)
        user_id = int(self.user_id_input.text)
        answers = self.answers_input.text.split(',')
        
        response = requests.post(
            f'{BASE_URL}/attempts/',
            json={'quiz_id': quiz_id, 'user_id': user_id, 'answers': answers}
        )
        print(response.json())

    def get_attempt(self, instance):
        attempt_id = 1  # Replace with actual attempt ID input or handling
        response = requests.get(f'{BASE_URL}/attempts/{attempt_id}')
        print(response.json())

    def goto_home(self, instance):
        screen_manager.current = 'home'

# Categories CRUD screen
class CategoriesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Categories CRUD"))

        # Input fields for creating and updating categories
        self.category_name_input = TextInput(hint_text='Enter category name', multiline=False)
        self.description_input = TextInput(hint_text='Enter description', multiline=False)
        
        layout.add_widget(Label(text="Category Name:"))
        layout.add_widget(self.category_name_input)
        layout.add_widget(Label(text="Description:"))
        layout.add_widget(self.description_input)

        layout.add_widget(Button(text="Create Category", on_press=self.create_category))
        layout.add_widget(Button(text="Update Category", on_press=self.update_category))
        layout.add_widget(Button(text="Get Categories", on_press=self.get_categories))
        layout.add_widget(Button(text="Delete Category", on_press=self.delete_category))
        layout.add_widget(Button(text="Back to Home", on_press=self.goto_home))
        
        self.add_widget(layout)

    def create_category(self, instance):
        category_name = self.category_name_input.text
        description = self.description_input.text
        response = requests.post(
            f'{BASE_URL}/categories/',
            json={'name': category_name, 'description': description}
        )
        print(response.json())

    def get_categories(self, instance):
        response = requests.get(f'{BASE_URL}/categories/')
        print(response.json())

    def update_category(self, instance):
        category_id = 1  # Replace with actual category ID input or handling
        category_name = self.category_name_input.text
        description = self.description_input.text
        response = requests.put(
            f'{BASE_URL}/categories/{category_id}',
            json={'name': category_name, 'description': description}
        )
        print(response.json())

    def delete_category(self, instance):
        category_id = 1  # Replace with actual category ID input or handling
        response = requests.delete(f'{BASE_URL}/categories/{category_id}')
        print(response.json())

    def goto_home(self, instance):
        screen_manager.current = 'home'

# Levels CRUD screen
class LevelsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Levels CRUD"))

        # Input fields for creating and updating levels
        self.level_name_input = TextInput(hint_text='Enter level name', multiline=False)
        self.description_input = TextInput(hint_text='Enter description', multiline=False)
        
        layout.add_widget(Label(text="Level Name:"))
        layout.add_widget(self.level_name_input)
        layout.add_widget(Label(text="Description:"))
        layout.add_widget(self.description_input)

        layout.add_widget(Button(text="Create Level", on_press=self.create_level))
        layout.add_widget(Button(text="Update Level", on_press=self.update_level))
        layout.add_widget(Button(text="Get Levels", on_press=self.get_levels))
        layout.add_widget(Button(text="Delete Level", on_press=self.delete_level))
        layout.add_widget(Button(text="Back to Home", on_press=self.goto_home))
        
        self.add_widget(layout)

    def create_level(self, instance):
        level_name = self.level_name_input.text
        description = self.description_input.text
        response = requests.post(
            f'{BASE_URL}/levels/',
            json={'name': level_name, 'description': description}
        )
        print(response.json())

    def get_levels(self, instance):
        response = requests.get(f'{BASE_URL}/levels/')
        print(response.json())

    def update_level(self, instance):
        level_id = 1  # Replace with actual level ID input or handling
        level_name = self.level_name_input.text
        description = self.description_input.text
        response = requests.put(
            f'{BASE_URL}/levels/{level_id}',
            json={'name': level_name, 'description': description}
        )
        print(response.json())

    def delete_level(self, instance):
        level_id = 1  # Replace with actual level ID input or handling
        response = requests.delete(f'{BASE_URL}/levels/{level_id}')
        print(response.json())

    def goto_home(self, instance):
        screen_manager.current = 'home'

# Topics CRUD screen
class TopicsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Topics CRUD"))

        # Input fields for creating and updating topics
        self.topic_name_input = TextInput(hint_text='Enter topic name', multiline=False)
        self.description_input = TextInput(hint_text='Enter description', multiline=False)
        
        layout.add_widget(Label(text="Topic Name:"))
        layout.add_widget(self.topic_name_input)
        layout.add_widget(Label(text="Description:"))
        layout.add_widget(self.description_input)

        layout.add_widget(Button(text="Create Topic", on_press=self.create_topic))
        layout.add_widget(Button(text="Update Topic", on_press=self.update_topic))
        layout.add_widget(Button(text="Get Topics", on_press=self.get_topics))
        layout.add_widget(Button(text="Delete Topic", on_press=self.delete_topic))
        layout.add_widget(Button(text="Back to Home", on_press=self.goto_home))
        
        self.add_widget(layout)

    def create_topic(self, instance):
        topic_name = self.topic_name_input.text
        description = self.description_input.text
        response = requests.post(
            f'{BASE_URL}/topics/',
            json={'name': topic_name, 'description': description}
        )
        print(response.json())

    def get_topics(self, instance):
        response = requests.get(f'{BASE_URL}/topics/')
        print(response.json())

    def update_topic(self, instance):
        topic_id = 1  # Replace with actual topic ID input or handling
        topic_name = self.topic_name_input.text
        description = self.description_input.text
        response = requests.put(
            f'{BASE_URL}/topics/{topic_id}',
            json={'name': topic_name, 'description': description}
        )
        print(response.json())

    def delete_topic(self, instance):
        topic_id = 1  # Replace with actual topic ID input or handling
        response = requests.delete(f'{BASE_URL}/topics/{topic_id}')
        print(response.json())

    def goto_home(self, instance):
        screen_manager.current = 'home'

class QuestionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Questions CRUD"))

        # Input fields for creating and updating questions
        self.question_text_input = TextInput(hint_text='Enter question text', multiline=False)
        self.option_a_input = TextInput(hint_text='Enter option A', multiline=False)
        self.option_b_input = TextInput(hint_text='Enter option B', multiline=False)
        self.option_c_input = TextInput(hint_text='Enter option C', multiline=False)
        self.option_d_input = TextInput(hint_text='Enter option D', multiline=False)
        self.correct_answer_input = TextInput(hint_text='Enter correct answer (A/B/C/D)', multiline=False)

        layout.add_widget(Label(text="Question Text:"))
        layout.add_widget(self.question_text_input)
        layout.add_widget(Label(text="Option A:"))
        layout.add_widget(self.option_a_input)
        layout.add_widget(Label(text="Option B:"))
        layout.add_widget(self.option_b_input)
        layout.add_widget(Label(text="Option C:"))
        layout.add_widget(self.option_c_input)
        layout.add_widget(Label(text="Option D:"))
        layout.add_widget(self.option_d_input)
        layout.add_widget(Label(text="Correct Answer:"))
        layout.add_widget(self.correct_answer_input)

        layout.add_widget(Button(text="Create Question", on_press=self.create_question))
        layout.add_widget(Button(text="Update Question", on_press=self.update_question))
        layout.add_widget(Button(text="Get Questions", on_press=self.get_questions))
        layout.add_widget(Button(text="Delete Question", on_press=self.delete_question))
        layout.add_widget(Button(text="Back to Home", on_press=self.goto_home))
        
        self.add_widget(layout)

    def create_question(self, instance):
        question_text = self.question_text_input.text
        option_a = self.option_a_input.text
        option_b = self.option_b_input.text
        option_c = self.option_c_input.text
        option_d = self.option_d_input.text
        correct_answer = self.correct_answer_input.text
        
        response = requests.post(
            f'{BASE_URL}/questions/',
            json={
                'question_text': question_text,
                'option_a': option_a,
                'option_b': option_b,
                'option_c': option_c,
                'option_d': option_d,
                'correct_answer': correct_answer
            }
        )
        print(response.json())

    def get_questions(self, instance):
        response = requests.get(f'{BASE_URL}/questions/')
        print(response.json())

    def update_question(self, instance):
        question_id = 1  # Replace with actual question ID input or handling
        question_text = self.question_text_input.text
        option_a = self.option_a_input.text
        option_b = self.option_b_input.text
        option_c = self.option_c_input.text
        option_d = self.option_d_input.text
        correct_answer = self.correct_answer_input.text
        
        response = requests.put(
            f'{BASE_URL}/questions/{question_id}',
            json={
                'question_text': question_text,
                'option_a': option_a,
                'option_b': option_b,
                'option_c': option_c,
                'option_d': option_d,
                'correct_answer': correct_answer
            }
        )
        print(response.json())

    def delete_question(self, instance):
        question_id = 1  # Replace with actual question ID input or handling
        response = requests.delete(f'{BASE_URL}/questions/{question_id}')
        print(response.json())

    def goto_home(self, instance):
        screen_manager.current = 'home'


# Main app class
class QuizApp(App):
    def build(self):
        screen_manager.add_widget(HomeScreen(name='home'))
        screen_manager.add_widget(QuizzesScreen(name='quizzes'))
        screen_manager.add_widget(QuestionsScreen(name='questions'))
        screen_manager.add_widget(AttemptsScreen(name='attempts'))
        screen_manager.add_widget(CategoriesScreen(name='categories'))
        screen_manager.add_widget(LevelsScreen(name='levels'))
        screen_manager.add_widget(TopicsScreen(name='topics'))
        return screen_manager

if __name__ == '__main__':
    QuizApp().run()
