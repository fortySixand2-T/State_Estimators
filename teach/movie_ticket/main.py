import theater
import movie
import random
import user

theater_names = {
                    "Cineplex Cinemas Yonge": "10 Dundas St E #402, Toronto, ON M5B 2G9, Canada",
                    "Imagine Cinemas":"80 Front St E, Toronto, ON M5E 1T4, Canada",
                    "Cinesphere Theatre":"955 Lake Shore Blvd W, Toronto, ON M6K 3B9, Canada"}
movie_names = {
                "John Wick: Chapter 4":"2h 49m",
                "Shazam! Fury of the Gods":"2h 10m",
                "Fast X":"2h 1m",
                "Scream VI":"2h 10m"}

seats = {
    "1": ["A3", "A4", "G5", "K6", "H26"],
    "2": ["B3", "A6", "F4", "C3"],
    "3": ["A12", "B4", "F6", "D16"],
    "4": ["B1", "B2", "B3","B4", "F6", "D18"],
    "5": ["F1", "F2", "F3","E4", "E6", "E8","D17"],
    "6": ["A16", "F5", "H14", "C8", "S4", "F7", "F12"],
    "7": ["C16", "G5", "F14", "B8", "S14", "E16", "E12"],
    "8": ["C6", "G15", "H14", "C8", "S24", "A17", "G12"],
    "9": ["F6", "E5", "E14", "C8", "G4", "G7", "G22"],
    "10": ["F16", "E5", "F14", "E8", "S14", "S7", "G2"],
}
timings = {
    "John Wick: Chapter 4_1": {"14":["08:30","10:40","18:05","23:30"]},
    "John Wick: Chapter 4_2": {"16":["09:10","10:25","15:05","20:30"]},
    "John Wick: Chapter 4_3": {"18":["12:30","10:40","18:05","23:30"]},
    "Shazam! Fury of the Gods_1": {"15":["09:30","14:05","20:30"]},
    "Shazam! Fury of the Gods_2": {"14":["07:30","11:40","18:45","23:30"]},
    "Shazam! Fury of the Gods_3": {"19":["09:05","11:45","17:05","19:30"]},
    "Fast X_1": {"18":["07:40","10:15","18:50","21:30"]},
    "Fast X_2": {"16":["08:45","12:05","14:35","18:20","20:40","22:55"]},
    "Fast X_3": {"12":["08:35","10:45","14:55","18:05","23:30"]},
    "Scream VI_1": {"12":["15:30","17:20","19:45","21:30","23:30"]},
    "Scream VI_2": {"11":["14:45","16:40","19:05","21:05","23:30"]},
    "Scream VI_3": {"13":["13:30","15:40","20:05","22:00","23:30"]},
}

user_list = {
                "adavies1":"hash11",
                "badams":"almonds",
                "brodgers":"leicester",
                "cancellotti":"rmadrid",
                "ethagg":"united",
                "gpotter":"chelsea",
                "hamla":"average",
                "jdoe":"password",
                "jdoe2":"password123",
                "jharris":"qwerty123",
                "jklopp":"liverpool",
                "jkohls":"randomize23",
                "jroot":"consistent",
                "lfars":"laptop",
                "lvuit":"12qwerty90",
                "marteta":"arsenal",
                "pgaurdiola":"mancity",
                "rlewis":"youngster",
                "mkeyenes":"cairns",
                "stendulkar":"cricketgoat",
                "vkohli":"centuries"
}

def getTimingList(movie,theater):
    theaterName = theater.getTheaterName()
    movieName = movie.getMovieName()
    if theaterName == "Cineplex Cinemas Yonge":
        movieName = movieName + "_1"
    elif theaterName == "Imagine Cinemas":
        movieName = movieName + "_2"
    else :
        movieName = movieName + "_3"
    
    timingCostDict = timings[movieName]
    cost = list(timingCostDict.keys())[0]
    # print(cost)
    timingList = timingCostDict[cost]
    movie.setPrice(int(cost))

    for timing in timingList:
        random_num = random.randint(1,10)
        movie.addSeatAndTiming(timing,seats[str(random_num)])

def setupMovies(theater):
    movielist = []
    for key,value in movie_names.items():
        tmp_movie = movie.Movie(key,value)
        getTimingList(tmp_movie,theater)
        theater.addMovie(tmp_movie)

def setupTheater():
    theatersList = []
    for key,value in theater_names.items():
        temp_theater = theater.Theater(key,value)
        setupMovies(temp_theater)
        # print(temp_theater.getMoviesAvailable()[0].getSeatAndTiming())
        theatersList.append(temp_theater)
    return theatersList

def setupUsers():
    userslist = []
    for key,value in user_list.items():
        tmp_user = user.User(key,value)
        userslist.append(tmp_user)
    return userslist

def checkUsernameExist(users, username):
    for us in users:
        if us.CheckUserName(username):
            return True

    return False

def checkUserIdPasswordCombo(users, username, password):
    for us in users:
        if us.CheckUserPwdCombo(username,password):
            return True
    return False

def checkMovieExists(movie_name):
    if movie_name in movie_names.keys():
        return True
    return False

def checkTheaterExists(theater_name):
    if theater_name in theater_names.keys():
        return True
    return False

def getShowTimingsAndSeatAvailability(theater_list,theater_name,movie_name):
    for th in theater_list:
        if th.getTheaterName() == theater_name:
            for mo in th.getMoviesAvailable():
                if mo.getMovieName() == movie_name:
                    timin = mo.getSeatAndTiming()
    
    return timin

def getTicketCost(theater_list,theater_name,movie_name):
    for th in theater_list:
        if th.getTheaterName() == theater_name:
            for mo in th.getMoviesAvailable():
                if mo.getMovieName() == movie_name:
                    price = mo.getPricePerTicket()
    
    return price

def checkChosentimingExists(timing, timing_list):
    if timing in timing_list:
        return True
    return False

def checkSeatsChosenExists(seat_list,total_seats):
    for s in seat_list:
        if s not in total_seats:
            return False
    return True

if __name__ == "__main__":
    theatres = setupTheater()
   
    users = setupUsers()
    while True:
        username = input("Enter User Id: ")#---------------------------------------------
        if(not checkUsernameExist(users,username)):
            bo = input("Error UserId doesn't exist. Would you like to create a new id? Y or N : ")
            if bo == 'Y' or bo =='y':
                new_user_id = input("Enter user_id: ")
                new_password = input("Enter user password: ")
                new_user = user.User(new_user_id,new_password)
                users.append(new_user)
                continue#------------------------------------------------------------------------
            elif bo == 'N' or bo =='n':
                print("Lets try re-Entering User ID :")
                continue
            else:
                exit_sig = ("Error Unexpected Input. Do You want to exit the console? Y or N : ")
                if exit_sig == 'Y' or exit_sig == 'y':
                    break
                elif exit_sig == 'N' or exit_sig == 'n':
                    print("Let Retry from the beggining!")
                    continue
                else:
                    print("Unexpected Input. Exiting Console")
                    break
        
        password = input("Enter User Password : ")
        if(not checkUserIdPasswordCombo(users,username,password)):
            exit_s = input("Error: Password-ID mismatch. Would you like to retry? Y or N")
            if exit_s == 'Y' or exit_s =="y":
                continue
            else:
                print("Exiting the console")
                break
        
        current_user = user.User(username,password)
##------------------- User movie, theater, total cost-----------------------------------#
        print("\n ********************************************************************************* \n")
        print(" Choose a Movie from the list: \n")
        for movie_key,movie_dur in movie_names.items():
            print(f"->{movie_key} : {movie_dur}\n")
        movie_n = input("Choose a movie from the above list: ")
        if checkMovieExists(movie_n):
            print(f"\nYour chosen movie is {movie_n} is available at the following theatres: \n")
            for theatr,th_address in theater_names.items():
                print(f"->{theatr}  : {th_address}\n")
            theater_n = input("Choose your favorite theater location listed above: ")
            if checkTheaterExists(theater_n):
                print( f"\nAvailable Showtimings of {movie_n} at {theater_n} are : \n")
                timingsList = getShowTimingsAndSeatAvailability(theatres,theater_n,movie_n)
                cost_perTicket = getTicketCost(theatres,theater_n,movie_n)
                # print(f"Available Timings : {timingsList}")
                for key,value in timingsList.items():
                    print(f"->{key} ----  {value}\n")
                timingChose = input( "\nChoose a timing from the above list : ")
                if checkChosentimingExists(timingChose,list(timingsList.keys())):
                    numberOfTickets = int(input("\nHow many tickets would you be choosing? : "))
                    if numberOfTickets < len(timingsList):
                        seatsChosen = []
                        print("\nSelect your Tickest from the list : ")
                        for i in range(numberOfTickets):
                            seatsChosen.append(str(input()))
                        if checkSeatsChosenExists(seatsChosen,list(timingsList[timingChose])):
                            current_user.setTheatreName(theater_n)
                            current_user.setMovieName(movie_n)
                            current_user.setChosenSeats(seatsChosen)
                            current_user.setTotalTickets(numberOfTickets)
                            current_user.setTotalCost(cost_perTicket)

                            print("-----------------------------------------------------------------------------------------------------\n\n")
                            print(f"\n Seats chosen by the user {current_user.getUserName()} is/are {seatsChosen}")
                            print(f"\n Total cost of {numberOfTickets} ticket/s is/are {current_user.getTotalCost()}$\n")
                            e = input( "Would you like to proceed with your booking? Y or N: ")
                            if e == "Y" or e == "y":
                                print("\n\n-----------------------------------------------------------------------------------------------------\n\n")
                                print("Your tickets have been booked successfuly. Thank you very much for using our service.\n")
                                print(f"Your total cost is {current_user.getTotalCost()}$\n")
                                print("\n\n-----------------------------------------------------------------------------------------------------\n\n")
                                exitFinal = input(" Would you like to exit the ticket booking console? Y or N: ")
                                if exitFinal == "Y" or exitFinal == 'y':
                                    print("\n\n Thank You! \n\n")
                                    break
                                elif exitFinal == "N" or exitFinal =="n":                                
                                    continue
                                else:
                                    break
                            elif e == "N" or e == "n":
                                current_user.ResetUserBookingDetails()
                                print("\nThank you for using our service. Comeback when you are ready to book your tickets.\n")
                                break
                        else:
                            print("The seats you have chosen seem to have already been booked. Please try again.\n")
                            continue
                    else:
                        print("The number of tickets required by the user exceeds the maximum tickets available for the show.")
                        e = input("Would you like to try again? Y or N")
                        if e =="Y" or e=='y':
                            print("Thank you for your patience.\n")
                            continue
                        else:
                            break
                else:
                    print("\nThe selected show timing is either invalid or unavailable. Please Try again.\n")
                    continue
            else:
                print("You seem to have chosen the theater incorrectly.")
                e = input("Would you like to retry? Y or N: ")
                if e == "Y" or e =="y":
                    continue
                else:
                    break
        else:
            print("The movie name is either not available or invalid.")
            e = input("Would you like to retry? Y or N: ")
            if e == "Y" or e =="y":
                continue
            else:
                break

    # movie1.addSeatAndTiming("1:30",seats["002"])
    # print(movie1.getSeatAndTiming()["1:30"])
    # # theaters -> 3;
    # movies -> 4;
    # timing:seat -> 12xtimings atleast

#     fine available seats
# seats = {
#     "001": {"A3", "A4", "G5", "K6", "H26"},
#     "002": {"B3", "A6", "F4", "C3"},
#     "003": {"A12", "B4", "F6", "D16"},
#     "004": {"C16", "D5", "H14", "C8", "S4", "A7", "G12"},


# theater-> allmoviesAssign -> seatAndTiming assign