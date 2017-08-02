import sqlite3

tableCharacteristics = """CREATE TABLE IF NOT EXISTS caracteristicas (
								tipologia   INTEGER,
								caso        VARCHAR(8),
								ambiente    VARCHAR(12),
								amb         INTEGER,
								uParExt     REAL,
								ctParExt    REAL,
								expCob      REAL,
								uCob        REAL,
								ctCob       REAL,
								expPis      REAL,
								uPisExt     REAL,
								ctPisExt    REAL,
								uvid        REAL,
								fSvid       REAL,
								fatVen      REAL,
								absPar      REAL,
								absCob      REAL,
								uParInt     REAL,
								ctParInt    REAL,
								somb        REAL,
								ventCruz    REAL,
								areaUtil    REAL,
								aParInt     REAL,
								parExtN     REAL,
								parExtS     REAL,
								parExtL     REAL,
								parExtO     REAL,
								aVaoN       REAL,
								aVaoS       REAL,
								aVaoL       REAL,
								aVaoO       REAL,
								PRIMARY KEY(tipologia, caso, ambiente)
							);"""

tableHeating = """CREATE TABLE IF NOT EXISTS aquecimento (
						clima       VARCHAR(15),
						tipologia   INTEGER,
						caso        VARCHAR(8),
						amb         VARCHAR(12),
						january     REAL,
						february    REAL,
						march       REAL,
						april       REAL,
						may         REAL,
						june        REAL,
						july        REAL,
						august      REAL,
						september   REAL,
						october     REAL,
						november    REAL,
						december    REAL,
						anual       REAL,
						FOREIGN KEY(tipologia, caso, amb) REFERENCES caracteristicas(tipologia, caso, ambiente)
						FOREIGN KEY(clima, tipologia, caso, amb) REFERENCES resfriamento(clima, tipologia, caso, amb)
						FOREIGN KEY(clima, tipologia, caso, amb) REFERENCES conforto(clima, tipologia, caso, amb)
						PRIMARY KEY(clima, tipologia, caso, amb)
						);"""

tableCooling = """CREATE TABLE IF NOT EXISTS resfriamento (
						clima       VARCHAR(15),
						tipologia   INTEGER,
						caso        VARCHAR(8),
						amb         VARCHAR(12),
						january     REAL,
						february    REAL,
						march       REAL,
						april       REAL,
						may         REAL,
						june        REAL,
						july        REAL,
						august      REAL,
						september   REAL,
						october     REAL,
						november    REAL,
						december    REAL,
						anual       REAL,
						FOREIGN KEY(tipologia, caso, amb) REFERENCES caracteristicas(tipologia, caso, ambiente)
						FOREIGN KEY(clima, tipologia, caso, amb) REFERENCES aquecimento(clima, tipologia, caso, amb)
						FOREIGN KEY(clima, tipologia, caso, amb) REFERENCES conforto(clima, tipologia, caso, amb)
						PRIMARY KEY(clima, tipologia, caso, amb)
						);"""

tableConf = """CREATE TABLE IF NOT EXISTS conforto (
						clima       VARCHAR(15),
						tipologia   INTEGER,
						caso        VARCHAR(8),
						amb         VARCHAR(12),
						january1     REAL,
						february1    REAL,
						march1       REAL,
						april1       REAL,
						may1         REAL,
						june1        REAL,
						july1        REAL,
						august1      REAL,
						september1   REAL,
						october1     REAL,
						november1    REAL,
						december1    REAL,
						anual1       REAL,
						january2     REAL,
						february2    REAL,
						march2       REAL,
						april2       REAL,
						may2         REAL,
						june2        REAL,
						july2        REAL,
						august2      REAL,
						september2   REAL,
						october2     REAL,
						november2    REAL,
						december2    REAL,
						anual2       REAL,
						january3     REAL,
						february3    REAL,
						march3       REAL,
						april3       REAL,
						may3         REAL,
						june3        REAL,
						july3        REAL,
						august3      REAL,
						september3   REAL,
						october3     REAL,
						november3    REAL,
						december3    REAL,
						anual3       REAL,
						consumo      REAL,
						phoras       REAL,
						FOREIGN KEY(tipologia, caso, amb) REFERENCES caracteristicas(tipologia, caso, ambiente)
						FOREIGN KEY(clima, tipologia, caso, amb) REFERENCES aquecimento(clima, tipologia, caso, amb)
						FOREIGN KEY(clima, tipologia, caso, amb) REFERENCES resfriamento(clima, tipologia, caso, amb)
						PRIMARY KEY(clima, tipologia, caso, amb)
						);"""

if __name__ == '__main__':
	conn = sqlite3.connect('../resultadoAnaliseNBR.db')
	cursor = conn.cursor()

	cursor.execute(tableCharacteristics)
	cursor.execute(tableHeating)
	cursor.execute(tableCooling)
	cursor.execute(tableConf)

	conn.commit()
	conn.close()