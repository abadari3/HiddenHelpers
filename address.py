import requests

class Address:
    def __init__(self, search = None, num = None, street = None, city = None, state = None):
        if not(search or num or street or city or state):
            print('Blank Searches are not allowed.')
            return
        self.num = num
        self.search = search
        self.street = street
        self.city = city
        self.state = state
        self.pos = None

        if (self.search):
            self.search = search.replace(' ', "%20")
        if (self.street):
            self.street = street.replace(' ', "%20")
        if (self.city):
            self.city = city.replace(' ', "%20")
        if (self.state):
            self.state = state.replace(' ', "%20")
    
    def structuredGeocode(self):
        link = 'https://api.tomtom.com/search/2/structuredGeocode.json?countryCode=USA'
        if (self.num):
            link += '&streetNumber=' + str(self.num)
        if (self.street):
            link += '&streetName=' + self.street
        if (self.city):
            link += '&municipality=' + self.city
        if (self.state):
            link += '&countrySubdivision=' + self.state
        link += '&key=WcfmLFVeYLwGWQDY08feLtdQps4g6E2N'
        location = requests.get(link)
        self.locationj = location.json()
    
    def fuzzySearch(self):
        link = 'https://api.tomtom.com/search/2/search/'
        link += self.search + '.json?countrySet=USA'
        # link += '&topLeft=28.221%2C-82.656&btmRight=27.890%2C-82.240'
        link += '&key=WcfmLFVeYLwGWQDY08feLtdQps4g6E2N'
        location = requests.get(link)
        self.locationj = location.json()
    
    def populate(self, i):
        if self.search != None:
            self.fuzzySearch()
        else:
            self.structuredGeocode()
        result = self.locationj['results']
        finalloc = result[i]
        try:
            self.num = finalloc['address']['streetNumber']
            self.street = finalloc['address']['streetName']
            self.city = finalloc['address']['municipality']
            self.state = finalloc['address']['countrySubdivisionName']
            self.addr = finalloc['address']['freeformAddress']
            lat = finalloc['position']['lat']
            lon = finalloc['position']['lon']
            self.pos = (lat, lon)
        except:
            print('Non-Address Found')
            lat = finalloc['position']['lat']
            lon = finalloc['position']['lon']
            self.addr = finalloc['address']['freeformAddress']
            self.pos = (lat, lon)

    def getNumber(self):
        return self.num
    def getStreet(self):
        return self.street
    def getCity(self):
        return self.city
    def getState(self):
        return self.state
    def getAddress(self):
        return self.addr
    def getPos(self):
        return self.pos
    def __str__(self):
        if (not self.pos):
            return "populate address first!"
        else:
            return self.getAddress()

x = Address('White House')
x.populate(0)
print(x)