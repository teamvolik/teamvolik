"""A module that contains a dictionary of bot responses."""

reply_list = dict()

reply_list["help"] = "#TODO"
reply_list["start"] = "Welcome to teamvolik bot. First you need to sign up."
reply_list["ask_perm"] = "Do you consent to the storage and processing of personal data (Name and Surname)? This is to facilitate registration for games."
reply_list["yes_permission"] = "Thanks! We promise to keep your personal data and not distribute it."
reply_list["no_permission"] = "Thanks! We respect your personal data and will not store it, but you will have to write your full name each time you register for the game."
reply_list["ask_name"] = "Enter full name:"
reply_list["signup_success"] = "You have successfully signed up."
reply_list["cancel"] = "Cancel."
reply_list["no_access"] = "You do not have permission to execute this command."

reply_list["adm_ask_date"] = "On what date do you want to open the registration for the game? (DD.MM.YYYY)"
reply_list["adm_ask_place"] = "Where do you want to play the game?"
reply_list["adm_ask_players_num"] = "Specify the number of players:"
reply_list["adm_ask_description"] = "Add a description to the game (Leave the field blank if you don't want to add a description):"
reply_list["adm_ask_to_check"] = "Is everything right?"
reply_list["adm_game_created"] = "The game has been successfully created!"
reply_list["adm_game_canceled"] = "The game has been cancelled."

reply_list["adm_date_error"] = "Incorrect date format. Enter the date again. (DD.MM.YYYY)"
reply_list["adm_players_num_error"] = "Incorrect number of players, please enter the number of players again:"

reply_list["reg_ask_game"] = "Choose one game from the list:"
reply_list["reg_success"] = "You have successfully registered for the game."
reply_list["reg_err_full"] = "Unfortunately, there are no more places left for this game. Try signing up for another one."
reply_list["reg_ask_reserve"] = "Unfortunately, there are no more places left for this game. Do you want to reserve?"
reply_list["reg_canceled"] = "Game selection successfully deselected."
reply_list["reg_from_reserve_to_active"] = "You were moved from the reserve to the list of active players in one of the games."

reply_list["games_get_players"] = "Select a game to see who signed up for it."
reply_list["games_player_list"] = "List of players for this game:"

reply_list["no_games_yet"] = "There are currently no games available to sign up for."
reply_list["no_players_yet"] = "No one is registered for this game."

reply_list["choose_game_to_leave"] = "Select the game you want to leave."
reply_list["left_game"] = "The game has been successfully abandoned."

reply_list["error_not_registered"] = "Sorry, but you need to register. Click on the button."
reply_list["error_already_exists"] = "Sorry, but you are already registered."
reply_list["error_wrong_name_format"] = "Full name entered incorrectly, make sure that the entered data is correct (two words are required)."
reply_list["error_wrong_data_format"] = "The date is entered incorrectly, make sure that the entered data is correct (DD.MM.YYYY)."
reply_list["error_wrong_players_num_format"] = "Incorrect number of players entered, check that the entered data is correct (requires a positive number)."
reply_list["error_wrong_game_chosen"] = "Please select the game again."
reply_list["error_sayitagain"] = "Please select one of the buttons."
