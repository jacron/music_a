# from django.db import models


# Create your models here.
class Album(object):
    def __init__(self, ID, InstrumentID, Title, Path, AlbumID, IsCollection,
                 Created, Description):
        self.ID = ID
        self.InstrumentID = InstrumentID
        self.Title = Title
        self.Path = Path
        self.AlbumID = AlbumID
        self.IsCollection = IsCollection
        self.Created = Created
        self.Description = Description

    def output(self):
        print(self.ID, self.Title)


if __name__ == '__main__':
    a = Album(123, 1, 'Pianoconcert no. 5')
    a.output()

