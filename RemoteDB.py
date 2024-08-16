import sqlite3 as sl

# Commit and close db
def commitDBUpdate(con):
    con.commit()
    con.close()

# Nake database
def makeTable():
    con = sl.connect('Remotes.db')
    with con:
        con.execute("""
            CREATE TABLE Remotes (
                remoteName TEXT,
                keyName TEXT,
                protocol TEXT,
                keyCode TEXT,
                remoteAndKeyName TEXT PRIMARY KEY
            );
        """)
    commitDBUpdate(con)
    
# Add list of button codes to db 
def addButtons(data):
    con = sl.connect('Remotes.db')
    sql = 'INSERT INTO Remotes (remoteName, keyName, protocol, keyCode, remoteAndKeyName) values(?, ?, ?, ?, ?) ON CONFLICT(remoteAndKeyName) DO UPDATE SET keyCode=excluded.keyCode'
    with con:
        con.executemany(sql, data)
    commitDBUpdate(con)
    print("Added new buttons to database")

# Get code and protocol for a specified button
def getKeyCode(remoteName, keyName):
    con = sl.connect('Remotes.db')
    with con:
        data = con.execute("SELECT * FROM Remotes WHERE remoteName= '" + remoteName + "' AND keyName='" + keyName + "'")
        for row in data:
            #print(row)
            return row
    con.close()

# Get list of remote names in db
def getRemoteNames():
    con = sl.connect('Remotes.db')
    remoteNames = []
    with con:
        data = con.execute("SELECT remoteName FROM Remotes GROUP BY remoteName ORDER BY remoteName")
        for row in data:
            remoteNames.append(row[0])
    con.close()
    return remoteNames

# Get list of configued buttons for a remote
def showConfiguredButtons(remoteName):
    con = sl.connect('Remotes.db')
    buttons = []
    with con:
        data = con.execute("SELECT * FROM Remotes WHERE remoteName= '" + remoteName + "'")
        for row in data:
            buttons.append(row)
    con.close()
    return buttons

# Make table for active remote
def makeActiveRemoteTable():
    con = sl.connect('Remotes.db')
    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS ActiveRemote (
                fieldName TEXT PRIMARY KEY,
                remoteName TEXT
            );
        """)
    commitDBUpdate(con)

# Set active remote in DB
def setActiveRemote(remoteName):
    makeActiveRemoteTable()
    updateDB("INSERT INTO ActiveRemote (fieldName, remoteName) VALUES ('activeRem','" + remoteName + "') ON CONFLICT (fieldName) DO UPDATE SET remoteName=excluded.remoteName")

# Get the active remote
def getActiveRemote():
    con = sl.connect('Remotes.db')
    activeRem = None
    with con:
        data = con.execute("SELECT remoteName FROM ActiveRemote WHERE fieldName= 'activeRem'")
        if(data.arraysize == 0):
            print("ERROR: Active remote not set")
            con.close()
            return None
        for row in data:
            activeRem = row[0]
            break
    #
    con.close()
    return activeRem

# Updates db with specified command
def updateDB(sqlCommand):
    con = sl.connect('Remotes.db')
    con.execute(sqlCommand)
    commitDBUpdate(con)    
    print("Database updated")

# Print database
def showDB():
    con = sl.connect('Remotes.db')
    with con:
        data = con.execute("SELECT * FROM Remotes")
        for row in data:
            print(row)
    con.close()