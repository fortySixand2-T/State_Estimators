# from typing import Self

class Movie:
    def __init__(self, movieName, duration):
        self.movieName = movieName
        self.duration = duration
        self.price = 10
        self.seatAndTiming = {}

    def addSeatAndTiming(self,timing,seats):
        if timing not in self.seatAndTiming:
            self.seatAndTiming[timing] = seats
    
    def setPrice(self, cost):
        self.price = cost

    def getMovieName(self):
        return self.movieName
    
    def getSeatAndTiming(self):
        return self.seatAndTiming

    def getDuration(self):
        return self.duration
    
    def getAvailableTimings(self):
        return list(self.seatAndTiming.keys())
    
    def getAvailableSeats(self):
        return list(self.seatAndTiming.values())
    
    def getPricePerTicket(self):
        return self.price