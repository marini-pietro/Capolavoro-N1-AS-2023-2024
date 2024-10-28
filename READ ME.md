Marini Pietro  
 Matricola:20548

**Relazione Capolavoro AS 2023-2024**

**Capolavoro N॰1:** [Rendering voxel con Pygame e ModernGL](https://github.com/shogun-ttgl/Capolavoro-N1-AS-2023-2024.git)

Prima di presentare la descrizione del progetto è necessario che introduca brevemente le tecnologie che ho applicato per realizzarlo:

* [Python](https://www.python.org/) 3.12.1 → Linguaggio di programmazione interpretato ad alto livello, orientato a oggetti ed conosciuto per la sua versatilità e sintassi concisa.  
* [Pygame](https://www.pygame.org/wiki/about) 2.5.2 → Libreria aggiuntiva per il linguaggio Python open-source quasi interamente scritta in [C](https://en.wikipedia.org/wiki/C_\(programming_language\)) per la creazione di videogiochi 2D-3D ed applicazioni di vario genere.  
* [ModernGL](https://github.com/moderngl/moderngl) 5.10.0 → Una rivisitazione moderna della storica API [OpenGL](https://www.opengl.org/).  
* [OpenSimplex](https://en.wikipedia.org/wiki/OpenSimplex_noise) → Libreria di generazione di rumore in grado di creare del rumore di qualità maggiore rispetto al [rumore di Perlin](https://it.m.wikipedia.org/wiki/Rumore_di_Perlin), spesso usato nella creazione di videogiochi.  
* [Voxel](https://it.wikipedia.org/wiki/Voxel) → Unità di volume cubica utilizzata nel mondo del rendering 3D per vari scopi.

E le motivazioni che mi hanno portato a fare questa scelta:

* Python: È il primo linguaggio di programmazione che ho imparato come autodidatta durante la prima superiore, mi risulta quindi naturale e tramite esso è possibile realizzare applicazioni e progetti di vario genere.  
* Pygame: Rappresenta il mio primo tentativo di entrare nel mondo del game development, un campo di cui sono particolarmente interessato.  
  Vista la sua natura semplicistica costituisce un ottimo inizio per chiunque voglia cominciare a sviluppare giochi, in quanto tramite essa si possono acquisire diverse buone abitudini da poi trasportare in ambienti di lavoro più complessi come Unity o Unreal Engine.  
* ModernGL: Semplifica l’utilizzo di OpenGL tramite l’adozione di nuovi strumenti e convenzioni moderne mantenendo però la compatibilità di OpenGL con hardware di vecchia data.  
* Utilizzo dei voxel: Grazie alla loro versatilità e facilità di implementazione costituiscono un buono strumento con cui fare esperienza e da tenere in mente per ogni aspirante game developer.  
  Pur avendo origine negli anni ‘60 ed essendo ormai abbandonata come tecnologia in favore di poligoni i voxel vengono ancora raramente utilizzati in giochi moderni come Counter Strike: Global Offensive 2, un gioco [AAA](https://it.wikipedia.org/wiki/AAA_\(videogiochi\)) (tripla A) rinomato in tutto il mondo.


**Descrizione del progetto:** 

Il progetto presentato consiste in una [demo](https://it.wikipedia.org/wiki/Demo#Informatica) di un motore grafico tridimensionale realizzato tramite l’uso di voxel e di triangoli di varie dimensioni posizionati secondo del rumore generato tramite la libreria [OpenSimplex](https://en.wikipedia.org/wiki/OpenSimplex_noise).  
La stessa libreria utilizzata per poter inserire nel mondo alberi, nuvole, caverne, neve, sabbia e forme d’acqua in modo randomico.  
L'acqua è gestita in modo che venga visualizzata leggermente più bassa degli altri blocchi per motivi estetici e una volta che il giocatore vi si immerge sulla finestra verrà applicato un filtro blu.  
Per motivi estetici sono state aggiunti diversi dettagli di cui però non è possibile garantire il corretto funzionamento su tutte le configurazioni hardware, questi sono:

* Leggera nebbia nella lontananza.  
* MSAA: Multi Sampling [Anti Aliasing](https://it.wikipedia.org/wiki/Antialiasing), tecnica implementata per implementata per smussare i bordi e migliorare l’immagine.  
  Tale metodo agisce sui bordi dei poligoni (non su tutta l'immagine), e l'effetto aliasing viene eliminato tramite un filtro di bilanciamento dei colori: se due (o più) poligoni giacciono sullo stesso pixel, il colore del pixel viene determinato in base ai colori dei poligoni. Per esempio, se su un pixel ci sono due poligoni di colori diversi p1 che copre 2/3 e p2 che copre il restante terzo, il colore del pixel sarà uguale al bilanciamento dei due colori, tenendo conto che la "forza" del colore di p1 sarà doppia rispetto a quella di p2.  
  Questa analisi sarà tanto più precisa quanto maggiore sarà tale filtro (2x, 4x, 8x, ecc).  
* Maschera ad isola: Senza l’implementazione di questa tecnica i bordi quadrati del mondo sarebbero evidenti risultando in un effetto sgradevole.  
  Quindi, tramite l’uso di del rumore e una specifica formula matematica:

    
  island \= 1 / (pow(0.0025 \* math.hypot(x \- CENTER\_XZ, z \- CENTER\_XZ), 20) \+ 0.0001)  
  island \= min(island, 1)

    
  è possibile fare in modo che il mondo appaia come un'isola risultando in un effetto decisamente più gradevole.

È possibile interagire con il mondo rimuovendo e piazzando blocchi a volontà tramite i pulsanti del mouse.  
Per aumentare le prestazioni sono state implementate diverse tecniche:

* **Face culling:** non renderizzare le facce dei voxel non visibili al giocatore.  
* **Frustum culling:** renderizzare solamente la porzione di terreno compresa nel campo visivo del giocatore.  
* **La compressione di dati tramite [operazioni bit per bit](https://it.wikipedia.org/wiki/Operazione_bit_a_bit):** Alcune variabili necessarie per il funzionamento del programma possono assumere solamente un numero inferiore di valori rispetto a quelli resi disponibili dagli 8 bit associati ad ogni dato.  
  Per esempio, nel caso del face id il numero di valori possibili è solamente 6 mentre quelli resi disponibili dagli 8 bit sono 256, si ha quindi una sostanziale quantità di dati inutilmente passata alla GPU causando una riduzione nelle prestazioni.  
  Per risolvere questo problema i valori sono stati compressi tramite operazioni di bit shift in modo che ad ogni variabile venga associato solamente il numero di bit minimo per garantire il corretto funzionamento.  
  Assieme quindi a i dati compressi quindi vengono anche passati alla GPU il numero di bit per cui è stato fatto lo shift, in modo che la GPU possa ricevere i dati e decomprimerli correttamente.

**Modalità di utilizzo del progetto:**

Dopo aver installato la versione [Python](https://www.python.org/downloads/release/python-3121/) citata nell’introduzione l’unico requisito rimanente è installare le librerie necessarie tramite questo comando eseguibile nel prompt dei comandi:  
	pip install pygame moderngl numpy PyGLM numba opensimplex  
Tramite il rispettivo comando:   
	pip uninstall \-y pygame moderngl numpy PyGLM numba opensimplex  
è possibile invece disinstallare i pacchetti se si desidera.  
Una volta fatto ciò per avviare il progetto basta avviare il file main.py, se invece si vogliono modificare delle impostazioni è possibile modificare il file settings.py, è possibile, per esempio, modificare le dimensioni del mondo e della finestra, cambiare il mondo modificando il [seme](https://it.wikipedia.org/wiki/Numeri_pseudo-casuali) e modificare la velocità di movimento.  
Per chiudere la finestra e quindi terminare il processo basta premere escape sulla tastiera o la x in alto a destra nella finestra.

**Eventuali crediti e fonti:**

La base concettuale del progetto è stata scritta e progettata seguendo una [repository](https://it.wikipedia.org/wiki/Repository) su GitHub, di cui è possibile vedere le licenza nel seguente paragrafo:

Licenza del MIT

Copyright (c) 2023 [StanislavPetrovV](https://github.com/StanislavPetrovV)

L'autorizzazione è concessa, gratuitamente, a chiunque ne ottenga una copia  
di questo software e dei file di documentazione associati (il "software"), da trattare  
nel software senza restrizioni, inclusi senza limitazione i diritti  
utilizzare, copiare, modificare, unire, pubblicare, distribuire, concedere in sublicenza e/o vendere copie del Software e per consentire alle persone a cui è destinato il Software  
attrezzato per farlo, alle seguenti condizioni.

