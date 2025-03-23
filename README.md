# UserSpecificChatbot

in the first terminal (to create a virtual env -> 
                          to activate the virtual env -> 
                              to install the required dependencies -> 
                                  to train the rasa model ->
                                      and finally to start the rasa server):->
    py -3.10 -m venv myenv : create a virtual env
    myenv\Scripts\activate : activate the virtual env
    python --version
    pip install rasa rasa-sdk requests : dependencies
    rasa train : training
    rasa run actions : start server

in the second terminal(to run the chatbot)
    myenv\Scripts\activate : activate the virtual env
    rasa shell : start the chatbot
