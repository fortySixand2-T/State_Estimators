import movie

class Theater:
    def __init__(self, theaterName, location):
        self.theaterName = theaterName
        self.location = location
        self.moviesAvailable = []
    
    def addMovieList(self,movieList):
        self.moviesAvailable = movieList

    def addMovie(self,movie):
        flag = self.checkIfMovieIsAvailable(movie.getMovieName())
        if flag is False:
            self.moviesAvailable.append(movie)

    def checkIfMovieIsAvailable(self,movieName):
        for movie in self.moviesAvailable:
            if( movieName == movie.getMovieName()):
                return True
            else:
                return False
        return False

    def getMoviesAvailable(self):
        return self.moviesAvailable
    
    def getTheaterName(self):
        return self.theaterName

    def getLocation(self):
        return self.location