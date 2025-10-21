import random
import pandas as pd

# ==================================
# PRODUZIONE AGRICOLA INTELLIGENTE
# ==================================

def genera_quantita(prodotti, superfice_ettari):
    """
    Genera casualmente la quantità da produrre per ciaascun prodotto agricolo.
    Ogni quantità è proporzionale alla superficie coltivata e alla resa media ettaro.
    """
    quantita = {}
    for prodotto, resa in prodotti.items():
        # Genera una resa variabile con +/-20% di variabilità per simulare condizioni reali
        resa_reale = resa * random.uniform(0.8, 1.2)
        # Quantità prodotta = resa_reale * ettari
        quantita[prodotto] = round(resa_reale * superfice_ettari, 2)
    return quantita

def configura_parametri():
    """ Imposta i parametri principali del processo produttivo:
    resa per ettaro, tempo di produzione unitario e capacità giornaliera. 
    leggendo da un file di configurazione """
    # Apro il file in sola lettura 
    f = open("config.ini", "r") 
    # Dichiaro le strutture dati in cui verrano caricati i dati 
    prodotti = {}
    tempi_unitari = {}
    capacità_giornaliera = {}
    confezionamento = {}
    superfice = 0
    sup = 0

    for riga in f:
        riga_pulita = riga.replace('\n','').rstrip()
        spl1 = riga_pulita.split(";")
        for riga_pulita in spl1:
            dettaglio = riga_pulita.split(",")
            if dettaglio[0] == "superfice":
                sup =  int(dettaglio[1])          
            if dettaglio[0] == "cultura":
                prodotto =  dettaglio[1]          
            if dettaglio[0] == "quintali_Ettaro":
                qpr = int(dettaglio[1])
            if dettaglio[0] == "tempi_unitari":
                tpu = float(dettaglio[1])
            if dettaglio[0] == "capacita_giornaliera":
                cpg = float(dettaglio[1])
            if dettaglio[0] == "confezionamento":
                cfn = float(dettaglio[1]) 
        if sup == 0:
            prodotti[prodotto] = qpr
            tempi_unitari[prodotto] = tpu
            capacità_giornaliera[prodotto] = cpg
            confezionamento[prodotto] = cfn
        else: 
            superfice = sup
            sup = 0         

    # Chiudo la lettura del file di configurazione dei prodotti
    f.close()
    # Restiruisco le strutture dati opportunamente caricate
    return prodotti, tempi_unitari, capacità_giornaliera, confezionamento, superfice

def simula_produzione(quantita, tempi_unitari, capacita_giornaliera, sequenza, confezionamento):
    """
    Calcola il tempo totale di produzione per ciascun prodotto,
    in base alla quantita generata, ai tempi unitari e alla capacità giornaliera.
    """
    risultati = []
    seq = sequenza[:1]

    for prodotto, quant in quantita.items():
        tempo_unit = tempi_unitari[prodotto]
        capacita = capacita_giornaliera[prodotto]
        confezion = confezionamento[prodotto]

        # Tempo totale di produzione in ore in base la tipo di sequenza produttiva
        match seq:
            case "A":
                tempo_totale_ore = quant * tempo_unit
            case "B":
                tempo_unit += confezion
                tempo_totale_ore = quant * tempo_unit
     
        # Giorni necessari = quantità / capacita giornaliera
        giorni = quant / capacita

        risultati.append({
            "Sequenza": sequenza,
            "Prodotto": prodotto,
            "Quantità (quintali)": quant,
            "Tempo unitario (h/quintale)": tempo_unit,
            "Tempo totale (h)": round(tempo_totale_ore, 2),
            "Giorni necessari": round(giorni, 2)
        })
        
    return risultati

def stampa_risultati(risultati_A, risultati_B):
    """
    Stampa e confronta i risultati delle due sequenze produttive,
    """
    df_A = pd.DataFrame(risultati_A)
    df_B = pd.DataFrame(risultati_B)

    print("\n===== RISULTATI SEQUENZA A: RACCOLTA E STOCCAGGIO =====")
    print(df_A.to_string(index=False))

    print("\n===== RISULTATI SEQUENZA B: RACCOLTA, LAVORAZIONE E CONFEZIONAMENTO =====")
    print(df_B.to_string(index=False))

    # Confronto generale
    print("\n===== ANALISI COMPARATIVA =====")
    totale_A = df_A["Tempo totale (h)"].sum()
    totale_B = df_B["Tempo totale (h)"].sum()
    print(f"Tempo totale Sequenza A: {totale_A:.2f} ore")
    print(f"Tempo totale Sequenza B: {totale_B:.2f} ore")

    if totale_A < totale_B:
        print("\n-> La Sequenza A risulta più efficiente in termini di tempo complessivo.")
    else:
        print("\n-> La Sequenza B richiede un maggiore tempo produttivo.")
    
    print("\n")

def main():
    print("\n")
    print("\nSIMULAZIONE PROCESSO PRODUTTIVO AGRICOLO - CULTIVAR FUTURA S.R.L.")
    print("==================================================================\n")
    
    prodotti, tempi_unitari, capacita_giornaliera, confezionamento, superfice = configura_parametri()

    # Stampo la Superfice Coltivabile in Ettari
    print(f"Superfice coltivabile: {superfice} ettari\n")

    # Generazione quantita causali
    quantita = genera_quantita(prodotti, superfice)
    print("Quantità generate casualmente (quintali):")
    for k, v in quantita.items():
        print(f" - {k} \t: {v} q.li")
    
    # Simulazione delle due sequenze
    risultati_A = simula_produzione(quantita, tempi_unitari, capacita_giornaliera, "A - Raccolta/Stoccaggio", confezionamento)
    risultati_B = simula_produzione(quantita, tempi_unitari, capacita_giornaliera, "B - Raccolta/Lavorazione/Confezionamento", confezionamento)

    # Stampa e confronto risultati
    stampa_risultati(risultati_A, risultati_B)

if __name__ == "__main__":
    main()