# main.py

import typer
from pandas import DataFrame
from get_papers.fetch import fetch_and_process_papers

app = typer.Typer()

@app.command()
def get_papers(
    query: str = typer.Argument(..., help="Search query for PubMed"),
    file: str = typer.Option(None, "--file", "-f", help="Filename to save output CSV"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode"),
):
    """
    Fetch PubMed papers for a query and filter non-academic authors.
    """
    try:
        df: DataFrame = fetch_and_process_papers(query, debug)

        if df is None or df.empty:
            print("⚠ No papers found with non-academic affiliations.")
            return

        if file:
            df.to_csv(file, index=False)
            print(f"✅ Results saved to: {file}")
        else:
            print(df.to_string(index=False))

    except Exception as e:
        typer.secho(f"❌ Error: {e}", err=True, fg=typer.colors.RED)

