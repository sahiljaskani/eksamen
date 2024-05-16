import csv
import hashlib
from datetime import datetime
import os

def krypterPassord(passord):
    return hashlib.sha256(passord.encode()).hexdigest()

def opprettBruker(epost, passord):
    if not erAdministrator(nåværende_bruker):
        raise PermissionError("Bare administratorer kan opprette brukere")
    kryptertPassord = krypterPassord(passord)
    gruppe = input('Velg gruppe (administrator/bruker): ')
    with open('randoms.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["", "", epost, "", "", kryptertPassord, gruppe])
    print('Bruker opprettet!')

def slettBruker(epost):
    if not erAdministrator(nåværende_bruker):
        raise PermissionError("Bare administratorer kan slette brukere")
    rader = []
    with open('randoms.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for rad in reader:
            if rad[2] != epost:
                rader.append(rad)
    with open('randoms.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rader)
    print('Bruker slettet!')

def endreBrukerPassord(epost):
    if not erAdministrator(nåværende_bruker):
        raise PermissionError("Bare administratorer kan endre passord")
    nytt_passord = input("Skriv inn det nye passordet for {}: ".format(epost))
    oppdatert = False
    rader = []
    with open('randoms.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for rad in reader:
            if rad[2] == epost:
                rad[5] = krypterPassord(nytt_passord)
                oppdatert = True
            rader.append(rad)

    if oppdatert:
        with open('randoms.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rader)
        print("Passord for {} endret vellykket.".format(epost))
    else:
        print("Bruker ikke funnet.")

def loggInn(epost, oppgitt_passord):
    with open('randoms.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for rad in reader:
            if rad[2] == epost and krypterPassord(oppgitt_passord) == rad[5]:
                print('Du er nå logget inn!')
                global nåværende_bruker
                nåværende_bruker = epost
                return rad[6]
    print('Feil brukernavn eller passord')
    return None

def erAdministrator(epost):
    with open('randoms.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for rad in reader:
            if rad[2] == epost and rad[6] == 'administrator':
                return True
    return False

def registrerArbeidstimer(epost):
    i_dag = datetime.today().date()
    år = i_dag.year
    timer_arbeidet = float(input('Skriv inn antall arbeidstimer i dag: '))

    funnet = False
    rader = []
    if os.path.exists('arbeidstimer.csv'):
        with open('arbeidstimer.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for rad in reader:
                if rad[0] == epost and int(rad[1]) == år:
                    rad[2] = str(float(rad[2]) + timer_arbeidet)
                    funnet = True
                rader.append(rad)

    if not funnet:
        rader.append([epost, år, timer_arbeidet])

    with open('arbeidstimer.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rader)

    print('Arbeidstimer registrert!')

def redigerArbeidstimer(epost):
    år = int(input('Skriv inn året for oppføringen som skal redigeres: '))
    nye_totale_timer = float(input('Skriv inn de nye totale arbeidstimene for året: '))

    funnet = False
    rader = []
    if os.path.exists('arbeidstimer.csv'):
        with open('arbeidstimer.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for rad in reader:
                if rad[0] == epost and int(rad[1]) == år:
                    rad[2] = nye_totale_timer
                    funnet = True
                rader.append(rad)

    if funnet:
        with open('arbeidstimer.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rader)
        print('Arbeidstimer oppdatert!')
    else:
        print('Ingen oppføring funnet for det angitte året.')

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
            ny_epost = input('Skriv inn en ny e-post: ')
            nytt_passord = input('Skriv inn et nytt passord: ')
            opprettBruker(ny_epost, nytt_passord)
        elif valg == 2:
            slett_epost = input('Skriv inn e-posten til brukeren du vil slette: ')
            slettBruker(slett_epost)
        elif valg == 3:
            epost_å_endre = input("Skriv inn e-posten til brukeren du vil endre passord for: ")
            endreBrukerPassord(epost_å_endre)
        elif valg == 4:
            rediger_epost = input("Skriv inn e-posten til brukeren du vil redigere arbeidstimer for: ")
            redigerArbeidstimer(rediger_epost)
        elif valg == 5:
            print('Du er nå logget ut.')
            break
        else:
            print("Ugyldig valg, prøv igjen.")

def hovedmeny(nåværende_bruker, gruppe):
    if gruppe == 'administrator':
        administratorMeny()
    else:
        brukerMeny()

if __name__ == "__main__":
    epost = input('Skriv inn din e-post: ')
    passord = input('Skriv inn ditt passord: ')
    gruppe = loggInn(epost, passord)
    if gruppe:
        hovedmeny(epost, gruppe)
    else:
        print("Innlogging mislyktes. Avslutter programmet.")
