import csv
import hashlib
from datetime import datetime
import os

# Funksjon for å kryptere passord ved hjelp av SHA-256 hashing
def krypterPassord(passord):
    return hashlib.sha256(passord.encode()).hexdigest()

# Funksjon for å opprette en ny bruker
def opprettBruker(brukernavn, passord):
    if not erAdministrator(nåværende_bruker):  # Sjekk om den nåværende brukeren er administrator
        raise PermissionError("Bare administratorer kan opprette brukere")
    kryptertPassord = krypterPassord(passord)  # Krypter passordet
    gruppe = input('Velg gruppe (administrator/bruker): ')  # Be om brukergruppe
    # Legg til den nye brukeren i CSV-filen
    with open('brukere.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([brukernavn, kryptertPassord, gruppe])
    print('Bruker opprettet!')

# Funksjon for å slette en bruker
def slettBruker(brukernavn):
    if not erAdministrator(nåværende_bruker):  # Sjekk om den nåværende brukeren er administrator
        raise PermissionError("Bare administratorer kan slette brukere")
    rader = []
    # Les alle brukere bortsett fra den som skal slettes
    with open('brukere.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for rad in reader:
            if rad[0] != brukernavn:
                rader.append(rad)
    # Skriv de gjenværende brukerne tilbake til CSV-filen
    with open('brukere.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rader)
    print('Bruker slettet!')

# Funksjon for å endre passordet til en bruker
def endreBrukerPassord(brukernavn):
    if not erAdministrator(nåværende_bruker):  # Sjekk om den nåværende brukeren er administrator
        raise PermissionError("Bare administratorer kan endre passord")
    nytt_passord = input("Skriv inn det nye passordet for {}: ".format(brukernavn))
    oppdatert = False
    rader = []
    # Les alle brukere og oppdater passordet for den spesifikke brukeren
    with open('brukere.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for rad in reader:
            if rad[0] == brukernavn:
                rad[1] = krypterPassord(nytt_passord)
                oppdatert = True
            rader.append(rad)
    # Skriv de oppdaterte brukerne tilbake til CSV-filen
    if oppdatert:
        with open('brukere.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rader)
        print("Passord for {} endret vellykket.".format(brukernavn))
    else:
        print("Bruker ikke funnet.")

# Funksjon for å logge inn en bruker
def loggInn(brukernavn, oppgitt_passord):
    # Les alle brukere og sjekk om brukernavn og passord stemmer
    with open('brukere.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for rad in reader:
            lagret_bruker, lagret_passord, gruppe = rad
            if brukernavn == lagret_bruker and krypterPassord(oppgitt_passord) == lagret_passord:
                print('Du er nå logget inn!')
                global nåværende_bruker
                nåværende_bruker = brukernavn
                return gruppe
    print('Feil brukernavn eller passord')
    return None

# Funksjon for å sjekke om en bruker er administrator
def erAdministrator(brukernavn):
    # Les alle brukere og sjekk om brukernavnet tilhører en administrator
    with open('brukere.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for rad in reader:
            lagret_bruker, lagret_passord, gruppe = rad
            if brukernavn == lagret_bruker and gruppe == 'administrator':
                return True
    return False

# Funksjon for å registrere arbeidstimer
def registrerArbeidstimer(brukernavn):
    i_dag = datetime.today().date()  # Få dagens dato
    år = i_dag.year  # Få inneværende år
    timer_arbeidet = float(input('Skriv inn antall arbeidstimer i dag: '))  # Be om antall arbeidstimer

    funnet = False
    rader = []
    # Les eksisterende arbeidstimer og oppdater hvis det finnes en post for inneværende år
    if os.path.exists('arbeidstimer.csv'):
        with open('arbeidstimer.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for rad in reader:
                if rad[0] == brukernavn and int(rad[1]) == år:
                    rad[2] = str(float(rad[2]) + timer_arbeidet)
                    funnet = True
                rader.append(rad)
    # Hvis ingen post ble funnet, legg til en ny
    if not funnet:
        rader.append([brukernavn, år, timer_arbeidet])
    # Skriv oppdaterte arbeidstimer tilbake til CSV-filen
    with open('arbeidstimer.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rader)
    print('Arbeidstimer registrert!')

# Funksjon for å redigere arbeidstimer
def redigerArbeidstimer(brukernavn):
    år = int(input('Skriv inn året for oppføringen som skal redigeres: '))
    nye_totale_timer = float(input('Skriv inn de nye totale arbeidstimene for året: '))

    funnet = False
    rader = []
    # Les eksisterende arbeidstimer og oppdater hvis det finnes en post for det angitte året
    if os.path.exists('arbeidstimer.csv'):
        with open('arbeidstimer.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for rad in reader:
                if rad[0] == brukernavn and int(rad[1]) == år:
                    rad[2] = nye_totale_timer
                    funnet = True
                rader.append(rad)
    # Skriv oppdaterte arbeidstimer tilbake til CSV-filen
    if funnet:
        with open('arbeidstimer.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rader)
        print('Arbeidstimer oppdatert!')
    else:
        print('Ingen oppføring funnet for det angitte året.')

# Funksjon for brukermeny
def brukerMeny():
    while True:
        print(f'Velkommen, {nåværende_bruker}! Du er en bruker.')
        print('1. Registrer arbeidstimer')
        print('2. Logg ut')

        try:
            valg = int(input('Velg en handling: '))
        except ValueError:
            print("Ugyldig input, vennligst skriv inn et tall.")
            continue
        
        if valg == 1:
            registrerArbeidstimer(nåværende_bruker)
        elif valg == 2:
            print('Du er nå logget ut.')
            break  
        else:
            print("Ugyldig valg, prøv igjen.")

# Funksjon for administratormeny
def administratorMeny():
    while True:
        print(f'Velkommen, {nåværende_bruker}! Du er en administrator.')
        print('1. Opprett en ny bruker')
        print('2. Slett en eksisterende bruker')
        print('3. Endre brukers passord')
        print('4. Rediger arbeidstimer')
        print('5. Logg ut')

        try:
            valg = int(input('Velg en handling: '))
        except ValueError:
            print("Ugyldig input, vennligst skriv inn et tall.")
            continue

        if valg == 1:
            nytt_brukernavn = input('Skriv inn et nytt brukernavn: ')
            nytt_passord = input('Skriv inn et nytt passord: ')
            opprettBruker(nytt_brukernavn, nytt_passord)
        elif valg == 2:
            slett_brukernavn = input('Skriv inn brukernavnet til brukeren du vil slette: ')
            slettBruker(slett_brukernavn)
        elif valg == 3:
            brukernavn_å_endre = input("Skriv inn brukernavnet til brukeren du vil endre passord for: ")
            endreBrukerPassord(brukernavn_å_endre)
        elif valg == 4:
            rediger_brukernavn = input("Skriv inn brukernavnet til brukeren du vil redigere arbeidstimer for: ")
            redigerArbeidstimer(rediger_brukernavn)
        elif valg == 5:
            print('Du er nå logget ut.')
            break
        else:
            print("Ugyldig valg, prøv igjen.")

# Hovedmenyfunksjon som avgjør hvilken meny som skal vises basert på brukerens gruppe
def hovedmeny(nåværende_bruker, gruppe):
    if gruppe == 'administrator':
        administratorMeny()
    else:
        brukerMeny()

# Startpunktet for programmet
if __name__ == "__main__":
    brukernavn = input('Skriv inn ditt brukernavn: ')
    passord = input('Skriv inn ditt passord: ')
    gruppe = loggInn(brukernavn, passord)
    if gruppe:
        hovedmeny(brukernavn, gruppe)
    else:
        print("Innlogging mislyktes. Avslutter programmet.")
