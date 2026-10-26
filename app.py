import streamlit as st
import matplotlib.pyplot as plt

# =========================================================
# STREAMLIT DESIGN (bestehende Optik, bessere Lesbarkeit)
# =========================================================
st.markdown("""
<style>
.stApp {
    background-color: #89CFF0;
}
.block-container {
    padding: 2.5rem 3rem;
    border-radius: 20px;
    background-color: white;
    color: #20232A;
}
/* Lesbarkeit bei dunklem Browser-/Streamlit-Theme */
.block-container h1, .block-container h2, .block-container h3,
.block-container p, .block-container label,
.block-container [data-testid="stMarkdownContainer"] {
    color: #20232A;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E6007E, #009FE3, #F39200, #6A2383);
    color: white;
}
section[data-testid="stSidebar"] * {
    color: white;
}
h1, h2, h3 {
    font-family: "Comic Sans MS", "Trebuchet MS", sans-serif;
}
button {
    border-radius: 25px !important;
    background-color: #E6007E !important;
    color: white !important;
    font-weight: bold;
}
div[data-baseweb="slider"] > div {
    color: #E6007E;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TITEL UND HINWEIS
# =========================================================
st.title("Enterale Ernährung – Bedarfsrechner")
st.caption(
    "Demonstrator mit vereinfachten Rechenmodellen und manuell eingegebenen "
    "Produktdaten; nicht für individuelle Therapieentscheidungen validiert."
)

# =========================================================
# PATIENTENDATEN (wie im Original)
# =========================================================
st.header("Patientendaten")
gewicht = st.number_input("Gewicht (kg)", min_value=30, max_value=200, value=70)
alter = st.number_input("Alter (Jahre)", min_value=0, max_value=100, value=30)

if alter < 18:
    st.warning("⚠️ Dieser Demonstrator ist nur für Erwachsene ab 18 Jahren vorgesehen.")
    st.stop() # Im Original stand st.stopp() – das existiert nicht.

geschlecht = st.selectbox("Geschlecht", options=["Mann", "Frau"])
pal = st.slider("Aktivitätslevel (PAL)", min_value=1.0, max_value=2.4,
                value=1.3, step=0.1)
protein_pro_kg = st.slider("Proteinbedarf (g/kg KG)", min_value=0.6,
                           max_value=2.0, value=1.2, step=0.1)

# =========================================================
# PRODUKTDATEN (wie im Original)
# =========================================================
st.header("Produktdaten (frei wählbar)")
kcal_pro_ml = st.number_input("Energiegehalt (kcal/ml)", min_value=0.5,
                              max_value=3.0, value=1.5, step=0.1)
protein_pro_100ml = st.number_input("Proteingehalt (g/100 ml)", min_value=0.0,
                                    max_value=20.0, value=6.3, step=0.1)
wasser_pro_100ml = st.number_input("Wassergehalt der Sondennahrung (g/100 ml)",
                                   min_value=50.0, max_value=100.0,
                                   value=80.0, step=0.1)
salz_pro_100ml = st.number_input("Salzgehalt der Sondennahrung (g/100 ml)",
                                 min_value=0.0, max_value=1.0,
                                 value=0.1, step=0.01)

protein_pro_ml = protein_pro_100ml / 100
wasser_pro_ml = wasser_pro_100ml / 100
salz_pro_ml = salz_pro_100ml / 100

# =========================================================
# BERECHNUNGEN – FORMELN AUS DEINEM ORIGINAL ÜBERNOMMEN
# =========================================================
if geschlecht == "Frau":
    grundumsatz = (0.047 * gewicht - 0.01452 * alter + 3.21) * 239
else:
    grundumsatz = (0.047 * gewicht + 1.009 - 0.01452 * alter + 3.21) * 239

energiebedarf = grundumsatz * pal
proteinbedarf = protein_pro_kg * gewicht
ml_pro_tag = energiebedarf / kcal_pro_ml
protein_zugefuehrt = ml_pro_tag * protein_pro_ml
salz_zugefuehrt = ml_pro_tag * salz_pro_ml
wasserbedarf = 35 * gewicht
wasser_aus_sonde = ml_pro_tag * wasser_pro_ml
wasser_ergaenzend = max(0.0, wasserbedarf - wasser_aus_sonde)

# =========================================================
# ERGEBNISSE (wie im Original)
# =========================================================
st.header("Ergebnisse")
st.write(f"**Energiebedarf:** {energiebedarf:.0f} kcal/Tag")
st.write(f"**Proteinbedarf:** {proteinbedarf:.1f} g/Tag")
st.write(f"**Gesamtwasserbedarf:** {wasserbedarf:.0f} g/Tag")
st.write("")
st.write(f"**Benötigte Sondenmenge:** {ml_pro_tag:.0f} ml/Tag")
st.write("")
st.write(f"**Proteinzufuhr:** {protein_zugefuehrt:.1f} g/Tag")
st.write(f"**Salzzufuhr:** {salz_zugefuehrt:.1f} g/Tag")
st.write(f"**Wasser aus Sondennahrung:** {wasser_aus_sonde:.0f} g/Tag")
st.write(f"**Zu ergänzendes Wasser:** {wasser_ergaenzend:.0f} g/Tag")

if protein_zugefuehrt >= proteinbedarf:
    st.success("Rechnerisches Proteinziel wird erreicht ✅")
else:
    st.warning("Rechnerisches Proteinziel wird unterschritten ⚠️")

stunden_laufzeit = [16, 20, 24]
ml_h_list = [ml_pro_tag / h for h in stunden_laufzeit]
fig, ax = plt.subplots()
bars = ax.bar([str(h) + " h" for h in stunden_laufzeit],
              ml_h_list, color=["skyblue", "orange", "purple"])
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 2,
            f"{yval:.1f}", ha="center", va="bottom", fontsize=10)
ax.set_xlabel("Laufzeit")
ax.set_ylabel("ml pro Stunde")
ax.set_title("Zufuhrgeschwindigkeit (rein rechnerisch)")
ax.set_ylim(0, max(ml_h_list) * 1.15)
ax.grid(axis="y")
st.pyplot(fig)
plt.close(fig)

# =========================================================
# NEU: REGELBASIERTER NUTRITION ASSISTANT
# =========================================================
st.divider()
st.subheader("🤖 Nutrition Assistant")
st.caption(
    "Erklärt die aktuell angezeigten Ergebnisse anhand deiner Python-Formeln. "
    "Kein Sprachmodell, keine zusätzlichen API-Kosten."
)

# Bei geänderten Eingaben Verlauf zurücksetzen, damit alte Antworten
# nicht fälschlich als Erklärungen der neuen Werte erscheinen.
eingaben = (
    gewicht, alter, geschlecht, pal, protein_pro_kg,
    kcal_pro_ml, protein_pro_100ml, wasser_pro_100ml, salz_pro_100ml,
)
willkommen = {
    "role": "assistant",
    "content": (
        "Hallo! Frage mich zum Beispiel: ‚Warum brauche ich diese Produktmenge?‘, "
        "‚Wie berechnest du das Protein?‘ oder ‚Wie viel ml/h bei 20 Stunden?‘"
    ),
}
if st.session_state.get("nutrition_inputs") != eingaben:
    st.session_state.nutrition_inputs = eingaben
    st.session_state.nutrition_chat = [willkommen]


def beantworte_frage(frage_text: str) -> str:
    f = frage_text.casefold()

    if any(w in f for w in ["protein", "eiweiß", "eiweiss"]):
        unterschied = protein_zugefuehrt - proteinbedarf
        status = ("über" if unterschied >= 0 else "unter")
        return (
            f"**Proteinziel:** {gewicht} kg × {protein_pro_kg:.1f} g/kg = "
            f"**{proteinbedarf:.1f} g/Tag**. Das Produkt enthält "
            f"{protein_pro_100ml:.1f} g Protein je 100 ml. Bei "
            f"{ml_pro_tag:.1f} ml liefert es "
            f"{ml_pro_tag:.1f} × {protein_pro_100ml:.1f} / 100 = "
            f"**{protein_zugefuehrt:.1f} g/Tag**. Das liegt rechnerisch "
            f"{abs(unterschied):.1f} g {status} dem gewählten Ziel. "
            "Die individuelle klinische Eignung wird damit nicht bewertet."
        )

    if any(w in f for w in ["wasser", "flüssigkeit", "fluessigkeit", "trinken"]):
        return (
            f"Dein Rechner setzt pauschal 35 g/kg an: "
            f"35 × {gewicht} = **{wasserbedarf:.0f} g/Tag**. "
            f"Das Produkt liefert {wasser_pro_100ml:.1f} g Wasser je 100 ml. "
            f"Bei {ml_pro_tag:.1f} ml sind das **{wasser_aus_sonde:.0f} g**. "
            f"Die rechnerische Differenz beträgt "
            f"**{wasser_ergaenzend:.0f} g/Tag**. "
            "Andere Flüssigkeitsquellen, Verluste oder Restriktionen berücksichtigt "
            "das vereinfachte Modell nicht."
        )

    if "salz" in f or "natrium" in f:
        return (
            f"Der eingegebene Salzgehalt beträgt {salz_pro_100ml:.2f} g/100 ml. "
            f"{ml_pro_tag:.1f} ml × {salz_pro_100ml:.2f} / 100 = "
            f"**{salz_zugefuehrt:.2f} g Salz/Tag**. "
            "Salz und Natrium dürfen nicht gleichgesetzt werden; "
            "hier wird nur der hinterlegte Salzgehalt berechnet."
        )

    if any(w in f for w in ["16 h", "20 h", "24 h", "stunde", "laufzeit", "geschwindigkeit", "ml/h"]):
        zeilen = [f"- **{h} Stunden:** {ml_pro_tag / h:.1f} ml/h" for h in stunden_laufzeit]
        return (
            f"Für eine errechnete Gesamtmenge von **{ml_pro_tag:.1f} ml** "
            "gilt: ml/h = Gesamtmenge ÷ Laufzeit.\n\n" + "\n".join(zeilen)
            + "\n\nDies sind mathematische Werte, keine Empfehlung "
              "zur individuellen Verabreichung."
        )

    if any(w in f for w in ["energie", "kalori", "kcal", "grundumsatz", "pal"]):
        return (
            "Der Rechner verwendet die im ursprünglichen Code hinterlegte "
            f"Grundumsatzformel. Daraus ergeben sich **{grundumsatz:.0f} kcal/Tag**. "
            f"Mit PAL {pal:.1f}: {grundumsatz:.1f} × {pal:.1f} = "
            f"**{energiebedarf:.0f} kcal/Tag**. "
            "Die Eignung dieser Formel für eine konkrete klinische Situation "
            "ist hier nicht validiert."
        )

    if any(w in f for w in ["sonden", "menge", "volumen", "produkt", "ml", "bedarf decken"]):
        return (
            f"Bei **{energiebedarf:.0f} kcal/Tag** und "
            f"**{kcal_pro_ml:.2f} kcal/ml** ergibt sich "
            f"{energiebedarf:.1f} ÷ {kcal_pro_ml:.2f} = "
            f"**{ml_pro_tag:.1f} ml/Tag**. "
            "Diese Menge deckt rechnerisch den gewählten Energiezielwert, "
            "nicht automatisch sämtliche individuellen Ernährungsbedürfnisse."
        )

    if any(w in f for w in ["hallo", "hilfe", "was kannst", "fragen"]):
        return (
            "Ich kann die Berechnungen zu **Energie, Protein, Wasser, Salz, "
            "Produktmenge und Laufzeit** anhand deiner aktuellen Eingaben erklären. "
            "Ich bin zunächst regelbasiert und kann noch keine freien "
            "Fachfragen oder Studien recherchieren."
        )

    return (
        "Dazu habe ich noch keine hinterlegte Antwort. "
        "Frage beispielsweise nach **Protein**, **Energie**, **Wasser**, "
        "**Salz**, **Produktmenge** oder **Zufuhrgeschwindigkeit**."
    )

for nachricht in st.session_state.nutrition_chat:
    with st.chat_message(nachricht["role"]):
        st.markdown(nachricht["content"])

frage = st.chat_input("Frage zu den aktuellen Berechnungsergebnissen ...")
if frage and frage.strip():
    st.session_state.nutrition_chat.append({"role": "user", "content": frage.strip()})
    st.session_state.nutrition_chat.append({
        "role": "assistant", "content": beantworte_frage(frage.strip())
    })
    st.rerun()

