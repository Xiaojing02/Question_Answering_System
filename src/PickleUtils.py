import pickle


def storeData(db, filename):
    dbfile = open(filename, 'wb')

    pickle.dump(db, dbfile, protocol=2)
    dbfile.close()


def loadData(filename):
    dbfile = open(filename, 'rb')
    db = pickle.load(dbfile)
    dbfile.close()
    return db

