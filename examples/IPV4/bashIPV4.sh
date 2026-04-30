#!/bin/bash

# Nomi dei file Python
DEPLOY_SCRIPT="clientIPV4.py"
UNDEPLOY_SCRIPT="clientUndeployIPV4.py"

# Esecuzione del primo script: creazione e deploy
echo "========================================="
echo "Avvio della creazione e del deploy del lab..."
echo "========================================="
python3 "$DEPLOY_SCRIPT"

# Controllo se il primo script è terminato senza errori
if [ $? -ne 0 ]; then
    echo "Si è verificato un errore durante la creazione del lab. Interruzione."
    exit 1
fi

echo ""
echo "Deploy completato con successo!"
echo ""

# Pausa per permetterti di testare il lab prima di distruggerlo
read -p "Premi [INVIO] quando sei pronto per eseguire l'undeploy del lab..."

# Esecuzione del secondo script: undeploy
echo "========================================="
echo "Avvio dell'undeploy del lab..."
echo "========================================="
python3 "$UNDEPLOY_SCRIPT"

echo "Operazione completata."