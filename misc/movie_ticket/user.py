class User:
    def __init__(self, user_name, user_password):
        self.user_name = user_name
        self.user_pwd = user_password
        self.tickets = 0
        self.total_cost = 0

    def setTotalCost(self, cost):
        self.total_cost = cost*self.tickets

#theater ->
    def setChosenSeats(self,seats_list):
        self.seats = seats_list
    
    def setMovieName(self, movie_name):
        self.movie_name = movie_name

    def setTheatreName(self, theatre_name):
        self.theatre_name = theatre_name

    def setTotalTickets(self, ticketCount):
        self.tickets = ticketCount

    def getUserName(self):
        return self.user_name
    
    def getUserPwd(self):
        return self.user_pwd

    def getTotalCost(self):
        return self.total_cost

    def CheckUserName(self, username):
        if username == self.getUserName():
            return True

        return False
    
    def CheckUserPwd(self, password):
        if password == self.getUserPwd():
            return True
        
        return False
    
    def CheckUserPwdCombo(self, username, password):
        if self.CheckUserName(username) and self.CheckUserPwd(password):
            return True
        
        return False
    
    def ResetUserBookingDetails(self):
        self.tickets = 0
        self.theatre_name = ""
        self.movie_name = ""
        self.total_cost = 0
        self.seats = []

#user raman-> user_id, user_password,tickets,total_cost,theater[enna padam, enna seat,enna time]