import pandas as pd
import os
import matplotlib.pyplot as plt
import google.generativeai as genai
from datetime import datetime

# Nastavenie API kľúča pre Google Gemini
# Poznámka: Nastavte environmentálnu premennú GOOGLE_API_KEY s vaším API kľúčom
genai.configure(api_key='')

def nacitaj_data(subor):
    """
    Načíta CSV súbor s údajmi používateľov.
    Spracuje chýbajúce hodnoty: pre numerické stĺpce použije medián, pre kategorické odstráni riadky.
    """
    try:
        df = pd.read_csv(subor)
        # Spracovanie chýbajúcich hodnôt
        for stlpec in df.columns:
            if df[stlpec].dtype in ['int64', 'float64']:
                df[stlpec].fillna(df[stlpec].median(), inplace=True)
            else:
                df.dropna(subset=[stlpec], inplace=True)
        return df
    except FileNotFoundError:
        print(f"Chyba: Súbor '{subor}' nebol nájdený.")
        return None
    except Exception as e:
        print(f"Chyba pri načítaní dát: {e}")
        return None

def vypocitaj_zakladne_statistiky(df):
    """
    Vypočíta základné štatistiky pre numerické stĺpce.
    Vráti slovník so štatistikami.
    """
    numericke_stlpce = df.select_dtypes(include=['number']).columns
    statistiky = {}
    for stlpec in numericke_stlpce:
        data = df[stlpec].dropna()
        statistiky[stlpec] = {
            'Priemer': data.mean(),
            'Medián': data.median(),
            'Modus': data.mode().iloc[0] if not data.mode().empty else 'N/A',
            'Štandardná odchýlka': data.std(),
            'Minimálna hodnota': data.min(),
            'Maximálna hodnota': data.max(),
            'Rozsah': data.max() - data.min(),
            '25. percentil': data.quantile(0.25),
            '75. percentil': data.quantile(0.75)
        }
    return statistiky

def vytvor_grafy(df, adresar_grafov):
    """
    Vytvorí a uloží grafy pre vizualizáciu dát.
    """
    os.makedirs(adresar_grafov, exist_ok=True)

    # Histogram pre platy
    plt.figure(figsize=(10, 6))
    plt.hist(df['salary'], bins=10, edgecolor='black')
    plt.title('Distribúcia platov')
    plt.xlabel('Plat')
    plt.ylabel('Počet používateľov')
    plt.savefig(os.path.join(adresar_grafov, 'histogram_platov.png'))
    plt.close()

    # Stĺpcový graf pre top 5 povolaní
    top_povolania = df['occupation'].value_counts().head(5)
    plt.figure(figsize=(10, 6))
    top_povolania.plot(kind='bar')
    plt.title('Top 5 povolaní')
    plt.xlabel('Povolanie')
    plt.ylabel('Počet')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(adresar_grafov, 'top_povolania.png'))
    plt.close()

    # Čiarový graf pre platy podľa dátumu vytvorenia (ak je možné zoradiť)
    df_sorted = df.sort_values('created_at')
    plt.figure(figsize=(10, 6))
    plt.plot(df_sorted['created_at'], df_sorted['salary'], marker='o')
    plt.title('Platy podľa dátumu vytvorenia')
    plt.xlabel('Dátum vytvorenia')
    plt.ylabel('Plat')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(adresar_grafov, 'platy_podla_datumu.png'))
    plt.close()

def analyzuj_s_gemini(statistiky, df_info):
    """
    Použije Google Gemini na analýzu dát na základe štatistík.
    Vráti odpoveď od AI.
    """
    prompt = f"""
    Analyzujte nasledujúce údaje o používateľoch. Poskytnite prehľadné zhrnutie, kľúčové poznatky a odporúčania.

    Informácie o dátach:
    - Celkový počet záznamov: {df_info['pocet_zaznamov']}
    - Počet stĺpcov: {df_info['pocet_stlpcov']}
    - Stĺpce: {', '.join(df_info['stlpce'])}

    Štatistiky pre numerické stĺpce:
    {statistiky}

    Poskytnite analýzu v slovenčine, ktorá zahŕňa:
    1. Prehľad dát
    2. Kľúčové trendy a vzory
    3. Odporúčania pre ďalšie kroky
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Chyba pri komunikácii s Gemini: {e}")
        return "Nebolo možné získať analýzu od AI."

def vytvor_markdown_report(analyza_gemini, statistiky, df_info, adresar_grafov, vystupny_subor):
    """
    Vytvorí Markdown súbor s reportom analýzy.
    """
    with open(vystupny_subor, 'w', encoding='utf-8') as f:
        f.write("# Analýza údajov používateľov pomocou AI (Gemini)\n\n")
        f.write(f"*Vygenerované dňa: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

        # Prehľad dát
        f.write("## Prehľad dát\n\n")
        f.write(f"- **Celkový počet záznamov:** {df_info['pocet_zaznamov']}\n")
        f.write(f"- **Počet stĺpcov:** {df_info['pocet_stlpcov']}\n")
        f.write(f"- **Stĺpce:** {', '.join(df_info['stlpce'])}\n\n")

        # Štatistiky
        f.write("## Štatistiky numerických stĺpcov\n\n")
        for stlpec, stats in statistiky.items():
            f.write(f"### {stlpec}\n\n")
            tabulka = "| Štatistika | Hodnota |\n|------------|--------|\n"
            for stat, hodnota in stats.items():
                if isinstance(hodnota, (int, float)) and not pd.isna(hodnota):
                    tabulka += f"| {stat} | {hodnota:.2f} |\n"
                else:
                    tabulka += f"| {stat} | {hodnota} |\n"
            f.write(tabulka + "\n")

        # Grafy
        f.write("## Grafy\n\n")
        grafy = [
            ('histogram_platov.png', 'Distribúcia platov'),
            ('top_povolania.png', 'Top 5 povolaní'),
            ('platy_podla_datumu.png', 'Platy podľa dátumu vytvorenia')
        ]
        for obrazok, popis in grafy:
            cesta = os.path.join(adresar_grafov, obrazok)
            if os.path.exists(cesta):
                f.write(f"### {popis}\n\n")
                f.write(f"![{popis}]({cesta})\n\n")

        # Analýza od Gemini
        f.write("## AI Analýza (Gemini)\n\n")
        f.write(analyza_gemini + "\n\n")

def hlavna_funkcia():
    """
    Hlavná funkcia na orchestráciu analýzy dát.
    """
    subor_dat = 'users_data4.csv'
    vystupny_subor = 'analyza_dat_ai.md'
    adresar_grafov = 'grafy'

    # Načítanie dát
    df = nacitaj_data(subor_dat)
    if df is None:
        return

    # Informácie o dátach
    df_info = {
        'pocet_zaznamov': len(df),
        'pocet_stlpcov': len(df.columns),
        'stlpce': list(df.columns)
    }

    # Výpočet štatistík
    statistiky = vypocitaj_zakladne_statistiky(df)

    # Vytvorenie grafov
    vytvor_grafy(df, adresar_grafov)

    # Analýza pomocou Gemini
    analyza_gemini = analyzuj_s_gemini(statistiky, df_info)

    # Vytvorenie Markdown reportu
    vytvor_markdown_report(analyza_gemini, statistiky, df_info, adresar_grafov, vystupny_subor)

    print(f"Analýza dokončená. Výsledky uložené v '{vystupny_subor}' a grafy v adresári '{adresar_grafov}'.")

if __name__ == "__main__":
    hlavna_funkcia()