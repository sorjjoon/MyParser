[Heroku link](https://vast-refuge-33676.herokuapp.com/)

Projekti ei tällä hetkellä toimi herokussa (se toimii lokaalisti, sekä reposta suoraan kloonaamalla ongelmitta). Ongelma liittyy runtime.txt tiedostoon, joka löytyy tästä reposta. Haluaisin käyttää python3.8 versiota projektiini (se tuo muutaman päivämäärien ja aikojen lukemiseen liittyvän funktion joita haluasin käyttää), ja heroku haluaa tämän tehtävän lisäämällä haluttu versio projektiin juuren runtime.txt tiedostoon (kuten requirments.txt)
Mutta kun pusken muutokset herokun git, saan virheen, 

remote: -----> Python app detected                                                                                                                                                                                                                                             remote:  !     Requested runtime (ÿþpython-3.8.1) is not available for this stack (heroku-18).    

Hetken hiusten repimisen jälkeen tajusin herokun lukevan tiedoston ut8 muodossa, joten kokeilin 
 echo "python-3.8.1" | out-file -encoding utf8 runtime.txt
(käytän ps windowsilla niin en tiedä mikä vastaava on ubuntulla), ja sain virhe ilmoituksen muuttuumaan
remote: -----> Python app detected                                                                                                                                                                                                                                             remote:  !     Requested runtime ( python-3.8.1) is not available for this stack (heroku-18).                                                                                                                                                                                  

Ja oletan, että jostain syystä tietokoneeni lisää ylimääräisen tavun tai kaksi python3.8.1 eteen (mikään tekstiedtori ei näytä python edessä olevan välilyöntiä), ja heroku ei osaa lukea tiedostoa tästä syystä (olen yrittänyt lukea ja kirjoitta tiedostoa tavu kerrallaan, mutta en ole onnistunut vielä löytämään versiota jonka heroku hyväksyy)

Korjaan kyllä ongelman ensi viikkon mennessä (kokeilen tiedoston kirjoittamista linux koneella, ja jos ei muu auta niin kirjoitan jonkin pienen päivämäärän lukijan itse 😔), mutta huomasin ongelman vasta tänään, ja lisäsin tämän selityksen, jos satut tarkastaamaan projektin, ennen kuin ehdin korjata sen

# MyParser
MyParser This project is for the interpretation (parsing) of combat logs provided by the role-playing game Star Wars The Old Republic (SWTOR). The goal is to provide users with statistics regarding their performance by analyzing logs provided by the user.

This project in particular deals with the storage of logs, and in particular logs for ranked pvp games and aims to provide the user statistics regarding played matches, win rate when playing with certain players etc.


[User stories](/documentation/stories.md)  
[Database](/documentation/data.png)
