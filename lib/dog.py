import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    all = []
    
    # instantiate the object
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed
        
    # create table if it doesn't exist
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        # execute the query
        CURSOR.execute(sql)
        
    # drop table if it exists
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        
        CURSOR.execute(sql)
        
    # save dog instance to the database
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        
        CURSOR.execute(sql, (self.name, self.breed))
        
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        
    # create a new row in the database
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    # create dog instance from database row
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    # return list of all instances
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * 
            FROM dogs
        """
        
        all = CURSOR.execute(sql)
        
        # iterate over the returned list and create instances
        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    
    # find by name
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * 
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        
        dog = CURSOR.execute(sql, (name,)).fetchone()
        
        # return a dog instance
        return cls.new_from_db(dog)
    
    # find by id
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * 
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        
        my_dog = CURSOR.execute(sql, (id,)).fetchone()
        
        # return a dog instance
        return cls.new_from_db(my_dog)
    
    # find or create
    @classmethod
    def find_or_create_by(cls, name, breed):
        
        # statement to fetch the dog with values passed
        sql = """
            SELECT * FROM dogs WHERE name = ? AND breed = ?
        """
        
        # Check if the dog already exists in the database
        existing_dog = CURSOR.execute(sql, (name, breed)).fetchone()
        
        if existing_dog:
            # If the dog exists, return the existing record
            return cls.find_by_name(name)
        else:
            # If the dog doesn't exist, insert a new record
            return cls.create(name, breed)
        
    # update a dog's name
    def update(self):
        
        # statement to update the name of a dog
        sql = """
            UPDATE dogs SET name = ? WHERE id = ?
        """
        
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()
        
        