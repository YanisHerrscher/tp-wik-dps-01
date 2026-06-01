import sqlite3 as sq
import pandas as pd
import os

prix_info = {13 : 60, 14: 70, 15: 80, 16: 90, 17: 100, 18: 120, 19: 140, 20: 160}

class Sql:
    def __init__(self, path = './Serveur/data'):
        self.__path = path
        self.__name = "pneus.dbs"
        self.__create_folder()
        self.__interact("""create table if not exists property (id text primary key NOT NULL, largeur integer NOT NULL, hauteur integer NOT NULL, diametre integer NOT NULL, charge integer, vitesse VARCHAR(1) NOT NULL)""")
        self.__interact("""create table if not exists stock (id text primary key NOT NULL, prix integer NOT NULL, quantite integer NOT NULL)""")

    def add_data(self, id, quantite):
        Width = int(id[:3])
        Height = int(id[3:6])
        Diameter = int(id[6:8])
        Charge = id[8:9]
        Speed = int(id[9:12])
        if Diameter > 20 or Diameter < 13:
            return False
        elif self.Check_Argument(id=id) == None:
            self.__interact("""INSERT INTO property (id, largeur, hauteur, diametre, charge, vitesse)VALUES(?,?,?,?,?,?)""", (id,Width, Height, Diameter, Charge, Speed))
            self.__interact("""INSERT INTO stock (id, prix, quantite)VALUES(?,?,?)""", (id,prix_info[Diameter] ,quantite))
            return True
        return False
        
    def read_sql(self):
        conn=sq.connect(f"{self.__path}/{self.__name}")
        return pd.read_sql_query("""SELECT property.id, property.largeur, property.hauteur, property.diametre, property.charge ,property.vitesse ,stock.prix,stock.quantite FROM stock JOIN property ON stock.id = property.id""", conn).to_dict(orient="records")
    
    def remove_data(self, id):
        self.__interact(f"""DELETE FROM stock WHERE id = '{id}'""")
        self.__interact(f"""DELETE FROM property WHERE id = '{id}'""")

    def add_quantity(self, id, quantite):
        self.__interact(f"""UPDATE stock SET quantite = quantite + {quantite} WHERE id = '{id}'""")
        
    def remove_quantity(self, id, quantite):
        self.__interact(f"""UPDATE stock SET quantite = quantite - {quantite} WHERE id = '{id}'  AND quantite >= {quantite}""")

    def __create_folder(self):
        init = ''
        for directory in self.__path.split('/'):
            init += f'{directory}/'
            if not os.path.isdir(init):
                os.mkdir(init)

    def __interact(self, arg, arg2=None):
        conn=sq.connect(f"{self.__path}/{self.__name}")
        if arg2 != None:
            ret = conn.cursor().execute(arg, arg2).fetchall()
        else:
            ret = conn.cursor().execute(arg).fetchall()
        conn.commit()
        conn.close()
        return ret
    
    def Check_Argument(self,id: str):
        Width = id[:3].replace(".", "")
        Height = id[3:6].replace(".", "")
        Diameter = id[6:8].replace(".", "")
        Charge = id[8:9].replace(".", "")
        Speed = id[9:12].replace(".", "")
        search = []
        arg = f"""SELECT property.id, property.largeur, property.hauteur, property.diametre, property.charge ,property.vitesse ,stock.prix,stock.quantite FROM stock JOIN property ON stock.id = property.id WHERE"""
        if id.replace(".", "") == "":
            return None
        if Width != "":
            search.append(f"property.largeur = {int(Width)}")
        if Height != "":
            search.append(f"property.hauteur = {int(Height)}")
        if Diameter != "":
            search.append(f"property.diametre = {int(Diameter)}")
        if Charge != "":
            search.append(f"property.charge = '{Charge}'")
        if Speed != "":
            search.append(f"property.vitesse = {int(Speed)}")
        Get_Data = self.__interact(f"{arg} {' AND '.join(search)}")
        if Get_Data != []:
            y = []
            for x in Get_Data:
                y.append({"id" : x[0], 'largeur': x[1], 'hauteur': x[2], 'diametre': x[3], 'charge': x[4], 'vitesse': x[5], 'prix': x[6], 'quantite' : x[7]})
            return y
        return None
