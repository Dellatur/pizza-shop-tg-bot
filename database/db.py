import sqlite3 as sql

conn = sql.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS pizza (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    price INTEGER NOT NULL,
    image_url TEXT DEFAULT NULL
)
''')

cursor.executemany('''
INSERT INTO pizza (name, ingredients, price, image_url) VALUES (?, ?, ?, ?)
''', [
    ('Пепперони', 'томатный соус, сыр моцарелла, пепперони', 500, 'images/pizza/pepperoni.jpg'),
    ('Маргарита', 'томатный соус, сыр моцарелла, свежие томаты, базилик', 450, 'images/pizza/margherita.jpg'),
    ('Четыре сыра', 'томатный соус, сыр моцарелла, сыр горгонзола, сыр пармезан, сыр эмменталь', 600, 'images/pizza/four_cheese.jpg'),
    ('Гавайская', 'томатный соус, сыр моцарелла, ветчина, ананасы', 550, 'images/pizza/hawaiian.jpg'),
    ('Мясная', 'томатный соус, сыр моцарелла, пепперони, ветчина, бекон, колбаски', 650, 'images/pizza/meat.jpg'),
    ('Овощная', 'томатный соус, сыр моцарелла, сладкий перец, красный лук, шампиньоны, черные оливки', 500, 'images/pizza/vegetarian.jpg'),
    ('Диабло', 'томатный соус, сыр моцарелла, пепперони, острая колбаса, перец чили, халапеньо', 700, 'images/pizza/diablo.jpg'),
    ('Куриная BBQ', 'соус BBQ, сыр моцарелла, куриное филе, красный лук, кукуруза', 600, 'images/pizza/chicken_bbq.jpg')
])
conn.commit()
conn.close()