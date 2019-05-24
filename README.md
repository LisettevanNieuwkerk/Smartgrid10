<h1> HI! Welkom in de repository van team Smartgrid10! </h1>

In onze repository kun je een aantal verschillende algoritmes runnen om het probleem van de Smartgrid op te lossen. Het doel van onze case was het minimaliseren van de kosten, met in achtneming van de constraints; een constraint optimization problem dus. Laat je leiden door de gids in de terminal en enjoy the ride :-)!

----------------------------------------------------------------------------------
<b>Aan de slag (Getting Started)</b>

Deze codebase is volledig geschreven in Python3.6.3. In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

pip install -r requirements.txt

----------------------------------------------------------------------------------
<b>Structuur (Structure)</b>

De meeste Python scripts staan in de folder Code. De smartgrid.py file en de application.py staan in de hoofdmap. De application wordt gerund om alles te laten runnen en de smartgrid.py file dient als 'helperfile'. In de map Data zitten alle input waardes en in de map resultaten worden alle resultaten opgeslagen door de code.

----------------------------------------------------------------------------------
<b>Test (Testing)</b>

Om de code te draaien voer je in de terminal het volgende in:

python3 application.py

Hierna zal een keuzemenu volgen waarin je de verschillende algoritmes kunt selecteren runnen.

----------------------------------------------------------------------------------
<b>Side notes</b>

Brute force:

Het Brute force algorithm geeft, gezien de state space van ons probleem (+- 4,5^100), geen antwoord binnen afzienbare tijd. Deze hebben we in een enthousiaste beginfase gebouwd, maar verder niet meer gebruikt. 

Stap D) van de opdracht:

Bij stap D van de opdracht krijgen we te maken met nieuwe batterijen. Wanneer je deze functie selecteert, dan genereert deze alleen een Random set uit deze batterijen met in totaal een capaciteit tot boven de 7500 (Output van alle huizen is voor elke wijk 7500 > dus mininmaal 7500 capaciteit nodig). Op deze random gegenereerde set van batterijen kunnen wel alle algoritmes worden gerund, maar we hebben nog geen optimalisaties voor de combinaties van verschillende batterijen gemaakt.


----------------------------------------------------------------------------------
<b> Auteurs (Authors)</b>

Lisette van Nieuwkerk, David Mokken & Casper Lammers


----------------------------------------------------------------------------------
<b> Dankwoord (Acknowledgments): </b>

Het wereldwijde web

Okke & Quinten & Daan 


