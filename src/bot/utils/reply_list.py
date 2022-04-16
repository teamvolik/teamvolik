"""A module that contains a dictionary of bot responses."""
from src.bot.utils.localization import _

reply_list = dict()

reply_list["help"] = _("#TODO")
reply_list["start"] = _("Welcome to teamvolik bot. First you need to sign up.")
reply_list["ask_perm"] = _("Do you consent to the storage and processing of personal data (Name and Surname)? This is to facilitate registration for games.")
reply_list["yes_permission"] = _("Thanks! We promise to keep your personal data and not distribute it.")
reply_list["no_permission"] = _("Thanks! We respect your personal data and will not store it, but you will have to write your full name each time you register for the game.")
reply_list["ask_name"] = _("Enter full name:")
reply_list["signup_success"] = _("You have successfully signed up.")
reply_list["cancel"] = _("Cancel.")
reply_list["no_access"] = _("You do not have permission to execute this command.")

reply_list["adm_ask_date"] = _("On what date do you want to open the registration for the game? (DD.MM.YYYY HH:MM)")
reply_list["adm_ask_place"] = _("Where do you want to play the game?")
reply_list["adm_ask_players_num"] = _("Specify the number of players:")
reply_list["adm_ask_description"] = _("Add a description to the game (Leave the field blank if you don't want to add a description):")
reply_list["adm_ask_to_check"] = _("Is everything right?")
reply_list["adm_game_created"] = _("The game has been successfully created!")
reply_list["adm_game_canceled"] = _("The game has been cancelled.")

reply_list["adm_date_error"] = _("Incorrect date format. Enter the date again. (DD.MM.YYYY HH:MM)")
reply_list["adm_players_num_error"] = _("Incorrect number of players, please enter the number of players again:")

reply_list["reg_ask_game"] = _("Choose one game from the list:")
reply_list["reg_success"] = _("You have successfully registered for the game.")
reply_list["reg_err_full"] = _("Unfortunately, there are no more places left for this game. Try signing up for another one.")
reply_list["reg_ask_reserve"] = _("Unfortunately, there are no more places left for this game. Do you want to reserve?")
reply_list["reg_canceled"] = _("Game selection successfully deselected.")
reply_list["reg_from_reserve_to_active"] = _("You were moved from the reserve to the list of active players in one of the games.")

reply_list["games_get_players"] = _("Select a game to see who signed up for it.")
reply_list["games_player_list"] = _("List of players for this game:")
reply_list["games_reserve_list"] = _("List of players from reserve:")

reply_list["no_games_yet"] = _("There are currently no games available to sign up for.")
reply_list["no_players_yet"] = _("No one is registered for this game.")

reply_list["choose_game_to_leave"] = _("Select the game you want to leave.")
reply_list["left_game"] = _("The game has been successfully abandoned.")

reply_list["error_not_registered"] = _("Sorry, but you need to register. Click on the button.")
reply_list["error_already_exists"] = _("Sorry, but you are already registered.")
reply_list["error_wrong_name_format"] = _("Full name entered incorrectly, make sure that the entered data is correct (two words are required).")
reply_list["error_wrong_data_format"] = _("The date is entered incorrectly, make sure that the entered data is correct (DD.MM.YYYY HH:MM).")
reply_list["error_wrong_players_num_format"] = _("Incorrect number of players entered, check that the entered data is correct (requires a positive number).")
reply_list["error_wrong_game_chosen"] = _("Please select the game again.")
reply_list["error_sayitagain"] = _("Please select one of the buttons.")
