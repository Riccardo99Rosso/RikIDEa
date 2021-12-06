# RikIDEa

RIkIDEa è un micro IDE creato con l'intento di avere un IDE light ed editabile facilmente strutturato soprattutto per i principianti.
L'IDE è strutturato in un unico script costruito per poter essere aperto in edit se qualcosa vuole essere modificato all'interno dell'IDE e con il classico doppio click quando lo si volesse utilizzare come software.
La struttura interna non sfrutta oggetti che non siano quelli incorporati nelle librerie Python e quindi utilizza la semplice programmazione procedurale.
Oltre ai comandi che vengono mostrati nel menu' in alto aggiungo:

- Ctrl + rotella del mouse per zoomare avanti e indietro (o zoom con il trackpad)
- esc al posto di F11 per uscire dallo schermo intero
- Se attivata la modalità Auto-fill dal menù edit si può utilizzare 'alt gr' per visualizzare le altre parole suggerite nel completamento di una parola e tab o Shift destro per completarla.

Una problematica che in questa versione non ha purtroppo soluzione è l'impossibilità di leggere lo storico (undo e redo) nel momento in cui si passa da uno script all'altro poichè
non vengono usati tab e viene gestito il multi-script attraverso la chiusura e riapertura dei files (visibili con l'impostazione 'Show files window' dal menù window).

Aggiungo inoltre che:

- La modalità Auto-fill ha qualche bug e non mi soddisfa per due motivi: a volte suggerimenti non perfettamente corretti e influenza dell'Undo (Ctrl+z) e Redo (Ctrl+y) (vorrei che non andasse ad incidere nelle varie finestre temporali l'autocomplete).
  Per questo motivo verrà in seguito sostituito l'Auto-fill con una finestra di suggerimenti tra cui poter selezionare la parola che corrispondente (con la più probabile già suggerita e selezionata per il tab di completamento)

- L'IDE supporta un Indentation fixer che sostituisce nel luogo della selezione ogni 4 spazi con un tab.

- Il reverse indent funziona come un tab ma al contrario 

- Se si seleziona una parola e si attiva il searcher, quella parola verrà automaticamente inserita nella finestra come se fosse stata copiata e incollata

- L'IDE supporta una funzione di run originale (Run Alone) capace di eseguire solo il codice selezionato dall'utente.
  In un caso in cui io avessi:

  ```python
  x = 5
  if x == 5:
      print("cinque")
  else:
      print("boh")
  ```

  e volessi semplicemente runnare `print("cinque")`, mi basterebbe selezionare l'istruzione e avviare il Run Alone mentre se volessi mandare in run più di una riga la selezione deve iniziare da inizio riga e non dalla semplice istruzione

- Esiste un supporto di indentazione automatico particolarmente immediato (anche indentazione corretta dopo l'inserimento di ':' su una linea che inizia con una keyword)

- Ha un processo autonomo di colorazione della sintassi e altre features ancora.

Se desse fastidio il terminale che si apre insieme all'IDE basta salvare l'IDE come .pyw invece di .py
