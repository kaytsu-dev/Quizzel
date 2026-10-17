"""Scegli un utente e leggi i riepiloghi dei quiz salvati in punteggi/*.txt."""

from pathlib import Path


SCORES_DIR = Path(__file__).resolve().parent / "punteggi"


def main() -> None:
    SCORES_DIR.mkdir(parents=True, exist_ok=True)
    while True:
        files = sorted(SCORES_DIR.glob("*.txt"), key=lambda path: path.name.casefold())
        print("\n=== Risultati Quizzel ===")
        if not files:
            print("Nessun riepilogo trovato. Completa un quiz per creare un file.")
        else:
            for index, path in enumerate(files, start=1):
                print(f"{index}. {path.stem.replace('_', ' ')}")
        choice = input("\nNumero del giocatore (Invio aggiorna, q esce): ").strip().casefold()
        if choice == "q":
            return
        if not choice:
            continue
        try:
            selected = int(choice) - 1
            path = files[selected]
        except (ValueError, IndexError):
            print("Scelta non valida: inserisci uno dei numeri nell’elenco.")
            continue
        print("\n" + "=" * 68)
        print(path.read_text(encoding="utf-8"))
        print("=" * 68)
        input("Premi Invio per tornare all’elenco…")


if __name__ == "__main__":
    main()
