import streamlit as st

# python modul til udklipsholder.
import pyperclip

# streng med alle mulige tegn og bogstaver som man kan bruge i krypteringen.
bogstaver = "abcdefghijklmnopqrstuvwxyzæøåABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ.:,;-_1234567890+?!=*'^/\"\\ #¤%&()@£$€{[]}<>½§´|¨"

# til streamlit så det ikke ødelægger ting. Gør så funktionen intro() ikke kører mere end 1 gang når man starter streamlit.
intro_begyndt = False

# til streamlit så det ikke ødelægger ting.
# gør så streamlit genindlæser da de forskellige streamlit input funktioner (f.eks. segmented_control) skal have forskellige keys hvilket de ikke får når de bliver kaldt fra funktioner.
rerun_streamlit = False

# intro funktionen bliver brugt til at vælge om man skal kryptere eller dekryptere, hvilket bliver sendt videre til start funktion som bruger det til at vælge den rigtige funktion.
# er_begyndt bestemmer om funktioner kører eller ej, da der bliver kaldt return tidligt hvis den er True.
def intro(er_begyndt):
    if er_begyndt: return
    global intro_begyndt
    intro_begyndt = True

    global rerun_streamlit
    if rerun_streamlit: st.rerun()
    rerun_streamlit = False

    # en segmented control knap bliver lavet med streamlit, og den styrer om man krypterer eller dekrypterer
    krypter_dekrypter = st.segmented_control("", ["Krypter", "Dekrypter"], default="Krypter")
    if krypter_dekrypter == "Krypter":
        start(krypter_dekrypter)
    elif krypter_dekrypter == "Dekrypter":
        start(krypter_dekrypter)

# funktion brugt til at kalde krypter() eller dekrypter() funktionerne.
# tager imod en streng som enten kan være Krypter eller Dekrypter, som bestemmer hvilken funktion der bliver kaldt efter brugeren har inputtet klartekst og nøgle.
def start(krypter_dekrypter):
    klartekst = st.text_input("Input din tekst: ")
    krypteringsnøgle = st.text_input("Input din nøgle: ")

    if krypter_dekrypter == "Krypter" or krypter_dekrypter == "k":
        krypter(klartekst, krypteringsnøgle)
    elif krypter_dekrypter == "Dekrypter" or krypter_dekrypter == "d":
        dekrypter(klartekst, krypteringsnøgle)

# funktion brugt til at kryptere strenge. Tager imod tekst der skal krypteres og nøglen som skal bruges til at kryptere.
def krypter(tekst, nøgle):

    # krypteret tekst variabel bliver defineret til lokalt brug
    krypteret_tekst = ""

    # kører for hvert bogstav i tekst strengen. For-lykken itererer over længden af variablen tekst i stedet for bare tag hvert bogstav da en int skal bruges.
    for i in range(len(tekst)):
        # grunden til at et try-except statement bliver brugt er fordi streamlit kører alt kode for hver frame og ødelægger ting. dette gør så hvis der er errors bliver der bare printet i konsollen.
        try:
            # finder det rigtige index til nøglen ved hjælp af modulus operatoren.
            nøgle_index = i % len(nøgle)

            # finder klartekst bogstav indexet fra bogstaver strengen.
            klartekst_bogstav_index = bogstaver.index(tekst[i])
            # finder nøgle bogstav indexet fra bogstaver strengen.
            nøgle_bogstav_index = bogstaver.index(nøgle[nøgle_index])

            # definerer en ny variabel som er indexet til det krypteret bogstav.
            krypteret_bogstav_index = klartekst_bogstav_index + nøgle_bogstav_index

            # hvis indexet til det krypterede bogstav er for stort vil længden af bogstaver strenget blive trukket fra.
            if krypteret_bogstav_index > len(bogstaver)-1:
                krypteret_bogstav_index -= len(bogstaver)

            # det krypterede bogstav tilføjes til den krypterede tekst.
            krypteret_tekst += bogstaver[krypteret_bogstav_index]
        except ZeroDivisionError: print("ZeroDivisionError")

    # bruger streamlit til at skrive hvad den krypterede tekst er.
    st.write(f"Din krypterede tekst er: {krypteret_tekst}")

    # definerer en streamlit knap som bruges til at kopierer den krypterede tekst til udklipsholderen.
    copy_knap_trykket = st.button("Kopier Tekst")

    # tjekker kopier tekst knappen og kopierer den krypterede tekst til udklipsholderen hvis den er blevet trykket.
    if copy_knap_trykket:
        pyperclip.copy(krypteret_tekst)

# funktion brugt til at dekryptere strenge. Tager imod tekst der skal dekrypteres og nøglen som skal bruges til at dekryptere.
# denne funktion fungerer på præcis samme måde som krypter() funktionen, og derfor bliver der ikke tilføjet kommentarer til denne funktion.
# Se krypter() for en forklaring af funktionen.
def dekrypter(tekst, nøgle):

    dekrypteret_tekst = ""

    for i in range(len(tekst)):
        try:
            nøgle_index = i % len(nøgle)

            krypteret_bogstav_index = bogstaver.index(tekst[i])
            nøgle_bogstav_index = bogstaver.index(nøgle[nøgle_index])

            dekrypteret_bogstav_index = krypteret_bogstav_index - nøgle_bogstav_index

            if dekrypteret_bogstav_index < 0:
                dekrypteret_bogstav_index += len(bogstaver)

            dekrypteret_tekst += bogstaver[dekrypteret_bogstav_index]
        except ZeroDivisionError: print("ZeroDivisionError")

    st.write(f"Din dekrypterede tekst er: {dekrypteret_tekst}")

    copy_knap_trykket = st.button("Kopier Tekst")

    if copy_knap_trykket:
        pyperclip.copy(dekrypteret_tekst)

# titel til brugergrænsefladen
st.title("Vigenére Kryptering")

# starter funktionsloopet
intro(intro_begyndt)