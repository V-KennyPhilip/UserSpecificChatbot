# UserSpecificChatbot

in the first terminal (to create a virtual env -> 
                          to activate the virtual env -> 
                              to install the required dependencies -> 
                                  to train the rasa model ->
                                      and finally to start the rasa server):->
    1. py -3.10 -m venv myenv : create a virtual env
    2. myenv\Scripts\activate : activate the virtual env
    3. python --version
    4. pip install rasa rasa-sdk requests : dependencies
    5. rasa train : training
    6. rasa run actions : start server

in the second terminal(to run the chatbot)
    1. myenv\Scripts\activate : activate the virtual env
    2. rasa shell : start the chatbot
