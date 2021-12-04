import mysql.connector

class mysqlConnection:
  def __init__(self):
    self.mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      autocommit=True,
      buffered=True
    )
    self.myCursor = self.mydb.cursor(dictionary=True)

  def getDatabasesList(self):
    self.myCursor.execute("SHOW DATABASES")
    output = self.myCursor.fetchall()
    output = [i[0] for i in output]
    return output

  def selectDatabase(self, databaseName):
    self.myCursor.execute("USE "+ databaseName)

  def createDatabases(self, databaseName):
    self.myCursor.execute("CREATE DATABASE IF NOT EXISTS "+ databaseName)

  def dropDatabases(self, databaseName):
    self.myCursor.execute("DROP DATABASE IF EXISTS "+ databaseName)

  def createNewContact(self, contactName, contactSurname = "NULL", contactMail= "NULL", contactNumber= "NULL", picture= "NULL"):
    self.myCursor.execute("INSERT INTO contacts (firstname, surname, email, number, picture) VALUES ("+ contactName + ", " + contactSurname + ", " + contactMail + ", " + contactNumber + ", " + picture + ");")

  def updateContact(self, contactId, contactName, contactSurname = "NULL", contactMail= "NULL", contactNumber= "NULL", picture= "NULL"):
    self.myCursor.execute("UPDATE contacts SET firstname = "+ contactName + ", surname = " + contactSurname + ", email = " + contactMail + ", number= " + contactNumber +", picture= " + picture +" WHERE id = " + str(contactId) + ";")

  def deleteContact(self, contactId):
    self.myCursor.execute("DELETE FROM contacts WHERE id=" + str(contactId) + ";")

  def getContactsList(self):
    self.myCursor.execute("SELECT id, firstname FROM contacts")
    output = self.myCursor.fetchall()
    contactDict = dict()
    for listElement in output:
      contactDict[listElement["firstname"]] = listElement["id"]
    return contactDict

  def getSearchContactList(self, criteria):
    self.myCursor.execute("SELECT id, firstname FROM contacts WHERE (firstname LIKE '" + criteria + "%') ;")
    output = self.myCursor.fetchall()
    contactDict = dict()
    for listElement in output:
      contactDict[listElement["firstname"]] = listElement["id"]
    return contactDict

  def getContact(self, contactId):
    self.myCursor.execute("SELECT * FROM contacts WHERE id=" + str(contactId) + ";")
    output = self.myCursor.fetchall()
    contactInfo = {
      "firstname": output[0]["firstname"],
      "surname": output[0]["surname"],
      "email": output[0]["email"],
      "number":  output[0]["number"],
      "picture": output[0]["picture"]
    }
    return contactInfo

