from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instance
chatbot = None
#     ChatBot(
#     'Bot',
#     storage_adapter='chatterbot.storage.SQLStorageAdapter',
#     logic_adapters=[
#         'chatterbot.logic.MathematicalEvaluation',
#         'chatterbot.logic.TimeLogicAdapter',
#         'chatterbot.logic.BestMatch',
#         {
#             'import_path': 'chatterbot.logic.BestMatch',
#             'default_response': 'I am sorry, but I do not understand. I am still learning.',
#             'maximum_similarity_threshold': 0.90
#         }
#     ],
#     database_uri='sqlite:///database.sqlite3'
# ) 

#  # Training with Personal Ques & Ans 
# training_data_quesans = open('training_data/personal_ques_ans.txt').read().splitlines()
# #training_data_personal = open('training_data/personal_ques.txt').read().splitlines()

# training_data = training_data_quesans #+ training_data_personal

# trainer = ListTrainer(chatbot)
# trainer.train(training_data)  